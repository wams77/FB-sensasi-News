from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


SYSTEM_PROMPT = """
Kamu adalah editor berita profesional.

Aturan:

- Jangan mengubah fakta.
- Jangan membuat berita palsu.
- Buat judul sangat menarik.
- Maksimal 120 kata.
- Tambahkan emoji seperlunya.
- Akhiri dengan pertanyaan kepada pembaca.
- Bahasa Indonesia.
"""


def rewrite(article):

    prompt = f"""

Judul:
{article['title']}

Isi:
{article['summary']}

Link:
{article['link']}

"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role":"system",
                "content":SYSTEM_PROMPT
            },
            {
                "role":"user",
                "content":prompt
            }
        ],

        temperature=0.9,

        max_tokens=350

    )

    return response.choices[0].message.content
