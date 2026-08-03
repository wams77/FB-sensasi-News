from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class NewsArticle:

    # Source

    title: str

    summary: str

    link: str

    image: Optional[str]

    source: str

    category: str

    published: Optional[datetime]

    # AI

    headline: str = ""

    article: str = ""

    hashtags: list[str] = field(default_factory=list)

    emoji: str = ""

    score: int = 0

    priority: int = 3

    # Facebook

    posted: bool = False

    facebook_post_id: str = ""

    # Internal

    thumbnail: str = ""

    language: str = ""

    duplicate_score: int = 0

    created_at: datetime = field(
        default_factory=datetime.utcnow
    )

    def to_dict(self):

        return {

            "title": self.title,

            "summary": self.summary,

            "link": self.link,

            "image": self.image,

            "source": self.source,

            "category": self.category,

            "published": (
                self.published.isoformat()
                if self.published
                else None
            ),

            "headline": self.headline,

            "article": self.article,

            "hashtags": self.hashtags,

            "emoji": self.emoji,

            "score": self.score,

            "priority": self.priority,

            "posted": self.posted,

            "facebook_post_id": self.facebook_post_id,

            "thumbnail": self.thumbnail,

            "language": self.language,

            "duplicate_score": self.duplicate_score,

            "created_at": self.created_at.isoformat(),

        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ):

        published = None

        if data.get("published"):

            published = datetime.fromisoformat(
                data["published"]
            )

        obj = cls(

            title=data["title"],

            summary=data["summary"],

            link=data["link"],

            image=data.get("image"),

            source=data["source"],

            category=data["category"],

            published=published,

        )

        obj.headline = data.get(
            "headline",
            ""
        )

        obj.article = data.get(
            "article",
            ""
        )

        obj.hashtags = data.get(
            "hashtags",
            []
        )

        obj.emoji = data.get(
            "emoji",
            ""
        )

        obj.score = data.get(
            "score",
            0
        )

        obj.priority = data.get(
            "priority",
            3
        )

        obj.posted = data.get(
            "posted",
            False
        )

        obj.facebook_post_id = data.get(
            "facebook_post_id",
            ""
        )

        obj.thumbnail = data.get(
            "thumbnail",
            ""
        )

        obj.language = data.get(
            "language",
            ""
        )

        obj.duplicate_score = data.get(
            "duplicate_score",
            0
        )

        return obj
