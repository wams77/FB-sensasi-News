from __future__ import annotations

from collector import NewsCollector
from editor_ai import AIEditor
from facebook import FacebookPublisher
from history import History

from config import (
    MAX_POST,
    MIN_VIRAL_SCORE,
)

from logger import logger


class NewsBot:

    def __init__(self):

        self.collector = NewsCollector()

        self.editor = AIEditor()

        self.facebook = FacebookPublisher()

        self.history = History()

    def should_skip(self, article):

        if self.history.exists(article.link):

            logger.info(
                "Skip History : %s",
                article.title
            )

            return True

        if article.priority == 4:

            logger.info(
                "Skip Priority : %s",
                article.title
            )

            return True

        if article.score < MIN_VIRAL_SCORE:

            logger.info(
                "Skip Score : %s (%s)",
                article.title,
                article.score
            )

            return True

        return False

    def process_article(self, article):

        article = self.editor.process(
            article
        )

        if self.should_skip(article):

            return False

        post_id = self.facebook.publish(
            article
        )

        if not post_id:

            logger.error(
                "Facebook Failed : %s",
                article.title
            )

            return False

        self.history.add(
            article.link
        )

        logger.info(
            "Posted : %s",
            article.title
        )

        return True

    def run(self):

        logger.info(
            "=" * 60
        )

        logger.info(
            "Sensasi News Bot Started"
        )

        articles = self.collector.collect()

        logger.info(
            "Articles : %s",
            len(articles)
        )

        posted = 0

        for article in articles:

            if posted >= MAX_POST:
                break

            try:

                success = self.process_article(
                    article
                )

                if success:

                    posted += 1

            except Exception as e:

                logger.exception(e)

        logger.info(
            "Total Posted : %s",
            posted
        )

        logger.info(
            "=" * 60
        )


if __name__ == "__main__":

    NewsBot().run()
