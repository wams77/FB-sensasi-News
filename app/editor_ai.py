from __future__ import annotations

import json
import re

from groq import Groq

from config import GROQ_API_KEY
from logger import logger
from models import NewsArticle


MODEL = "llama-3.3-70b-versatile"


SYSTEM_PROMPT = """
Kamu adalah jurnalis senior media online Indonesia dan analis profesional.

Tugasmu adalah menulis ulang SATU berita menjadi artikel Facebook.

ATURAN:
- Jangan mengubah fakta.
- Jangan menambah fakta di luar konteks.
- Jangan membuat berita palsu.
- Bahasa Indonesia.
- Gaya media online profesional.
- Headline maksimal 14 kata.
- Artikel 180-250 kata.
- Awali dengan paragraf pembuka yang menarik.
- Isi terdiri dari 2-3 paragraf.
- WAJIB membuat 1 paragraf "Analisis Profesional" yang tajam HANYA berdasarkan fakta berita tersebut (misal: analisis taktik/klasemen jika olahraga, atau dampak karier/sosial jika hiburan).
- Tutup artikel dengan pertanyaan agar pembaca berdiskusi.
- Jangan menyebut nama AI.
- Maksimal 5 hashtag.
- JANGAN gunakan tanda kutip ganda (") di dalam nilai teks JSON untuk menghindari error parsing. Gunakan kutip tunggal (') jika diperlukan.

Balas HARUS JSON VALID.

Schema:
{
    "viral_score":95,
    "priority":1,
    "headline":"",
    "article":"",
    "analysis":"",
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
        summary = article.summary[:800] if article.summary else ""
        return f"""
TITLE
{article.title}

SUMMARY
{summary}

SOURCE
{article.source}

Tulis ulang menjadi artikel Facebook yang menarik dan tambahkan analisis profesional tanpa mengubah fakta asli.
"""

    def analyze(
        self,
        article: NewsArticle,
    ) -> dict:
        response = self.client.chat.completions.create(
            model=MODEL,
            temperature=0.3,
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
        content = re.sub(r"^```json\s*", "", content, flags=re.IGNORECASE)
        content = re.sub(r"\s*```$", "", content)
        
        return json.loads(content.strip())

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
            # MENANGKAP HASIL ANALISIS DARI JSON AI
            article.analysis = result.get(
                "analysis",
                ""
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
            logger.exception("AI Editor Error: %s", e)
            article.score = 0
            article.priority = 4
            article.headline = article.title
            article.article = article.summary
            article.analysis = ""
            article.hashtags = []
            article.emoji = ""
            return article
