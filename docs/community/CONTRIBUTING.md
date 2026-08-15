# Contributing to AI-Telegram-News-Bot

Thank you for your interest in contributing to the AI Daily Telegram Bot! This document outlines the guidelines for contributing.

## Getting Started

### Prerequisites
- Python 3.11+
- A Telegram bot token (from [@BotFather](https://t.me/BotFather))
- A Google Gemini API key (from [Google AI Studio](https://aistudio.google.com/))

### Setup
1. Fork and clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your keys:
   ```bash
   cp .env.example .env
   ```
5. Run the bot to verify it starts correctly:
   ```bash
   python run_bot.py
   ```

### Required Environment Variables
| Variable | Description |
| --- | --- |
| `TELEGRAM_BOT_TOKEN` | Your bot's token from BotFather |
| `TELEGRAM_CHAT_ID` | Target chat/channel ID for digests |
| `GEMINI_API_KEY` | Your Google Gemini API key |

## Code Style

- Follow PEP 8 for Python code.
- Use descriptive variable and function names.
- Add docstrings to all public functions and classes.
- Keep functions focused and single-purpose.
- Use async/await for I/O-bound operations (network requests, API calls).

## Project Structure

- **`scrapers/`** — One file per source category (news, github, twitter, indian_news, etc.)
- **`services/`** — Core orchestration (report_generator, scheduler, summarizer)
- **`utils/`** — Shared utilities (cache, logging, telegram formatting)
- **`config/`** — Configuration class and constants

When adding a new scraper:
1. Create a new file or add to an existing scraper module in `scrapers/`
2. Follow the existing scraper pattern (fetch → parse → return structured data)
3. Register the scraper in `services/report_generator.py`

## Running Tests

Run test scripts individually to validate changes:
```bash
python tests/test_all_scrapers.py
python tests/test_bot_logic.py
python scripts/verify_async_scrapers.py
```

There is no formal pytest suite — tests are standalone Python scripts. If you add a new scraper or feature, please include a corresponding test script.

## Submitting Changes

1. Create a new branch for your feature or fix:
   ```bash
   git checkout -b feat/my-feature
   ```
2. Make your changes, keeping them focused and minimal.
3. Run the relevant test scripts to verify nothing is broken.
4. Commit with a descriptive message:
   - Format: `type(scope): description`
   - Types: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`
   - Example: `feat(scraper): add Reddit scraper for AI community posts`
5. Push and open a Pull Request.

## Reporting Issues

When reporting a bug, please include:
- The error message and stack trace (if applicable)
- Steps to reproduce
- Your environment (Python version, OS)
- Whether the issue is with a specific scraper (name the source site)

## Adding News Sources

1. Add the RSS feed URL or scrape target to `config/config.py` in the appropriate category.
2. If a new scraper module is needed, create it in `scrapers/` following the existing pattern.
3. Register the scraper in `services/report_generator.py`.

## Deployment Notes

- Primary deployment: Railway (uses `railway.json` + `Procfile`)
- Alternative: Render (uses `render.yaml` + `Procfile`)
- The bot runs as a **worker** process (not web), using long-polling
- Do not introduce webhook mode without updating deployment configs

## Code of Conduct

This project and everyone participating in it is governed by the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.
