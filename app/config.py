from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"
LOG_DIR = BASE_DIR / "logs"
OUTPUT_DIR = BASE_DIR / "output"

DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================
# API
# ============================================

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    "",
)

FACEBOOK_PAGE_ID = os.getenv(
    "FACEBOOK_PAGE_ID",
    "",
)

FACEBOOK_ACCESS_TOKEN = os.getenv(
    "FACEBOOK_ACCESS_TOKEN",
    "",
)


# ============================================
# BOT
# ============================================

MAX_POST = int(

    os.getenv(

        "MAX_POST",

        "1",

    )

)

MIN_VIRAL_SCORE = int(

    os.getenv(

        "MIN_VIRAL_SCORE",

        "80",

    )

)

REQUEST_TIMEOUT = int(

    os.getenv(

        "REQUEST_TIMEOUT",

        "30",

    )

)

MAX_RETRY = int(

    os.getenv(

        "MAX_RETRY",

        "3",

    )

)

RSS_LIMIT = int(

    os.getenv(

        "RSS_LIMIT",

        "10",

    )

)

GOOGLE_LIMIT = int(

    os.getenv(

        "GOOGLE_LIMIT",

        "5",

    )

)


USER_AGENT = (

    "Mozilla/5.0 "

    "(Windows NT 10.0; Win64; x64) "

    "AppleWebKit/537.36 "

    "(KHTML, like Gecko) "

    "Chrome/138 Safari/537.36"

)

# ============================================
# RSS SOURCES
# ============================================

RSS_FEEDS = [

    {
        "name": "BBC Football",
        "category": "football",
        "url": "https://feeds.bbci.co.uk/sport/football/rss.xml",
    },

    {
        "name": "ESPN Soccer",
        "category": "football",
        "url": "https://www.espn.com/espn/rss/soccer/news",
    },

    {
        "name": "Soompi",
        "category": "kpop",
        "url": "https://www.soompi.com/feed",
    },

    {
        "name": "Korea Herald",
        "category": "entertainment",
        "url": "https://www.koreaherald.com/rss",
    },

    {
        "name": "Yonhap Entertainment",
        "category": "entertainment",
        "url": "https://en.yna.co.kr/RSS/news.xml",
    },

]


# ============================================
# GOOGLE NEWS KEYWORDS
# ============================================

GOOGLE_KEYWORDS = [

    # Football

    "Lionel Messi",

    "Cristiano Ronaldo",

    "Erling Haaland",

    "Kylian Mbappe",

    "Manchester United",

    "Liverpool",

    "Real Madrid",

    "Barcelona",

    "Arsenal",

    "Chelsea",

    "Tottenham",

    "Premier League",

    "Champions League",

    "Transfer Football",

    # Korea

    "BLACKPINK",

    "BTS",

    "IU",

    "aespa",

    "NewJeans",

    "IVE",

    "LE SSERAFIM",

    "Korean Drama",

    "Netflix Korea",

    "Disney+ Korea",

    "KPop",

]
