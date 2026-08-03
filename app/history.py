from __future__ import annotations

import json
from pathlib import Path

from config import DATA_DIR
from logger import logger


class History:

    def __init__(self):

        self.file = DATA_DIR / "history.json"

        self.items = set()

        self.load()

    def load(self):

        if not self.file.exists():

            self.save()

            return

        try:

            with open(

                self.file,

                "r",

                encoding="utf-8",

            ) as f:

                data = json.load(f)

            self.items = set(data)

            logger.info(

                "History Loaded : %s",

                len(self.items),

            )

        except Exception as e:

            logger.exception(e)

            self.items = set()

    def save(self):

        with open(

            self.file,

            "w",

            encoding="utf-8",

        ) as f:

            json.dump(

                sorted(self.items),

                f,

                indent=4,

                ensure_ascii=False,

            )
    def exists(

        self,

        url: str,

    ) -> bool:

        return url in self.items

    def add(

        self,

        url: str,

    ):

        if not url:

            return

        self.items.add(

            url

        )

        self.save()

        logger.info(

            "History Added : %s",

            url,

        )

    def remove(

        self,

        url: str,

    ):

        if url in self.items:

            self.items.remove(

                url

            )

            self.save()

    def clear(

        self,

    ):

        self.items = set()

        self.save()

        logger.info(

            "History Cleared"

        )


if __name__ == "__main__":

    history = History()

    history.add(

        "https://example.com/article"

    )

    print(

        history.exists(

            "https://example.com/article"

        )

    )

    history.remove(

        "https://example.com/article"

    )

    print(

        history.exists(

            "https://example.com/article"

        )

    )
