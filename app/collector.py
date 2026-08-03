from __future__ import annotations

import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
import time

from config import RSS_FEEDS, RSS_LIMIT, USER_AGENT
from logger import logger
from models import NewsArticle


class NewsCollector:

    def __init__(self):
        self.feeds = RSS_FEEDS

    def extract_image(self, entry) -> str | None:
        """Mengekstrak URL gambar asli dari berbagai format tag RSS feed."""
        try:
            # 1. Cek media:content
            if hasattr(entry, "media_content") and entry.media_content:
                for media in entry.media_content:
                    url = media.get("url")
                    if url and any(ext in url.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                        return url

            # 2. Cek media:thumbnail
            if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
                for thumb in entry.media_thumbnail:
                    url = thumb.get("url")
                    if url:
                        return url

            # 3. Cek enclosures (lampiran file/gambar)
            if hasattr(entry, "enclosures") and entry.enclosures:
                for enc in entry.enclosures:
                    if "image" in enc.get("type", ""):
                        return enc.get("href")

            # 4. Cari tag <img> di dalam content atau summary/description
            content_html = ""
            if hasattr(entry, "content") and entry.content:
                content_html = entry.content[0].get("value", "")
            elif hasattr(entry, "summary"):
                content_html = entry.summary
            elif hasattr(entry, "description"):
                content_html = entry.description

            if content_html:
                soup = BeautifulSoup(content_html, "html.parser")
                img_tag = soup.find("img")
                if img_tag and img_tag.get("src"):
                    return img_tag.get("src")

        except Exception as e:
            logger.warning("Gagal mengekstrak gambar dari entry RSS: %s", e)

        return None

    def fetch_feed(self, feed_info: dict) -> list[NewsArticle]:
        articles = []
        name = feed_info["name"]
        category = feed_info["category"]
        url = feed_info["url"]

        try:
            logger.info("Mengambil RSS dari: %s (%s)", name, url)
            
            # Menggunakan feedparser dengan parsing standar
            parsed = feedparser.parse(url)

            if not parsed.entries:
                logger.warning("Tidak ada entri ditemukan pada feed: %s", name)
                return articles

            # Batasi jumlah artikel per feed sesuai konfigurasi
            entries = parsed.entries[:RSS_LIMIT]

            for entry in entries:
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                
                if not title or not link:
                    continue

                # Ambil ringkasan/deskripsi
                summary = entry.get("summary", "") or entry.get("description", "")
                if summary:
                    soup = BeautifulSoup(summary, "html.parser")
                    summary = soup.get_text().strip()

                # Ekstrak gambar asli
                image_url = self.extract_image(entry)

                article = NewsArticle(
                    title=title,
                    url=link,
                    summary=summary,
                    category=category,
                    source=name,
                    image=image_url,
                )
                articles.append(article)

        except Exception as e:
            logger.error("Error saat mengambil feed %s: %s", name, e)

        logger.info("Berhasil mengumpulkan %d artikel dari %s", len(articles), name)
        return articles

    def collect_all(self) -> list[NewsArticle]:
        all_articles = []
        
        for feed in self.feeds:
            articles = self.fetch_feed(feed)
            all_articles.extend(articles)
            time.sleep(1) # Jeda singkat antar feed untuk mencegah rate-limit

        logger.info("Total keseluruhan artikel terkumpul: %d", len(all_articles))
        return all_articles
