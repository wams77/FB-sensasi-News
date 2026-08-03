from __future__ import annotations

from datetime import datetime, timedelta

from models import NewsArticle


class QualityFilter:

    def __init__(

        self,

        max_age_hours: int = 48,

    ):

        self.max_age = timedelta(

            hours=max_age_hours

        )

    def valid_title(

        self,

        article: NewsArticle,

    ) -> bool:

        return len(

            article.title.strip()

        ) >= 20

    def valid_summary(

        self,

        article: NewsArticle,

    ) -> bool:

        return len(

            article.summary.strip()

        ) >= 40

    def valid_image(

        self,

        article: NewsArticle,

    ) -> bool:

        return bool(article.image)

    def valid_date(

        self,

        article: NewsArticle,

    ) -> bool:

        if article.published is None:

            return True

        now = datetime.now(

            article.published.tzinfo

        )

        return (

            now - article.published

        ) <= self.max_age

    def keep(

        self,

        article: NewsArticle,

    ) -> bool:

        return (

            self.valid_title(article)

            and

            self.valid_summary(article)

            and

            self.valid_image(article)

            and

            self.valid_date(article)

        )

    def process(

        self,

        articles,

    ):

        return [

            article

            for article in articles

            if self.keep(article)

        ]
