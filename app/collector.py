from __future__ import annotations

import html
import re
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Optional

import feedparser
import requests
from bs4 import BeautifulSoup

from config import (
    RSS_FEEDS,
    GOOGLE_KEYWORDS,
    USER_AGENT,
    RSS_LIMIT,
    GOOGLE_LIMIT,
    MAX_RETRY,
    REQUEST_TIMEOUT,
)

from logger import logger
from models import NewsArticle


HEADERS = {

    "User-Agent": USER_AGENT

}


class NewsCollector:

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update(

            HEADERS

        )

    def google_news_url(

        self,

        keyword: str,

    ) -> str:

        keyword = keyword.replace(

            " ",

            "+",

        )

        return (

            "https://news.google.com/rss/search?"

            f"q={keyword}"

            "&hl=en-US"

            "&gl=US"

            "&ceid=US:en"

        )

    def google_feeds(self):

        feeds = []

        for keyword in GOOGLE_KEYWORDS:

            feeds.append({

                "name": f"Google News ({keyword})",

                "category": "google",

                "url": self.google_news_url(

                    keyword

                ),

                "limit": GOOGLE_LIMIT,

            })

        return feeds

    def clean_html(

        self,

        text: str,

    ) -> str:

        if not text:

            return ""

        text = html.unescape(

            text

        )

        soup = BeautifulSoup(

            text,

            "html.parser",

        )

        text = soup.get_text(

            " ",

            strip=True,

        )

        text = re.sub(

            r"\s+",

            " ",

            text,

        )

        return text.strip()

    def parse_date(

        self,

        value: str,

    ) -> Optional[datetime]:

        if not value:

            return None

        try:

            return parsedate_to_datetime(

                value

            )

        except Exception:

            return None

    def extract_image(

        self,

        entry,

    ) -> Optional[str]:

        if hasattr(

            entry,

            "media_content",

        ):

            media = entry.media_content

            if media:

                return media[0].get(

                    "url"

                )

        if hasattr(

            entry,

            "media_thumbnail",

        ):

            media = entry.media_thumbnail

            if media:

                return media[0].get(

                    "url"

                )

        summary = entry.get(

            "summary",

            "",

        )

        if summary:

            soup = BeautifulSoup(

                summary,

                "html.parser",

            )

            img = soup.find(

                "img"

            )

            if img:

                return img.get(

                    "src"

                )

        return None

    def fetch_feed(

        self,

        url: str,

    ):

        for _ in range(

            MAX_RETRY

        ):

            try:

                logger.info(

                    "Fetch %s",

                    url,

                )

                return feedparser.parse(

                    url

                )

            except Exception as e:

                logger.exception(

                    e

                )

        return None

    def normalize(

        self,

        entry,

        source,

    ) -> NewsArticle:

        return NewsArticle(

            title=entry.get(

                "title",

                "",

            ).strip(),

            summary=self.clean_html(

                entry.get(

                    "summary",

                    "",

                )

            ),

            link=entry.get(

                "link",

                "",

            ),

            image=self.extract_image(

                entry

            ),

            source=source["name"],

            category=source["category"],

            published=self.parse_date(

                entry.get(

                    "published",

                    "",

                )

            ),

        )

    def collect_feed(

        self,

        source,

    ):

        articles = []

        feed = self.fetch_feed(

            source["url"]

        )

        if not feed:

            return articles

        limit = source.get(

            "limit",

            RSS_LIMIT,

        )

        logger.info(

            "%s : %s",

            source["name"],

            len(feed.entries),

        )

        for entry in feed.entries[:limit]:

            try:

                articles.append(

                    self.normalize(

                        entry,

                        source,

                    )

                )

            except Exception as e:

                logger.exception(

                    e

                )

        return articles

    def collect(self):

        articles = []

        feeds = []

        for feed in RSS_FEEDS:

            feed = dict(feed)

            feed["limit"] = RSS_LIMIT

            feeds.append(feed)

        feeds.extend(

            self.google_feeds()

        )

        logger.info(

            "Total Feeds : %s",

            len(feeds),

        )

        for feed in feeds:

            logger.info(

                "Feed : %s",

                feed["name"],

            )

            articles.extend(

                self.collect_feed(

                    feed

                )

            )

        logger.info(

            "Collected : %s Articles",

            len(articles),

        )

        articles.sort(

            key=lambda x: (

                x.published

                or datetime.min

            ),

            reverse=True,

        )

        return articles


if __name__ == "__main__":

    collector = NewsCollector()

    articles = collector.collect()

    print()

    print(

        "TOTAL:",

        len(articles)

    )

    print()

    for article in articles[:10]:

        print(

            article.published,

            article.title,

        )
