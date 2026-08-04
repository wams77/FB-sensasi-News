from __future__ import annotations

import urllib.request
from pathlib import Path
from textwrap import fill
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps

from config import CACHE_DIR
from logger import logger
from models import NewsArticle

# STANDAR UKURAN FACEBOOK LINK PREVIEW
WIDTH = 1200
HEIGHT = 630


class ThumbnailGenerator:

    def __init__(self):
        self.output = CACHE_DIR / "thumbs"
        self.output.mkdir(parents=True, exist_ok=True)
        
        # --- AUTO DOWNLOAD FONT ---
        font_path = Path("assets/fonts/Poppins-Bold.ttf")
        if not font_path.exists():
            logger.info("Font tidak ditemukan. Mengunduh Poppins-Bold.ttf otomatis...")
            font_path.parent.mkdir(parents=True, exist_ok=True)
            font_url = "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf"
            try:
                urllib.request.urlretrieve(font_url, font_path)
            except Exception as e:
                logger.error("Gagal mengunduh font: %s", e)

        try:
            # Ukuran font disesuaikan agar pas di layar HP (Mobile Feed FB)
            self.title_font = ImageFont.truetype(str(font_path), 54)
            self.brand_font = ImageFont.truetype(str(font_path), 28)
            self.label_font = ImageFont.truetype(str(font_path), 24)
        except Exception:
            self.title_font = ImageFont.load_default()
            self.brand_font = ImageFont.load_default()
            self.label_font = ImageFont.load_default()

    def download_image(self, image_url: str | None) -> Image.Image | None:
        if not image_url:
            return None
        try:
            logger.info("Mengunduh gambar asli dari berita: %s", image_url[:50])
            response = requests.get(image_url, timeout=15)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content)).convert("RGB")
                # Tetap ambil semua ukuran gambar, crop ke 1200x630 tanpa merusak proporsi
                img = ImageOps.fit(img, (WIDTH, HEIGHT), Image.Resampling.LANCZOS)
                return img
        except Exception as e:
            logger.warning("Gagal mendownload gambar asli: %s", e)
        return None

    def dark_overlay(self, image):
        # Menggelapkan gambar dengan opasitas 150 agar teks sangat kontras dan mudah dibaca di FB
        overlay = Image.new("RGBA", image.size, (15, 23, 42, 160))
        image = image.convert("RGBA")
        image.alpha_composite(overlay)
        return image.convert("RGB")

    def generate(self, article: NewsArticle) -> str:
        try:
            headline_text = article.headline or article.title or "Breaking News"
            
            image = self.download_image(article.image)
            
            if image is None:
                # Fallback jika tidak ada gambar sama sekali
                logger.info("Gambar berita tidak ada, menggunakan background solid.")
                image = Image.new("RGB", (WIDTH, HEIGHT), color=(15, 23, 42))

            image = self.dark_overlay(image)
            draw = ImageDraw.Draw(image)

            # ZONA AMAN FACEBOOK (SAFE ZONE)
            # Menghindari bagian ujung yang sering ter-crop di HP
            margin_left = 80
            margin_top = 80

            # 1. KOTAK BREAKING LABEL
            label_text = "BREAKING NEWS"
            # Menghitung panjang kotak otomatis berdasarkan teks
            bbox = draw.textbbox((0, 0), label_text, font=self.label_font)
            label_width = bbox[2] - bbox[0] + 40  # Padding kiri-kanan 20px
            label_height = 50
            
            draw.rounded_rectangle(
                (margin_left, margin_top, margin_left + label_width, margin_top + label_height),
                radius=10,
                fill=(220, 38, 38), # Warna Merah Terang Modern
            )
            draw.text(
                (margin_left + 20, margin_top + 8),
                label_text,
                font=self.label_font,
                fill="white",
            )

            # 2. JUDUL BERITA (TITLE)
            # Lebar teks dibatasi agar tidak menyentuh ujung kanan gambar
            title = fill(headline_text, width=32)
            draw.multiline_text(
                (margin_left, margin_top + 90),
                title,
                font=self.title_font,
                fill="white",
                spacing=16, # Jarak antar baris teks diperlebar agar rapi
            )

            # 3. BRAND GOSIP.ID (Di sudut bawah)
            draw.text(
                (margin_left, HEIGHT - 90),
                "Gosip.ID",
                font=self.brand_font,
                fill=(203, 213, 225), # Warna teks abu-abu terang elegan
            )

            # FORMATTING NAMA FILE
            safe_title = article.title if article.title else "news_article"
            filename = "".join(c if c.isalnum() or c in " _-" else "_" for c in safe_title)[:40].strip() + ".jpg"
            output = self.output / filename
            
            # Simpan dengan kualitas HD (95%)
            image.save(output, quality=95)
            
            article.thumbnail = str(output.resolve())
            return article.thumbnail
            
        except Exception as e:
            logger.exception("Gagal total membuat thumbnail: %s", e)
            return ""
