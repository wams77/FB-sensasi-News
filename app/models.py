from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class NewsArticle:
    title: str
    summary: str
    link: str
    image: str | None
    source: str
    category: str
    published: datetime | None
    headline: str = ""
    article: str = ""
    hashtags: list[str] = field(default_factory=list)
    emoji: str = "🔥"
    score: int = 0
    priority: int = 3
    thumbnail: str | None = None
    facebook_post_id: str | None = None
    posted: bool = False
