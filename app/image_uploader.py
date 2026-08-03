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


GRAPH_URL = "https://graph.facebook.com/v23.0"


class ImageUploader:

    def __init__(self):
        self.url = (
            f"{GRAPH_URL}/{FACEBOOK_PAGE_ID}/photos"
        )

    def upload(
        self,
        image_path: str,
        caption: str = "",
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
            with open(
                image,
                "rb",
            ) as fp:
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
                    self.url,
                    files=files,
                    data=data,
                    timeout=REQUEST_TIMEOUT,
                )
        except Exception as e:
            logger.exception("Gagal melakukan HTTP request ke Facebook: %s", e)
            return None

        logger.info(
            response.text
        )

        if not response.ok:
            logger.error(
                response.text
            )
            return None

        try:
            result = response.json()
        except Exception as e:
            logger.exception("Gagal memparsing JSON dari respons Facebook: %s", e)
            return None

        photo_id = result.get("id")

        if not photo_id:
            logger.error(
                "Facebook response does not contain photo id"
            )
            return None

        logger.info(
            "Photo Uploaded : %s",
            photo_id,
        )
        return photo_id


if __name__ == "__main__":
    uploader = ImageUploader()
    photo_id = uploader.upload(
        "cache/thumbs/test.jpg",
        "Upload test dari Gosip.ID"
    )
    print(photo_id)
