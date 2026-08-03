from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass(slots=True)
class NewsArticle:

    # Original Data

    title: str
    summary: str
    link: str

    source: str

    category: str

    published: Optional[datetime] = None

    image: Optional[str] = None

    # AI Result

    headline: str = ""

    caption: str = ""

    hashtags: List[str] = field(default_factory=list)

    emoji: str = ""

    score: int = 0

    priority: int = 3

    language: str = "en"

    # Metadata

    collected_at: datetime = field(
        default_factory=datetime.utcnow
    )

    posted: bool = False

    facebook_post_id: Optional[str] = None

    def short_dict(self):

        return {

            "title": self.title,

            "headline": self.headline,

            "score": self.score,

            "priority": self.priority,

            "source": self.source,

            "category": self.category,

            "link": self.link,

        }

    def to_post(self):

        hashtags = " ".join(self.hashtags)

        text = f"""{self.headline}

{self.caption}

{hashtags}
"""

        return text.strip()

    @property
    def is_breaking(self):

        return self.priority == 1

    @property
    def is_viral(self):

        return self.score >= 90
