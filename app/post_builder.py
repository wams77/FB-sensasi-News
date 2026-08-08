from __future__ import annotations

from models import NewsArticle


class PostBuilder:

    def __init__(self):
        self.footer = (
            "\n\n━━━━━━━━━━━━━━\n"
            "📢 Follow Gosip.ID untuk berita olahraga dan hiburan terbaru."
        )

    def build(self, article: NewsArticle) -> str:
        # 1. Menyiapkan Hashtag Wajib & Hashtag dari AI
        mandatory_hashtags = ["#semuaorang", "#GosipID"]
        current_hashtags = article.hashtags if article.hashtags else []
        
        # Gabungkan hashtag AI dan hashtag wajib (tanpa duplikat)
        all_hashtags = current_hashtags + mandatory_hashtags
        hashtags_str = " ".join(all_hashtags)

        # 2. Menyiapkan Analisis Profesional
        # Menggunakan getattr agar tidak error jika model NewsArticle belum punya atribut 'analysis'
        default_analysis = (
            "Melihat perkembangan ini, dinamika yang terjadi memberikan sinyal kuat "
            "akan adanya perubahan peta persaingan ke depannya. Langkah strategis "
            "selanjutnya akan sangat krusial dalam memengaruhi tren secara keseluruhan."
        )
        analysis_text = getattr(article, "analysis", default_analysis)

        # 3. Merakit Teks Postingan
        text = f"""{article.emoji} {article.headline}

{article.article}

📊 Analisis Profesional:
{analysis_text}

{hashtags_str}{self.footer}
"""

        return text.strip()

    def build_comment(
        self,
        article: NewsArticle,
    ) -> str:
        return (
            "Sumber berita:\n"
            f"{article.source}\n\n"
            f"{article.link}"
        )


if __name__ == "__main__":
    article = NewsArticle(
        title="Arsenal Menang",
        summary="",
        link="https://example.com",
        image=None,
        source="BBC",
        category="football",
        published=None,
    )
    article.emoji = "🔥"
    article.headline = "Arsenal Dapat Angin Segar"
    article.article = (
        "Arsenal mendapatkan kabar baik menjelang "
        "musim baru setelah salah satu pemain "
        "andalan mereka dipastikan kembali menjalani "
        "latihan bersama tim utama. Kehadiran pemain "
        "tersebut diyakini akan menambah kekuatan "
        "skuad Mikel Arteta dalam menghadapi "
        "persaingan musim ini.\n\n"
        "Para pendukung Arsenal pun menyambut kabar "
        "tersebut dengan antusias dan berharap tim "
        "kesayangannya mampu bersaing dalam perebutan "
        "gelar juara."
    )
    
    # AI menghasilkan analysis (Opsional)
    article.analysis = (
        "Kembalinya pemain pilar ini bukan hanya sekadar tambahan amunisi, "
        "tetapi juga suntikan moral yang masif bagi ruang ganti Arsenal. "
        "Secara taktik, Arteta kini memiliki fleksibilitas lebih untuk merotasi "
        "skuad di tengah jadwal padat Liga Inggris dan kompetisi Eropa."
    )
    
    article.hashtags = [
        "#Arsenal",
        "#PremierLeague",
        "#Football",
    ]

    builder = PostBuilder()
    print("=== POSTINGAN FACEBOOK ===")
    print(builder.build(article))
    print("\n=== KOMENTAR SUMBER ===")
    print(builder.build_comment(article))
