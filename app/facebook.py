from __future__ import annotations

import time
import requests

from config import (
    FACEBOOK_PAGE_ID,
    FACEBOOK_ACCESS_TOKEN,
    MAX_RETRY,
    REQUEST_TIMEOUT,
)

from logger import logger
from models import NewsArticle


GRAPH_URL = "https://graph.facebook.com/v23.0"


class FacebookPublisher:

    def __init__(self):

        self.feed_url = (
            f"{GRAPH_URL}/{FACEBOOK_PAGE_ID}/feed"
        )

        self.photo_url = (
            f"{GRAPH_URL}/{FACEBOOK_PAGE_ID}/photos"
        )

    def _request(
        self,
        url: str,
        payload: dict,
    ):

        payload["access_token"] = FACEBOOK_ACCESS_TOKEN

        for _ in range(MAX_RETRY):

            try:

                response = requests.post(

                    url,

                    data=payload,

                    timeout=REQUEST_TIMEOUT,

                )

                if response.ok:

                    return response.json()

                logger.error(response.text)

            except Exception as e:

                logger.exception(e)

            time.sleep(2)

        return None

    def publish_text(
        self,
        message: str,
        link: str,
    ):

        payload = {

            "message": message,

            "link": link,

        }

        return self._request(

            self.feed_url,

            payload,

        )

    def publish_photo(
        self,
        image: str,
        caption: str,
    ):

        payload = {

            "url": image,

            "caption": caption,

        }

        return self._request(

            self.photo_url,

            payload,

        )

    def build_caption(
        self,
        article: NewsArticle,
    ) -> str:

        hashtags = " ".join(
            article.hashtags
        )

        text = f"""{article.headline}

{article.caption}

{hashtags}
"""

        return text.strip()

    def publish(
        self,
        article: NewsArticle,
    ) -> str | None:

        caption = self.build_caption(
            article
        )

        if article.image:

            result = self.publish_photo(

                article.image,

                caption,

            )

        else:

            result = self.publish_text(

                caption,

                article.link,

            )

        if not result:

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
