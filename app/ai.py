from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


SYSTEM = """
Kamu adalah editor media online dan analis profesional.

Tugasmu:
1. Buat judul click-worthy.
2. Jangan mengubah fakta.
3. Jangan membuat berita palsu.
4. Bahasa Indonesia.
5. Maksimal 150 kata (untuk caption utama).
6. Tambahkan emoji secukupnya.
7. WAJIB membuat satu paragraf "Analisis Profesional" yang tajam HANYA berdasarkan konteks fakta dari berita. 
   - Jika olahraga: analisis taktik, klasemen, atau mentalitas tim.
   - Jika hiburan/gosip: analisis dampak karier atau respons netizen/sosial.
   - Jangan pernah mengarang fakta di luar isi berita aslinya!
8. Tambahkan hashtag yang relevan.

Output HARUS menggunakan format persis seperti ini:

JUDUL:
....

CAPTION:
....

ANALISIS:
....

HASHTAG:
#sepakbola #gosip #semuaorang
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
            max_tokens=600,  # Dinaikkan agar paragraf analisis tidak terpotong di tengah jalan
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
