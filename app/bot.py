from __future__ import annotations

from collector import NewsCollector
from editor_ai import AIEditor
from facebook import FacebookPublisher
from history import History

from filters.duplicate import DuplicateFilter
from filters.quality import QualityFilter
from filters.trending import TrendingFilter

from config import (
    MAX_POST,
    MIN_VIRAL_SCORE,
)
from logger import logger


class NewsBot:

    def __init__(self):
        self.collector = NewsCollector()
        self.duplicate = DuplicateFilter()
        self.quality = QualityFilter()
        self.trending = TrendingFilter()
        self.editor = AIEditor()
        self.facebook = FacebookPublisher()
        self.history = History()

    def preprocess(self):
        articles = self.collector.collect()
        logger.info(
            "Collected : %s",
            len(articles)
        )

        articles = self.duplicate.process(
            articles
        )
        logger.info(
            "After Duplicate : %s",
            len(articles)
        )

        articles = self.quality.process(
            articles
        )
        logger.info(
            "After Quality : %s",
            len(articles)
        )

        articles = self.trending.process(
            articles,
            limit=20
        )
        logger.info(
            "After Trending : %s",
            len(articles)
        )

        return articles

    def should_skip(
        self,
        article,
    ) -> bool:
        if self.history.exists(
            article.link
        ):
            logger.info(
                "History Skip : %s",
                article.title,
            )
            return True

        if article.priority == 4:
            logger.info(
                "Priority Skip : %s",
                article.title,
            )
            return True

        if article.score < MIN_VIRAL_SCORE:
            logger.info(
                "Score Skip : %s (%s)",
                article.title,
                article.score,
            )
            return True

        return False

    def process_article(
        self,
        article,
    ) -> bool:
        article = self.editor.process(
            article
        )

        if self.should_skip(
            article
        ):
            return False

        post_id = self.facebook.publish(
            article
        )

        if not post_id:
            logger.error(
                "Publish Failed : %s",
                article.title,
            )
            return False

        self.history.add(
            article.link
        )
        logger.info(
            "Posted : %s",
            article.title,
        )
        return True

    def run(self):
        logger.info(
            "=" * 60
        )
        logger.info(
            "Sensasi News Bot Started"
        )

        articles = self.preprocess()
        posted = 0

        for article in articles:
            if posted >= MAX_POST:
                break
            try:
                if self.process_article(
                    article
                ):
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
