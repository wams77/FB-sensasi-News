import json
from groq import Groq
from config import GROQ_API_KEY

MODEL = "llama-3.3-70b-versatile"

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
Kamu adalah editor berita profesional.

Tugasmu adalah membaca SATU berita.

Balas HARUS berupa JSON VALID.

Jangan gunakan markdown.

Jangan gunakan ```json

Schema:

{
"viral_score":0-100,
"headline":"",
"caption":"",
"hashtags":["#A","#B","#C"],
"category":"",
"emoji":""
}

Aturan:

headline maksimal 14 kata.

caption maksimal 120 kata.

Jangan mengubah fakta.

Jangan membuat berita palsu.

Hashtag maksimal 5.

Kategori hanya salah satu:

football

kpop

drama

entertainment

transfer

other
"""

class AIEditor:

    def __init__(self):

        self.client = clientclass AIEditor:

    def __init__(self):

        self.client = client

      def build_prompt(self, article):

        return f"""

TITLE

{article.title}

SUMMARY

{article.summary}

SOURCE

{article.source}

"""    def build_prompt(self, article):

        return f"""

TITLE

{article.title}

SUMMARY

{article.summary}

SOURCE

{article.source}

"""

    def analyze(self, article):

        response = self.client.chat.completions.create(

            model=MODEL,

            temperature=0.6,

            response_format={
                "type":"json_object"
            },

            messages=[

                {
                    "role":"system",
                    "content":SYSTEM_PROMPT
                },

                {
                    "role":"user",
                    "content":self.build_prompt(article)
                }

            ]

        )

        content = response.choices[0].message.content

        return json.loads(content)

    def process(self, article):

        result = self.analyze(article)

        article.score = result["viral_score"]

        article.headline = result["headline"]

        article.caption = result["caption"]

        article.hashtags = result["hashtags"]

        article.category = result["category"]

        article.emoji = result["emoji"]

        return article    def process(self, article):

        result = self.analyze(article)

        article.score = result["viral_score"]

        article.headline = result["headline"]

        article.caption = result["caption"]

        article.hashtags = result["hashtags"]

        article.category = result["category"]

        article.emoji = result["emoji"]

        return article
