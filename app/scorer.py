from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


SYSTEM = """
Kamu editor media olahraga dan entertainment.

Nilai seberapa VIRAL berita berikut.

Nilai 0-100.

Kriteria:

Transfer pemain besar.

Messi.

Ronaldo.

Haaland.

Mbappe.

Son Heung Min.

BLACKPINK.

BTS.

IU.

Drama Korea.

Dating.

Comeback.

Netflix.

Cedera pemain.

Juara.

Skandal.

Berikan HANYA angka.

Contoh:

92
"""


class ViralScorer:

    def score(self, article):

        prompt = f"""

Judul:

{article['title']}

Ringkasan:

{article['summary']}

"""

        try:

            response = client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                temperature=0,

                max_tokens=10,

                messages=[

                    {
                        "role":"system",
                        "content":SYSTEM
                    },

                    {
                        "role":"user",
                        "content":prompt
                    }

                ]

            )

            value = response.choices[0].message.content.strip()

            value = int(value)

            article["score"] = value

        except:

            article["score"] = 0

        return article

    def process(self, articles):

        scored = []

        for article in articles:

            scored.append(self.score(article))

        scored.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return scored
