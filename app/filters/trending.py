from __future__ import annotations

import random
from models import NewsArticle


class TrendingFilter:

    def __init__(self):
        self.keywords = {
            # Football
            "messi": 20,
            "ronaldo": 20,
            "haaland": 18,
            "mbappe": 18,
            "real madrid": 15,
            "barcelona": 15,
            "liverpool": 15,
            "arsenal": 15,
            "chelsea": 15,
            "manchester united": 18,
            "premier league": 15,
            "champions league": 18,
            "transfer": 18,
            "breaking": 20,
            "official": 12,

            # Korea
            "blackpink": 20,
            "bts": 20,
            "iu": 18,
            "aespa": 18,
            "newjeans": 18,
            "kdrama": 15,
            "korean drama": 15,
            "netflix": 12,
            "disney+": 10,
        }

    def score(self, article: NewsArticle) -> int:
        text = f"{article.title} {article.summary}".lower()
        total_score = 0

        for keyword, value in self.keywords.items():
            if keyword in text:
                total_score += value

        return total_score

    def process(
        self,
        articles,
        limit: int = 20,
    ):
        # Berikan sedikit variasi acak agar urutan tidak kaku pada skor yang sama
        articles_list = list(articles)
        random.shuffle(articles_list)

        # Urutkan berdasarkan skor trending
        ranked = sorted(
            articles_list,
            key=self.score,
            reverse=True,
        )

        return ranked[:limit]
