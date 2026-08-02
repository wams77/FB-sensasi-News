from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")

FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")

MAX_POST = int(os.getenv("MAX_POST", 1))

MIN_SCORE = int(os.getenv("MIN_SCORE", 70))


RSS_FEEDS = [

    # FOOTBALL

    "https://feeds.bbci.co.uk/sport/football/rss.xml",

    "https://www.espn.com/espn/rss/soccer/news",

    "https://www.fifa.com/rss/index.xml",

    "https://www.goal.com/feeds/en/news",

    # KOREA

    "https://www.soompi.com/feed",

    "https://www.koreaherald.com/rss",

]
