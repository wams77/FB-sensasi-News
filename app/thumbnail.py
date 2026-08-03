from __future__ import annotations

from pathlib import Path
from textwrap import fill
from urllib.parse import quote
from io import BytesIO

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
            parents=True,
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

    def generate_ai_image(self, headline: str, category: str) -> Image.Image | None:
        try:
            clean_headline = headline.encode("ascii", "ignore").decode("ascii")
            if not clean_headline.strip():
                clean_headline = "breaking news update"
                
            prompt = f"Cinematic professional news background about {clean_headline}, category {category}, high quality"
            encoded_prompt = quote(prompt)
            ai_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={WIDTH}&height={HEIGHT}&nologo=true&seed=42"
            
            logger.info("Membuat gambar AI via Pollinations: %s", clean_headline[:30])
            r = requests.get(ai_url, timeout=30)
            if r.status_code == 200:
                return Image.open(BytesIO(r.content)).convert("RGB")
        except Exception as e:
            logger.warning("Gagal membuat gambar AI dari Pollinations: %s", e)
        return None

    def dark_overlay(self, image):
        overlay = Image.new("RGBA", image.size, (0, 0, 0, 140))
        image = image.convert("RGBA")
        image.alpha_composite(overlay)
        return image.convert("RGB")

    def generate(self, article: NewsArticle) -> str:
        try:
            image = None
            headline_text = article.headline or article.title or "Breaking News"
            
            # Coba buat gambar via Pollinations AI
            image = self.generate_ai_image(headline_text, article.category)
            
            # Fallback jika AI gagal (latar belakang warna gelap elegan)
            if image is None:
                logger.info("Menggunakan background warna solid sebagai fallback thumbnail.")
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
            logger.info("Thumbnail berhasil disimpan: %s", article.thumbnail)
            return article.thumbnail
            
        except Exception as e:
            logger.exception("Gagal total membuat thumbnail: %s", e)
            return ""
