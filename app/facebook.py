from __future__ import annotations

import time

import requests

from config import (
    FACEBOOK_ACCESS_TOKEN,
    FACEBOOK_PAGE_ID,
    MAX_RETRY,
    REQUEST_TIMEOUT,
)

from logger import logger
from models import NewsArticle


GRAPH_URL = "https://graph.facebook.com/v23.0"


class FacebookPublisher:

    def __init__(self):

        self.photo_url = (
            f"{GRAPH_URL}/{FACEBOOK_PAGE_ID}/photos"
        )

    def request(
        self,
        payload: dict,
    ):

        payload["access_token"] = FACEBOOK_ACCESS_TOKEN

        for _ in range(MAX_RETRY):

            try:

                response = requests.post(

                    self.photo_url,

                    data=payload,

                    timeout=REQUEST_TIMEOUT,

                )

                logger.info(

                    response.text

                )

                if response.ok:

                    return response.json()

            except Exception as e:

                logger.exception(e)

            time.sleep(2)

        return None

    def build_caption(
        self,
        article: NewsArticle,
    ) -> str:

        hashtags = " ".join(
            article.hashtags
        )

        caption = f"""{article.emoji} {article.headline}

{article.article}

{hashtags}

━━━━━━━━━━━━━━
📢 Ikuti Gosip.ID untuk berita olahraga & hiburan terbaru.
"""

        return caption.strip()

    def publish(
        self,
        article: NewsArticle,
    ):

                caption = self.build_caption(
            article
        )

        payload = {

            # Upload foto dari URL RSS
            "url": article.image,

            # Artikel hasil AI
            "caption": caption,

            # Pastikan muncul di timeline
            "published": "true",

        }

        result = self.request(
            payload
        )

        if not result:

            logger.error(

                "Facebook Failed : %s",

                article.title,

            )

            return None

        post_id = (

            result.get("post_id")

            or result.get("id")

        )

        article.facebook_post_id = post_id

        article.posted = True

        logger.info(

            "Facebook Success : %s",

            article.title,

        )

        return post_id


if __name__ == "__main__":

    article = NewsArticle(

        title="Dummy",

        summary="",

        link="",

        image="https://picsum.photos/1200/630",

        source="Test",

        category="football",

        published=None,

    )

    article.headline = "Judul Berita"

    article.article = (
        "Ini adalah artikel hasil AI. "
        "Artikel ini hanya digunakan "
        "untuk pengujian upload ke Facebook."
    )

    article.hashtags = [

        "#Football",

        "#Breaking",

    ]

    article.emoji = "🔥"

    FacebookPublisher().publish(
        article
    )
