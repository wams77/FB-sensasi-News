from __future__ import annotations

import json
from groq import Groq

from config import GROQ_API_KEY
from logger import logger
from models import NewsArticle

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """
Kamu adalah editor media online Indonesia.

Tugasmu mengubah SATU berita menjadi posting Facebook yang menarik.

ATURAN:

- Jangan mengubah fakta.
- Jangan membuat berita palsu.
- Bahasa Indonesia.
- Headline maksimal 14 kata.
- Caption maksimal 120 kata.
- Tambahkan CTA.
- Maksimal 5 hashtag.
- Emoji secukupnya.

Balas HARUS berupa JSON VALID.

Schema:

{
    "viral_score":95,
    "priority":1,
    "headline":"",
    "caption":"",
    "hashtags":["#Football","#Messi"],
    "category":"football",
    "emoji":"🔥"
}

priority:

1 = Breaking
2 = Viral
3 = Normal
4 = Skip

category:

football
transfer
kpop
drama
entertainment
other
"""


class AIEditor:

    def __init__(self):

        self.client = Groq(
            api_key=GROQ_API_KEY
        )

    def build_prompt(
        self,
        article: NewsArticle,
    ) -> str:

        return f"""
TITLE
{article.title}

SUMMARY
{article.summary}

SOURCE
{article.source}
"""

    def analyze(
        self,
        article: NewsArticle,
    ) -> dict:

        response = self.client.chat.completions.create(

            model=MODEL,

            temperature=0.5,

            response_format={
                "type": "json_object"
            },

            messages=[

                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },

                {
                    "role": "user",
                    "content": self.build_prompt(article)
                }

            ]

        )

        content = response.choices[0].message.content

        return json.loads(content)

    def process(
        self,
        article: NewsArticle,
    ) -> NewsArticle:

        try:

            result = self.analyze(
                article
            )

            article.score = int(
                result.get(
                    "viral_score",
                    0
                )
            )

            article.priority = int(
                result.get(
                    "priority",
                    3
                )
            )

            article.headline = result.get(
                "headline",
                article.title
            )

            article.caption = result.get(
                "caption",
                article.summary
            )

            article.hashtags = result.get(
                "hashtags",
                []
            )

            article.category = result.get(
                "category",
                article.category
            )

            article.emoji = result.get(
                "emoji",
                ""
            )

            return article

        except Exception as e:

            logger.exception(e)

            article.score = 0
            article.priority = 4
            article.headline = article.title
            article.caption = article.summary
            article.hashtags = []
            article.emoji = ""

            return article
