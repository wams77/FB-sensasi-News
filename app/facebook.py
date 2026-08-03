"""
facebook.py

Facebook Graph API Publisher
"""

import logging
import time
from typing import Optional

import requests

from config import (
    FACEBOOK_ACCESS_TOKEN,
    FACEBOOK_PAGE_ID,
)

logger = logging.getLogger(__name__)

GRAPH = "https://graph.facebook.com/v23.0"

TIMEOUT = 60

MAX_RETRY = 3

class FacebookPublisher:

    def __init__(self):

        self.feed_url = (
            f"{GRAPH}/{FACEBOOK_PAGE_ID}/feed"
        )

        self.photo_url = (
            f"{GRAPH}/{FACEBOOK_PAGE_ID}/photos"
        )

        self.comment_url = GRAPH

    def request(
        self,
        url,
        payload,
    ):

        payload["access_token"] = FACEBOOK_ACCESS_TOKEN

        for retry in range(MAX_RETRY):

            try:

                r = requests.post(

                    url,

                    data=payload,

                    timeout=TIMEOUT

                )

                if r.status_code == 200:

                    return r.json()

                logger.warning(r.text)

            except Exception as e:

                logger.warning(e)

            time.sleep(2)

        return None

    def publish_text(

        self,

        message,

        link,

    ):

        payload = {

            "message": message,

            "link": link

        }

        return self.request(

            self.feed_url,

            payload

        )

    def publish_photo(

        self,

        image,

        caption,

    ):

        payload = {

            "url": image,

            "caption": caption

        }

        return self.request(

            self.photo_url,

            payload

        )

    def comment(

        self,

        post_id,

        message,

    ):

        payload = {

            "message": message

        }

        return self.request(

            f"{GRAPH}/{post_id}/comments",

            payload

        )

    def publish(

        self,

        article,

    ):

        hashtags = ""

        if article.hashtags:

            hashtags = " ".join(

                article.hashtags

            )

        caption = f"""

{article.headline}

{article.caption}

{hashtags}

"""

        if article.image:

            result = self.publish_photo(

                article.image,

                caption

            )

        else:

            result = self.publish_text(

                caption,

                article.link

            )

        if not result:

            return False

        post_id = result.get("post_id")

        if not post_id:

            post_id = result.get("id")

        if post_id:

            self.comment(

                post_id,

                f"📰 Sumber:\n{article.link}"

            )

        logger.info(

            "Posted %s",

            article.title

        )

        return True

