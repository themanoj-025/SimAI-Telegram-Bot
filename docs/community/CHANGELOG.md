# Changelog

All notable changes to **AI-Telegram-News-Bot** are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-06-01

### Added

#### Core Bot
- Telegram bot powered by `python-telegram-bot` v20.x with Gemini AI summarization
- Daily AI news digest delivered to configured Telegram chat
- Commands: `/start`, `/help`, `/news`, `/sources`, `/about`
- Polling-based message handling with command routing

#### News Scrapers
- **`ai_features_scraper.py`** — AI model comparison, roadmap, and leaderboard sites
- **`github_scraper.py`** — GitHub trending repositories in AI/ML categories
- **`indian_news_scraper.py`** — Indian tech news via RSS + HTML scraping
- **`news_scraper.py`** — General AI news, arXiv papers, blogs, YouTube
- **`extended_scrapers.py`** — Job listings, learning resources, models, tools, trending, startups
- Error isolation per scraper — one scraper failure doesn't crash the bot

#### Summarization Engine
- Google Gemini AI (`gemini-2.0-flash`) for article summarization
- Configurable summary style and length via prompt templates
- Caching via `diskcache` to avoid re-summarizing same content

#### Report Generation
- Multi-source report compilation with deduplication
- Formatted Telegram message output with source attribution
- RSS feed support via `feedparser`

#### Scheduling
- APScheduler-based scheduling every 2 hours
- Optional daily summary at 9:00 AM

#### Infrastructure
- Railway deployment config (`railway.json`)
- Render deployment config (`render.yaml`)
- Procfile with gunicorn for process management
- Environment variable configuration for API keys
- Comprehensive logging via Python stdlib

---

## [0.1.0] — Initial Development

### Added
- Project scaffolding and module structure
- Basic scraper framework
- Initial Gemini API integration
- Configuration system for environment variables
