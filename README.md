# 🤖 AI Daily Telegram Bot

<p align="center">
  <img src="https://img.shields.io/badge/AI%20Daily%20Bot-Telegram%20News-2CA5E0?style=for-the-badge" alt="AI Daily Telegram Bot" />
</p>

<h1 align="center">🤖 AI Daily Telegram Bot</h1>

<p align="center">
  <strong>Your Personal AI/ML News Curator — Delivered to Telegram</strong>
</p>

<p align="center">
  <a href="https://github.com/themanoj-025/SimAI-Telegram-Bot/actions"><img src="https://img.shields.io/github/actions/workflow/status/themanoj-025/SimAI-Telegram-Bot/ci.yml?style=flat-square&label=CI" alt="CI Status" /></a>
  <a href="https://github.com/themanoj-025/SimAI-Telegram-Bot/blob/main/LICENSE"><img src="https://img.shields.io/github/license/themanoj-025/SimAI-Telegram-Bot?style=flat-square" alt="License" /></a>
  <a href="https://github.com/themanoj-025/SimAI-Telegram-Bot/stargazers"><img src="https://img.shields.io/github/stars/themanoj-025/SimAI-Telegram-Bot?style=social" alt="Stars" /></a>
  <a href="https://github.com/themanoj-025/SimAI-Telegram-Bot/issues"><img src="https://img.shields.io/github/issues/themanoj-025/SimAI-Telegram-Bot?style=flat-square" alt="Issues" /></a>
</p>

---

## 📋 Table of Contents

- [What it does](#what-it-does)
- [Screenshots](#screenshots)
- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [🚀 Quick start](#-quick-start)
- [📋 Environment variables](#-environment-variables)
- [📁 Project structure](#-project-structure)
- [🧪 Testing](#-testing)
- [🚢 Deployment](#-deployment)
- [🗺️ Roadmap](#️-roadmap)
- [🤝 Contributing](#-contributing)
- [📬 Support](#-support)
- [License](#license)

---

## What it does

Aggregates AI/ML news from 16+ sources, summarizes each article with a large-language-model, and delivers a daily digest to your Telegram channel or chat. It can also respond to free-text queries in chat, and compares models side-by-side.

> [!NOTE] The bot runs on a schedule (daily digest) but processes on-demand queries immediately — the schedule and the query path are separate code paths and can be run independently.

## Screenshots

> To add screenshots: run the bot, capture your screen, save images to `docs/assets/`, and reference them below.
>
> **Suggested screenshots:**
> - `/daily` brief delivered in Telegram
> - `/compare` model comparison output
> - Bot responding to a free-text query

---

## ✨ Features

| Feature | Description |
| --- | --- |
| 📅 **Daily digest** | Scheduled aggregation of 16+ AI/ML news sources, summarized per article |
| 💬 **Chat queries** | Free-text Q&A about AI news, answered over Telegram |
| 📊 **Model comparison** | Side-by-side comparison of LLM models (via Gemini) |
| 🔔 **Scheduled delivery** | APScheduler-backed daily digest at a configured time |
| 🌐 **Multi-source** | Aggregates from 16+ sources via feedparser |

## 🏗️ Architecture

```text
AI Daily Telegram Bot/
├── scrapers/               # Source aggregators (RSS/HTML)
├── services/               # Summarization + comparison services
├── config/                 # Settings (Telegram token, LLM key, schedule)
├── utils/                  # Helpers (logging, scheduling)
└── main.py                 # Bot entry point (python-telegram-bot)
```

## 🚀 Quick start

### Prerequisites

- Python 3.11 or newer
- A Telegram Bot Token (from @BotFather)
- A Gemini API key for summarization/comparison

### Install & run

```bash
# 1. Clone the repository
git clone https://github.com/themanoj-025/SimAI-Telegram-Bot.git
cd SimAI-Telegram-Bot

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and edit the environment template
cp .env.example .env
#   → Set TELEGRAM_BOT_TOKEN, GEMINI_API_KEY, and SCHEDULER_DAILY_HOUR

# 5. Run the bot
python main.py
```

### Environment variables

| Variable | Default | Required | Description |
| --- | --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | — | Yes | Token from @BotFather |
| `GEMINI_API_KEY` | — | Yes | Gemini API key for LLM summarization |
| `SCHEDULER_DAILY_HOUR` | `9` | No | Hour (UTC) to send the daily digest |
| `REQUESTS_TIMEOUT` | `30` | No | Seconds to wait on HTTP requests |

## 📋 Environment variables

(Duplicate of the table above for cross-referencing. Same rows.)

## 📁 Project structure

```
AI-Telegram-News-Bot/
├── scrapers/               # Source aggregators
├── services/               # Summarization + comparison
├── config/                 # Settings
├── utils/                  # Helpers
├── main.py                 # Bot entry point
├── requirements.txt
└── .env.example
```

## 🧪 Testing

```bash
# Run the test suite
pytest tests/ -v
```

## 🚢 Deployment

### Schedule (GitHub Actions)

```yaml
# .github/workflows/schedule-daily-brief.yml
name: Daily AI Brief
on:
  schedule:
    - cron: '0 9 * * *'   # Daily at 09:00 UTC
jobs:
  brief:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python -m services.daily_brief
```

> [!NOTE] For a self-hosted alternative, `APScheduler` runs the digest in-process; GitHub Actions is the recommended production schedule so the bot can wake up without a long-running VM.

## 🗺️ Roadmap

> [!CAUTION] Checked items are built and verified. Unchecked items are tracked in the issue tracker.

- [x] Daily digest from 16+ sources
- [x] Gemini-based article summaries
- [x] Free-text chat queries
- [x] Model comparison command
- [ ] User-friendly onboarding / setup wizard
- [ ] Multiple recipient routing

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## 📬 Support

- 🐛 [Report a bug](https://github.com/themanoj-025/SimAI-Telegram-Bot/issues)
- 💡 [Request a feature](https://github.com/themanoj-025/SimAI-Telegram-Bot/issues)
- 📧 Email the maintainer via the issue tracker

## License

MIT License — see [LICENSE](LICENSE).
