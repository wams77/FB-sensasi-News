import feedparser
from bs4 import BeautifulSoup
from config import RSS_FEEDS


class NewsCollector:

    def __init__(self):

        self.news = []

    def clean_html(self, text):

        soup = BeautifulSoup(text, "html.parser")

        return soup.get_text(" ", strip=True)

    def collect(self):

        articles = []

        for url in RSS_FEEDS:

            try:

                feed = feedparser.parse(url)

                for item in feed.entries:

                    summary = item.get("summary", "")

                    summary = self.clean_html(summary)

                    articles.append({

                        "title": item.get("title", "").strip(),

                        "summary": summary,

                        "link": item.get("link", ""),

                        "source": feed.feed.get("title", "")

                    })

            except Exception as e:

                print(e)

        return articles
