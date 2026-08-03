from __future__ import annotations

from pathlib import Path
from textwrap import fill
from urllib.parse import quote

import requests

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)

from config import CACHE_DIR
from logger import logger
from models import NewsArticle


WIDTH = 1200
HEIGHT = 630


class ThumbnailGenerator:

    def __init__(self):
        self.output = CACHE_DIR / "thumbs"
        self.output.mkdir(
            exist_ok=True
        )
        try:
            self.title_font = ImageFont.truetype(
                "assets/fonts/Poppins-Bold.ttf",
                58
            )
            self.brand_font = ImageFont.truetype(
                "assets/fonts/Poppins-Bold.ttf",
                30
            )
            self.label_font = ImageFont.truetype(
                "assets/fonts/Poppins-Bold.ttf",
                26
            )
        except Exception:
            self.title_font = ImageFont.load_default()
            self.brand_font = ImageFont.load_default()
            self.label_font = ImageFont.load_default()

    def download_image(
        self,
        url: str | None,
    ):
        if not url:
            raise ValueError("Image URL is empty")
        
        r = requests.get(
            url,
            timeout=30,
        )
        r.raise_for_status()
        return Image.open(
            r.raw
        ).convert(
            "RGB"
        )

    def generate_ai_image(self, headline: str, category: str) -> Image.Image | None:
        """
        Menghasilkan gambar AI menggunakan Pollinations AI berdasarkan headline berita.
        """
        try:
            # Buat prompt bahasa Inggris yang deskriptif agar hasil gambar AI lebih optimal
            clean_headline = headline.encode("ascii", "ignore").decode("ascii")
            prompt = f"Professional cinematic news background about {clean_headline}, category {category}, high quality, 4k"
            encoded_prompt = quote(prompt)
            
            # URL API Pollinations AI (Flux / default model)
            ai_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={WIDTH}&height={HEIGHT}&nologo=true"
            
            logger.info("Membuat gambar AI via Pollinations AI untuk: %s", headline)
            r = requests.get(ai_url, timeout=45)
            if r.status_code == 200:
                from io import BytesIO
                return Image.open(BytesIO(r.content)).convert("RGB")
        except Exception as e:
            logger.warning("Gagal membuat gambar AI dari Pollinations: %s", e)
        
        return None

    def dark_overlay(
        self,
        image,
    ):
        overlay = Image.new(
            "RGBA",
            image.size,
            (0, 0, 0, 140)
        )
        image = image.convert(
            "RGBA"
        )
        image.alpha_composite(
            overlay
        )
        return image.convert(
            "RGB"
        )

    def fit_image(
        self,
        image,
    ):
        image.thumbnail(
            (
                WIDTH,
                HEIGHT
            )
        )
        canvas = Image.new(
            "RGB",
            (
                WIDTH,
                HEIGHT
            )
        )
        x = (
            WIDTH -
            image.width
        ) // 2
        y = (
            HEIGHT -
            image.height
        ) // 2
        canvas.paste(
            image,
            (
                x,
                y
            )
        )
        return canvas

    def generate(
        self,
        article: NewsArticle,
    ) -> str:
        try:
            image = None
            
            # 1. Coba unduh gambar asli dari artikel terlebih dahulu
            if article.image:
                try:
                    image = self.download_image(article.image)
                    image = self.fit_image(image)
                    image = self.dark_overlay(image)
                except Exception as img_err:
                    logger.warning("Gagal unduh gambar asli (%s). Mencoba buat via AI...", img_err)

            # 2. Jika gambar asli tidak ada/gagal, generate menggunakan Pollinations AI
            if image is None:
                headline_text = article.headline or article.title or "Breaking News"
                image = self.generate_ai_image(headline_text, article.category)
                if image:
                    image = self.dark_overlay(image)

            # 3. Fallback terakhir jika AI juga gagal (warna solid gelap)
            if image is None:
                image = Image.new("RGB", (WIDTH, HEIGHT), color=(15, 23, 42))
                image = self.dark_overlay(image)

            draw = ImageDraw.Draw(
                image
            )
            # BREAKING LABEL
            draw.rounded_rectangle(
                (
                    40,
                    40,
                    260,
                    90,
                ),
                radius=12,
                fill=(220, 0, 0),
            )
            draw.text(
                (
                    60,
                    50,
                ),
                "BREAKING",
                font=self.label_font,
                fill="white",
            )
            # TITLE
            headline_text = article.headline or article.title or "Berita Terbaru"
            title = fill(
                headline_text,
                width=26,
            )
            draw.multiline_text(
                (
                    60,
                    140,
                ),
                title,
                font=self.title_font,
                fill="white",
                spacing=12,
            )
            # BRAND
            draw.text(
                (
                    60,
                    HEIGHT - 70,
                ),
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
            image.save(
                output,
                quality=95,
            )
            article.thumbnail = str(
                output
            )
            logger.info(
                "Thumbnail : %s",
                output,
            )
            return str(output)
        except Exception as e:
            logger.exception(e)
            return ""


if __name__ == "__main__":
    article = NewsArticle(
        title="Dummy",
        summary="",
        link="",
        image=None,  # Sengaja dikosongkan untuk menguji Pollinations AI
        source="Test",
        category="football",
        published=None,
    )
    article.headline = (
        "Arsenal Dapat Angin Segar "
        "Jelang Musim Baru"
    )
    ThumbnailGenerator().generate(
        article
    )
