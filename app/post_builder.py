from __future__ import annotations

from models import NewsArticle


class PostBuilder:

    def __init__(self):
        self.footer = (
            "\n\n━━━━━━━━━━━━━━\n"
            "📢 Follow Gosip.ID untuk berita olahraga dan hiburan terbaru."
        )

    def build(self, article: NewsArticle) -> str:
        hashtags = ""

        if article.hashtags:
            hashtags = " ".join(
                article.hashtags
            )

        text = f"""{article.emoji} {article.headline}

{article.article}

{hashtags}{self.footer}
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
    article.hashtags = [
        "#Arsenal",
        "#PremierLeague",
        "#Football",
    ]

    builder = PostBuilder()
    print(
        builder.build(
            article
        )
    )
    print()
    print(
        builder.build_comment(
            article
        )
    )
