from __future__ import annotations

from email.utils import parsedate_to_datetime
from datetime import datetime
from typing import Optional
import html
import re
import time

import feedparser
import requests
from bs4 import BeautifulSoup

from config import (
    RSS_FEEDS,
    GOOGLE_KEYWORDS,
    USER_AGENT,
    REQUEST_TIMEOUT,
    MAX_RETRY,
)

from models import NewsArticle
from logger import logger


HEADERS = {
    "User-Agent": USER_AGENT
}


class NewsCollector:

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update(HEADERS)

    # -----------------------------
    # TEXT
    # -----------------------------

    def clean_html(self, text: str) -> str:

        if not text:
            return ""

        text = html.unescape(text)

        soup = BeautifulSoup(
            text,
            "html.parser"
        )

        text = soup.get_text(
            " ",
            strip=True
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # -----------------------------
    # DATE
    # -----------------------------

    def parse_date(
        self,
        value: str
    ) -> Optional[datetime]:

        if not value:
            return None

        try:
            return parsedate_to_datetime(
                value
            )

        except Exception:

            return None

    # -----------------------------
    # IMAGE
    # -----------------------------

    def extract_image(
        self,
        entry
    ) -> Optional[str]:

        if hasattr(entry, "media_content"):

            media = entry.media_content

            if media:

                return media[0].get("url")

        if hasattr(entry, "media_thumbnail"):

            media = entry.media_thumbnail

            if media:

                return media[0].get("url")

        summary = entry.get(
            "summary",
            ""
        )

        if summary:

            soup = BeautifulSoup(
                summary,
                "html.parser"
            )

            img = soup.find("img")

            if img:

                return img.get("src")

        return None

    # -----------------------------
    # URL
    # -----------------------------

    def canonical_url(
        self,
        url: str
    ) -> str:

        if not url:

            return ""

        url = url.split("?")[0]

        url = url.rstrip("/")

        return url

    # -----------------------------
    # HTTP
    # -----------------------------

    def fetch_feed(
        self,
        url: str
    ):

        for retry in range(MAX_RETRY):

            try:

                logger.info(
                    "Fetch %s",
                    url
                )

                return feedparser.parse(url)

            except Exception as e:

                logger.exception(e)

                time.sleep(2)

        return None

    # -----------------------------
    # GOOGLE NEWS
    # -----------------------------

    def google_news_url(
        self,
        keyword: str
    ) -> str:

        keyword = keyword.replace(
            " ",
            "+"
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
                )

            })

        return feeds

    # -----------------------------
    # NORMALIZE
    # -----------------------------

    def normalize(
        self,
        entry,
        source: dict,
    ) -> NewsArticle:

        return NewsArticle(

            title=entry.get(
                "title",
                ""
            ).strip(),

            summary=self.clean_html(

                entry.get(
                    "summary",
                    ""
                )

            ),

            link=self.canonical_url(

                entry.get(
                    "link",
                    ""
                )

            ),

            image=self.extract_image(
                entry
            ),

            source=source["name"],

            category=source["category"],

            published=self.parse_date(

                entry.get(
                    "published",
                    ""
                )

            )

        )

    # -----------------------------
    # VALIDATION
    # -----------------------------

    def is_valid(
        self,
        article: NewsArticle,
    ) -> bool:

        if not article.title:
            return False

        if len(article.title) < 10:
            return False

        if not article.link:
            return False

        if article.title.lower().startswith(
            "photo"
        ):
            return False

        if article.title.lower().startswith(
            "gallery"
        ):
            return False

        return True

    # -----------------------------
    # DUPLICATE
    # -----------------------------

    def remove_duplicate_url(
        self,
        articles,
    ):

        result = []

        urls = set()

        for article in articles:

            if article.link in urls:
                continue

            urls.add(
                article.link
            )

            result.append(
                article
            )

        return result

    # -----------------------------
    # SORT
    # -----------------------------

    def sort_articles(
        self,
        articles,
    ):

        return sorted(

            articles,

            key=lambda x:
                x.published
                or datetime.min,

            reverse=True

        )

    # -----------------------------
    # LOAD ONE FEED
    # -----------------------------

    def load_feed(
        self,
        source,
    ):

        logger.info(

            "Feed : %s",

            source["name"]

        )

        feed = self.fetch_feed(

            source["url"]

        )

        if not feed:

            return []

        articles = []

        for entry in feed.entries:

            article = self.normalize(

                entry,

                source

            )

            if not self.is_valid(
                article
            ):
                continue

            articles.append(
                article
            )

        logger.info(

            "%s : %s",

            source["name"],

            len(articles)

        )

        return articles

    # -----------------------------
    # MAIN COLLECTOR
    # -----------------------------

    def collect(self):

        articles = []

        feeds = []

        feeds.extend(RSS_FEEDS)

        feeds.extend(self.google_feeds())

        logger.info(
            "Total Feeds : %s",
            len(feeds)
        )

        for source in feeds:

            try:

                items = self.load_feed(
                    source
                )

                if items:

                    articles.extend(
                        items
                    )

            except Exception as e:

                logger.exception(e)

        before = len(articles)

        articles = self.remove_duplicate_url(
            articles
        )

        after = len(articles)

        logger.info(
            "Duplicate Removed : %s",
            before - after
        )

        articles = self.sort_articles(
            articles
        )

        logger.info(
            "Collected : %s Articles",
            len(articles)
        )

        return articles

# -----------------------------
# DEBUG
# -----------------------------

if __name__ == "__main__":

    collector = NewsCollector()

    articles = collector.collect()

    print()

    print("=" * 60)

    print("TOTAL :", len(articles))

    print("=" * 60)

    for article in articles[:10]:

        print()

        print(article.title)

        print(article.source)

        print(article.link)
