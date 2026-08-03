from collector import NewsCollector
from duplicate import DuplicateRemover
from scorer import ViralScorer
from ai import AIWriter
from history import History
from facebook import FacebookPublisher
from config import MIN_SCORE, MAX_POST


collector = NewsCollector()

duplicate = DuplicateRemover()

scorer = ViralScorer()

writer = AIWriter()

history = History()

facebook = FacebookPublisher()


def run():

    print("Collecting News...")

    news = collector.collect()

    print(f"Collected {len(news)} Articles")

    news = duplicate.process(news)

    print(f"Unique {len(news)} Articles")

    news = scorer.process(news)

    posted = 0

    for article in news:

        if posted >= MAX_POST:
            break

        if article["score"] < MIN_SCORE:
            continue

        if history.exists(article["link"]):
            continue

        print(article["title"])

        text = writer.rewrite(article)

        message = f"""{text}

📰 Sumber:
{article['source']}

🔗 {article['link']}
"""

        ok = facebook.publish(
            message,
            article["link"]
        )

        if ok:

            history.add(article["link"])

            posted += 1

            print("Posted")


if __name__ == "__main__":

    run()
