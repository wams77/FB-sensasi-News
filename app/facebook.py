from __future__ import annotations

import mimetypes
from pathlib import Path

import requests

from config import (
    FACEBOOK_ACCESS_TOKEN,
    FACEBOOK_PAGE_ID,
    REQUEST_TIMEOUT,
)
from logger import logger
from models import NewsArticle
from post_builder import PostBuilder
from thumbnail import ThumbnailGenerator


GRAPH_URL = "https://graph.facebook.com/v23.0"


class FacebookPublisher:

    def __init__(self):
        self.builder = PostBuilder()
        self.thumbnail_gen = ThumbnailGenerator()
        self.photo_endpoint = (
            f"{GRAPH_URL}/{FACEBOOK_PAGE_ID}/photos"
        )

    def upload_photo(
        self,
        image_path: str,
        caption: str,
    ) -> str | None:
        image = Path(image_path)
        if not image.exists():
            logger.error(
                "Image not found : %s",
                image_path,
            )
            return None

        mime = mimetypes.guess_type(
            image.name
        )[0] or "image/jpeg"

        try:
            with open(image, "rb") as fp:
                files = {
                    "source": (
                        image.name,
                        fp,
                        mime,
                    )
                }
                data = {
                    "caption": caption,
                    "published": "true",
                    "access_token": FACEBOOK_ACCESS_TOKEN,
                }
                response = requests.post(
                    self.photo_endpoint,
                    files=files,
                    data=data,
                    timeout=REQUEST_TIMEOUT,
                )
        except Exception as e:
            logger.exception("Gagal koneksi ke Facebook Graph API: %s", e)
            return None

        logger.info(response.text)

        if not response.ok:
            logger.error(response.text)
            return None

        try:
            result = response.json()
        except Exception:
            return None

        post_id = result.get("id") or result.get("post_id")
        return post_id

    def publish(
        self,
        article: NewsArticle,
    ) -> str | None:
        # Buat thumbnail otomatis menggunakan generator
        thumb_path = self.thumbnail_gen.generate(article)
        if not thumb_path:
            logger.error("Thumbnail generation failed.")
            return None

        caption = self.builder.build(
            article
        )

        post_id = self.upload_photo(
            thumb_path,
            caption,
        )

        if not post_id:
            logger.error(
                "Facebook upload failed."
            )
            return None

        article.facebook_post_id = post_id
        article.posted = True

        logger.info(
            "Facebook Success : %s",
            post_id,
        )
        return post_id
