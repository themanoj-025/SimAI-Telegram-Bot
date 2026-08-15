# AI-Telegram-News-Bot — Copilot Instructions

## Code conventions
- Python with 4-space indentation
- Async patterns with aiohttp for HTTP requests
- Fallback content pattern: try live source → cache → curated fallback
- Environment variables via python-dotenv from .env file

## Key commands
- Start: `python run_bot.py`
- Scraper tests: `python tests/test_all_scrapers.py`
- Bot logic: `python tests/test_bot_logic.py`

## Architecture
- `scrapers/` — individual news source scrapers
- `services/` — report generation, scheduling, summarization
- `utils/` — cache, logging, Telegram helpers
- Fallback system ensures bot never crashes on source failures
