from __future__ import annotations

import json

from groq import Groq

from config import GROQ_API_KEY

from logger import logger

from models import NewsArticle


MODEL = "llama-3.3-70b-versatile"


SYSTEM_PROMPT = """
Kamu adalah jurnalis senior media online Indonesia.

Tugasmu adalah menulis ulang SATU berita menjadi artikel Facebook.

ATURAN:

- Jangan mengubah fakta.
- Jangan menambah fakta.
- Jangan membuat berita palsu.
- Bahasa Indonesia.
- Gaya media online profesional.
- Headline maksimal 14 kata.
- Artikel 180-250 kata.
- Awali dengan paragraf pembuka yang menarik.
- Isi terdiri dari 2-3 paragraf.
- Tutup dengan pertanyaan agar pembaca berdiskusi.
- Jangan menyebut nama AI.
- Maksimal 5 hashtag.

Balas HARUS JSON VALID.

Schema:

{
    "viral_score":95,
    "priority":1,
    "headline":"",
    "article":"",
    "hashtags":[
        "#Football"
    ],
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

LINK

{article.link}

Tulis ulang menjadi artikel Facebook yang menarik tanpa mengubah fakta.
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

                    "content": self.build_prompt(

                        article

                    )

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

            article.article = result.get(

                "article",

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

            article.article = article.summary

            article.hashtags = []

            article.emoji = ""

            return article


if __name__ == "__main__":

    sample = NewsArticle(

        title="Arsenal resmi mendapatkan pemain baru.",

        summary="Arsenal dikabarkan menyelesaikan proses transfer setelah negosiasi selama beberapa pekan.",

        link="https://example.com",

        image=None,

        source="BBC Football",

        category="football",

        published=None,

    )

    editor = AIEditor()

    result = editor.process(sample)

    print()

    print("=" * 60)

    print(result.headline)

    print()

    print(result.article)

    print()

    print(result.hashtags)

    print()

    print(result.score)
