from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


SYSTEM = """
Kamu adalah editor media online profesional.

Tugasmu:

1. Buat judul click-worthy.

2. Jangan mengubah fakta.

3. Jangan membuat berita palsu.

4. Bahasa Indonesia.

5. Maksimal 150 kata.

6. Tambahkan emoji secukupnya.

7. Tambahkan CTA.

8. Tambahkan hashtag.

Output HARUS seperti ini:

JUDUL:
....

CAPTION:
....

HASHTAG:
#Football #KPop
"""


class AIWriter:

    def rewrite(self, article):

        prompt = f"""

Judul:

{article['title']}

Isi:

{article['summary']}

Sumber:

{article['source']}

"""

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            temperature=0.8,

            max_tokens=400,

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

        return response.choices[0].message.content
