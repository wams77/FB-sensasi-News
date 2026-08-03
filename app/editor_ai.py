import json
from groq import Groq
from config import GROQ_API_KEY

MODEL = "llama-3.3-70b-versatile"

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
Kamu adalah editor berita profesional.

Tugasmu membaca SATU berita lalu mengembalikan JSON VALID.

JANGAN gunakan markdown.
JANGAN gunakan ```.

Schema:

{
    "viral_score":95,
    "headline":"...",
    "caption":"...",
    "hashtags":["#Football","#Messi"],
    "category":"football",
    "emoji":"🔥",
    "priority":1
}

priority:

1 = Breaking
2 = Viral
3 = Normal
4 = Skip

Aturan:

- Jangan mengubah fakta.
- Jangan membuat berita palsu.
- Judul maksimal 14 kata.
- Caption maksimal 120 kata.
- Maksimal 5 hashtag.
- Bahasa Indonesia.

Kategori hanya:

football
transfer
kpop
drama
entertainment
other
"""


class AIEditor:

    def __init__(self):
        self.client = client

    def build_prompt(self, article):

        return f"""
TITLE:
{article.title}

SUMMARY:
{article.summary}

SOURCE:
{article.source}
"""

    def analyze(self, article):

        response = self.client.chat.completions.create(

            model=MODEL,

            temperature=0.6,

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

    def process(self, article):

        result = self.analyze(article)

        article.score = result.get("viral_score", 0)

        article.headline = result.get("headline", article.title)

        article.caption = result.get("caption", article.summary)

        article.hashtags = result.get("hashtags", [])

        article.category = result.get("category", "other")

        article.emoji = result.get("emoji", "")

        article.priority = result.get("priority", 3)

        return article
