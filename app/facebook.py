from __future__ import annotations

import time
from pathlib import Path

import requests

from config import (
    FACEBOOK_ACCESS_TOKEN,
    FACEBOOK_PAGE_ID,
    REQUEST_TIMEOUT,
    MAX_RETRY,
)

from logger import logger
from models import NewsArticle
from post_builder import PostBuilder


GRAPH_URL = "https://graph.facebook.com/v23.0"


class FacebookPublisher:

    def __init__(self):

        self.builder = PostBuilder()

        self.photo_endpoint = (
            f"{GRAPH_URL}/{FACEBOOK_PAGE_ID}/photos"
        )

    def upload_photo(

        self,

        image_path: str,

        caption: str,

    ):

        image = Path(image_path)

        if not image.exists():

            logger.error(

                "Image not found : %s",

                image_path,

            )

            return None

        for _ in range(MAX_RETRY):

            try:

                with open(image, "rb") as fp:

                    files = {

                        "source": fp

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

                logger.info(

                    response.text

                )

                if response.ok:

                    return response.json()

            except Exception as e:

                logger.exception(e)

            time.sleep(2)

        return None
            def publish(

        self,

        article: NewsArticle,

    ) -> str | None:

        if not article.thumbnail:

            logger.error(

                "Thumbnail not found."

            )

            return None

        caption = self.builder.build(

            article

        )

        result = self.upload_photo(

            article.thumbnail,

            caption,

        )

        if not result:

            logger.error(

                "Facebook upload failed."

            )

            return None

        post_id = (

            result.get("post_id")

            or result.get("id")

        )

        article.facebook_post_id = (

            post_id

        )

        article.posted = True

        logger.info(

            "Facebook Success : %s",

            post_id,

        )

        return post_id
        if __name__ == "__main__":

    article = NewsArticle(

        title="Dummy",

        summary="",

        link="https://example.com",

        image="https://picsum.photos/1200/630",

        source="BBC",

        category="football",

        published=None,

    )

    article.headline = (

        "Arsenal Dapat Angin Segar"

    )

    article.article = (

        "Arsenal mendapatkan kabar baik menjelang musim baru. "

        "Pemain andalan mereka dipastikan kembali mengikuti "

        "latihan penuh bersama skuad utama setelah pulih dari "

        "cedera. Kehadiran sang pemain diharapkan mampu "

        "meningkatkan performa tim dalam persaingan musim ini."

    )

    article.hashtags = [

        "#Arsenal",

        "#PremierLeague",

        "#Football",

    ]

    article.emoji = "🔥"

    article.thumbnail = "cache/thumbs/test.jpg"

    publisher = FacebookPublisher()

    post_id = publisher.publish(

        article

    )

    print(

        "POST ID:",

        post_id

    )
