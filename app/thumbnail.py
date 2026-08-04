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

WIDTH = 1200
HEIGHT = 630


class ThumbnailGenerator:

    def __init__(self):
        self.output = CACHE_DIR / "thumbs"
        self.output.mkdir(parents=True, exist_ok=True)
        
        # --- AUTO DOWNLOAD FONT JIKA TIDAK ADA ---
        font_path = Path("assets/fonts/Poppins-Bold.ttf")
        if not font_path.exists():
            logger.info("Font tidak ditemukan. Mengunduh Poppins-Bold.ttf otomatis...")
            font_path.parent.mkdir(parents=True, exist_ok=True)
            font_url = "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf"
            try:
                urllib.request.urlretrieve(font_url, font_path)
                logger.info("Font berhasil diunduh!")
            except Exception as e:
                logger.error("Gagal mengunduh font: %s", e)

        try:
            self.title_font = ImageFont.truetype(str(font_path), 58)
            self.brand_font = ImageFont.truetype(str(font_path), 30)
            self.label_font = ImageFont.truetype(str(font_path), 26)
        except Exception as e:
            logger.error("FONT TIDAK DITEMUKAN! Menggunakan font default kecil. Error: %s", e)
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
                
                # Jika resolusi asli gambar terlalu kecil, buang agar tidak buram/pecah saat diperbesar
                if img.width < 400 or img.height < 300:
                    logger.warning("Gambar bawaan terlalu kecil (%dx%d). Menggunakan background solid.", img.width, img.height)
                    return None

                # Gunakan ImageOps.fit untuk memotong (crop) proporsional, BUKAN resize yang bikin gepeng
                img = ImageOps.fit(img, (WIDTH, HEIGHT), Image.Resampling.LANCZOS)
                return img
        except Exception as e:
            logger.warning("Gagal mendownload gambar asli: %s", e)
        return None

    def dark_overlay(self, image):
        overlay = Image.new("RGBA", image.size, (0, 0, 0, 140))
        image = image.convert("RGBA")
        image.alpha_composite(overlay)
        return image.convert("RGB")

    def generate(self, article: NewsArticle) -> str:
        try:
            headline_text = article.headline or article.title or "Breaking News"
            
            # Coba ambil gambar asli dari artikel
            image = self.download_image(article.image)
            
            # Fallback jika berita tidak punya gambar atau gambarnya buram
            if image is None:
                logger.info("Gambar berita tidak valid, menggunakan background solid.")
                image = Image.new("RGB", (WIDTH, HEIGHT), color=(15, 23, 42))

            image = self.dark_overlay(image)
            draw = ImageDraw.Draw(image)

            # BREAKING LABEL
            draw.rounded_rectangle(
                (40, 40, 260, 90),
                radius=12,
                fill=(220, 0, 0),
            )
            draw.text(
                (60, 50),
                "BREAKING",
                font=self.label_font,
                fill="white",
            )

            # TITLE
            title = fill(headline_text, width=26)
            draw.multiline_text(
                (60, 140),
                title,
                font=self.title_font,
                fill="white",
                spacing=12,
            )

            # BRAND
            draw.text(
                (60, HEIGHT - 70),
                "Gosip.ID",
                font=self.brand_font,
                fill="white",
            )

            safe_title = article.title if article.title else "news_article"
            filename = (
                safe_title[:40]
                .replace("/", "_")
                .replace("\\", "_")
                .replace(":", "_")
                .replace("*", "_")
                .replace("?", "_")
                .replace("\"", "_")
                .replace("<", "_")
                .replace(">", "_")
                .replace("|", "_")
                + ".jpg"
            )
            output = self.output / filename
            image.save(output, quality=95)
            
            article.thumbnail = str(output.resolve())
            logger.info("Thumbnail dari gambar asli berhasil disimpan: %s", article.thumbnail)
            return article.thumbnail
            
        except Exception as e:
            logger.exception("Gagal total membuat thumbnail: %s", e)
            return ""
