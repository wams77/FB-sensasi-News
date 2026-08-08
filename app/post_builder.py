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
        
        # Gabungkan hashtag (mencegah duplikasi jika AI kebetulan membuat hashtag yang sama)
        all_hashtags = current_hashtags + [h for h in mandatory_hashtags if h not in current_hashtags]
        hashtags_str = " ".join(all_hashtags)

        # 2. Menyiapkan Analisis dari AI (Tanpa teks default)
        analysis_section = ""
        # Mengecek apakah atribut 'analysis' ada dan tidak kosong
        if hasattr(article, "analysis") and article.analysis:
            analysis_section = f"\n\n📊 Analisis Profesional:\n{article.analysis}"

        # 3. Merakit Teks Postingan
        text = f"""{article.emoji} {article.headline}

{article.article}{analysis_section}

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
    
    # Simulasi: AI membaca teks di atas dan menyimpulkan analisis ini
    article.analysis = (
        "Kembalinya pemain inti ini tidak hanya menaikkan moral tim, tetapi juga "
        "memberikan Mikel Arteta opsi taktis yang krusial. Dalam perburuan gelar "
        "Premier League yang ketat, kedalaman skuad sering kali menjadi penentu "
        "utama antara juara dan runner-up."
    )
    
    article.hashtags = [
        "#Arsenal",
        "#PremierLeague",
        "#Football",
    ]

    builder = PostBuilder()
    print("=== POSTINGAN FACEBOOK ===")
    print(builder.build(article))
