"""
collector.py
Version : 1.0
Part    : 1

News Collector

- Multi RSS
- Google News RSS
- Retry
- Timeout
- HTML Cleaner
- Image Extractor
- Published Date
- Language Filter
"""

from __future__ import annotations

import html
import logging
import re
import time
from dataclasses import dataclass
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import List, Optional

import feedparser
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/138 Safari/537.36"
    )
}

TIMEOUT = 30

MAX_RETRY = 3


RSS_SOURCES = [

    # FOOTBALL

    {
        "name": "BBC Football",
        "category": "football",
        "url": "https://feeds.bbci.co.uk/sport/football/rss.xml"
    },

    {
        "name": "ESPN Soccer",
        "category": "football",
        "url": "https://www.espn.com/espn/rss/soccer/news"
    },

    {
        "name": "Goal",
        "category": "football",
        "url": "https://www.goal.com/feeds/en/news"
    },

    {
        "name": "FIFA",
        "category": "football",
        "url": "https://inside.fifa.com/rss"
    },

    {
        "name": "UEFA",
        "category": "football",
        "url": "https://www.uefa.com/rssfeed/news/rss.xml"
    },

    # KOREA

    {
        "name": "Soompi",
        "category": "kpop",
        "url": "https://www.soompi.com/feed"
    },

    {
        "name": "Korea Herald",
        "category": "korea",
        "url": "https://www.koreaherald.com/rss"
    },

    {
        "name": "Yonhap",

        @dataclass
class NewsArticle:

    title: str

    summary: str

    link: str

    image: Optional[str]

    source: str

    category: str

    published: Optional[datetime]
        "category": "korea",
        "url": "https://en.yna.co.kr/RSS/news.xml"
    },

]

    class NewsCollector:

    def __init__(self):

        self.session = requests.Session()

        self.session.headers.update(HEADERS)

    def clean_html(self, text: str) -> str:

        if not text:
            return ""

        text = html.unescape(text)

        soup = BeautifulSoup(text, "html.parser")

        text = soup.get_text(" ", strip=True)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    def parse_date(self, value):

        if not value:

            return None

        try:

            return parsedate_to_datetime(value)

        except Exception:

            return None

    def extract_image(self, entry):

        if "media_content" in entry:

            media = entry.media_content

            if media:

                return media[0].get("url")

        if "media_thumbnail" in entry:

            media = entry.media_thumbnail

            if media:

                return media[0].get("url")

        if "summary" in entry:

            soup = BeautifulSoup(entry.summary, "html.parser")

            img = soup.find("img")

            if img:

                return img.get("src")

        return None

    def fetch_feed(self, url):

        for attempt in range(MAX_RETRY):

            try:

                logger.info("Fetch %s", url)

                return feedparser.parse(url)

            except Exception as e:

                logger.warning(e)

                time.sleep(2)

        return None

    def normalize(self, entry, source):

        title = entry.get("title", "").strip()

        summary = self.clean_html(

            entry.get("summary", "")

        )

        return NewsArticle(

            title=title,

            summary=summary,

            link=entry.get("link", ""),

            image=self.extract_image(entry),

            source=source["name"],

            category=source["category"],

            published=self.parse_date(

                entry.get("published", "")

            )

        )

    def google_news_url(self, keyword: str) -> str:
        """
        Google News RSS

        contoh:
        https://news.google.com/rss/search?q=messi
        """

        keyword = keyword.strip().replace(" ", "+")

        return (
            "https://news.google.com/rss/search?"
            f"q={keyword}&hl=en-US&gl=US&ceid=US:en"
        )

    def google_sources(self):

        keywords = [

            # Football

            "Messi",
            "Ronaldo",
            "Haaland",
            "Mbappe",
            "Liverpool",
            "Manchester United",
            "Barcelona",
            "Real Madrid",
            "Arsenal",
            "Chelsea",
            "Tottenham",
            "Premier League",
            "Champions League",

            # Korea

            "BLACKPINK",
            "BTS",
            "IU",
            "aespa",
            "NewJeans",
            "Korean Drama",
            "Netflix Korea",
            "KPop"

        ]

        feeds = []

        for keyword in keywords:

            feeds.append({

                "name": f"Google News ({keyword})",

                "category": "google",

                "url": self.google_news_url(keyword)

            })

        return feeds

    def is_valid(self, article: NewsArticle):

        if len(article.title) < 10:
            return False

        if len(article.link) < 10:
            return False

        if article.title.lower().startswith("photo"):
            return False

        return True

    def canonical_url(self, url: str):

        if not url:
            return ""

        url = url.split("?")[0]

        url = url.rstrip("/")

        return url

    def remove_duplicate_url(self, articles):

        urls = set()

        result = []

        for article in articles:

            url = self.canonical_url(article.link)

            if url in urls:
                continue

            urls.add(url)

            article.link = url

            result.append(article)

        return result

    def sort_articles(self, articles):

        return sorted(

            articles,

            key=lambda x: x.published or datetime.min,

            reverse=True

        )

    def collect(self):

        articles = []

        feeds = RSS_SOURCES + self.google_sources()

        logger.info(

            "Collector : %s feeds",

            len(feeds)

        )

        for source in feeds:

            feed = self.fetch_feed(

                source["url"]

            )

            if not feed:

                continue

            for entry in feed.entries:

                article = self.normalize(

                    entry,

                    source

                )

                if not self.is_valid(article):

                    continue

                articles.append(article)

        articles = self.remove_duplicate_url(

            articles

        )

        articles = self.sort_articles(

            articles

        )

        logger.info(

            "Collector : %s articles",

            len(articles)

        )

        return articles
