from __future__ import annotations

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

        score = 0

        for keyword, value in self.keywords.items():

            if keyword in text:

                score += value

        return score

    def process(

        self,

        articles,

        limit: int = 20,

    ):

        ranked = sorted(

            articles,

            key=self.score,

            reverse=True,

        )

        return ranked[:limit]
