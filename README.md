# FB Sensasi News

AI Facebook News Bot menggunakan:

- Groq AI
- Facebook Graph API
- GitHub Actions

## Feature

- Multi RSS
- Google News RSS
- Football News
- Korean Entertainment
- AI Rewrite
- AI Viral Score
- Auto Hashtag
- Auto Facebook Posting
- Duplicate History
- Logging

## Install

```bash
pip install -r requirements.txt
```

Copy

```
.env.example
```

menjadi

```
.env
```

isi API.

Jalankan

```bash
python app/bot.py
```

## GitHub Secrets

Tambahkan pada repository

```
GROQ_API_KEY

FACEBOOK_PAGE_ID

FACEBOOK_ACCESS_TOKEN
```

GitHub Actions akan berjalan setiap 30 menit.
