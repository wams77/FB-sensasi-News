from rapidfuzz import fuzz


class DuplicateRemover:

    def __init__(self, threshold=88):
        self.threshold = threshold

    def process(self, articles):

        unique = []

        for article in articles:

            duplicated = False

            for u in unique:

                score = fuzz.token_sort_ratio(
                    article["title"],
                    u["title"]
                )

                if score >= self.threshold:
                    duplicated = True
                    break

            if not duplicated:
                unique.append(article)

        return unique
