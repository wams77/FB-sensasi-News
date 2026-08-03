from __future__ import annotations

import time

import requests

from config import (
    FACEBOOK_ACCESS_TOKEN,
    REQUEST_TIMEOUT,
    MAX_RETRY,
)

from logger import logger


GRAPH_URL = "https://graph.facebook.com/v23.0"


class FacebookComment:

    def __init__(self):

        self.token = FACEBOOK_ACCESS_TOKEN

    def comment(

        self,

        post_id: str,

        message: str,

    ) -> bool:

        if not post_id:

            return False

        url = f"{GRAPH_URL}/{post_id}/comments"

        payload = {

            "message": message,

            "access_token": self.token,

        }

        for _ in range(MAX_RETRY):

            try:

                response = requests.post(

                    url,

                    data=payload,

                    timeout=REQUEST_TIMEOUT,

                )

                logger.info(

                    response.text

                )

                if response.ok:

                    logger.info(

                        "Comment Success"

                    )

                    return True

            except Exception as e:

                logger.exception(e)

            time.sleep(2)

        logger.error(

            "Comment Failed"

        )

        return False

  if __name__ == "__main__":

    POST_ID = "YOUR_POST_ID"

    message = """
Sumber:
BBC Sport

https://www.bbc.com/sport

Artikel ini dirangkum dan ditulis ulang oleh Gosip.ID berdasarkan sumber berita di atas.
"""

    FacebookComment().comment(

        POST_ID,

        message,

    )
