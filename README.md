<p align="center">
  <img src="https://img.shields.io/badge/AI%20Daily%20Bot-Telegram%20News-2CA5E0?style=for-the-badge" alt="AI Daily Telegram Bot Logo" />
</p>

<h1 align="center">AI Daily Telegram Bot</h1>

<p align="center">
  <strong>Automated AI/ML news aggregation, smart summarization, and scheduled Telegram delivery.</strong>
</p>

<p align="center">
  <a href="https://github.com/themanoj-025/SimAI-Telegram-Bot/actions"><img src="https://img.shields.io/github/actions/workflow/status/themanoj-025/SimAI-Telegram-Bot/ci.yml?style=flat-square&label=CI" alt="CI Status" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License MIT" /></a>
  <a href="https://github.com/themanoj-025/SimAI-Telegram-Bot/stargazers"><img src="https://img.shields.io/github/stars/themanoj-025/SimAI-Telegram-Bot?style=social" alt="GitHub Stars" /></a>
  <a href="https://github.com/themanoj-025/SimAI-Telegram-Bot/issues"><img src="https://img.shields.io/github/issues/themanoj-025/SimAI-Telegram-Bot?style=flat-square" alt="GitHub Issues" /></a>
  <a href="https://github.com/themanoj-025/SimAI-Telegram-Bot/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square" alt="PRs Welcome" /></a>
</p>

---

## Overview

AI Daily Telegram Bot monitors 16+ top artificial intelligence and machine learning publications, distills technical articles into concise bulleted briefs using Google Gemini, and delivers scheduled digests directly to your Telegram channel, group, or direct message.

Beyond scheduled broadcasts, the bot responds to interactive in-chat queries, generates on-demand summaries of breaking news, and provides side-by-side LLM model comparisons.

---

## Table of Contents

- [Key Features](#key-features)
- [Bot Commands](#bot-commands)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Quick Start](#installation--quick-start)
- [Configuration](#configuration)
- [Testing](#testing)
- [Deployment](#deployment)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)
- [Support](#support)

---

## Key Features

- **Multi-Source Aggregation**: Periodically parses 16+ high-signal RSS/Atom feeds (including arXiv, OpenAI, Google AI, Hugging Face, MIT Tech Review).
- **Gemini-Powered Summaries**: Condenses dense machine learning papers and news into key takeaways and practical implications.
- **Automated Broadcast Engine**: Periodically broadcasts new stories every 2 hours or on a configurable schedule, caching delivered items in SQLite (`bot_cache.db`) to eliminate duplicates.
- **Interactive On-Demand Chat**: Allows users to request instant digests or query topics directly inside Telegram.
- **Resilient Circuit Breaker**: Includes failure fallback patterns (`circuit_breaker.py`) and built-in health monitoring (`health_server.py`).

---

## Bot Commands

| Command | Action |
| :--- | :--- |
| `/start` | Welcome message, usage guide, and bot status |
| `/daily` | Fetch and deliver the latest curated daily AI brief |
| `/summary` | Generate an AI summary for the most recent trending articles |
| `/compare` | Run a side-by-side model comparison |
| `/help` | Detailed listing of commands and available sources |

---

## Architecture

```text
  [16+ AI/ML RSS Feeds]
           │
           ▼
     scrapers/ (Feedparser & Article Ingestion)
           │
           ▼
     SQLite Deduplication Cache (bot_cache.db)
           │
           ▼
     services/ (Google Gemini Summarizer API)
           │
     ┌─────┴─────────────────────────┐
     ▼                               ▼
Scheduled Auto-Broadcast       Interactive Commands
(Every 2 Hours / Daily)        (/daily, /summary, /compare)
     │                               │
     └───────────────┬───────────────┘
                     ▼
        Telegram Bot API (run_bot.py)
                     │
                     ▼
          Target Channels / Users
```

---

## Project Structure

```text
AI-Telegram-News-Bot/
├── config/                 # Feed sources, scheduler & bot configuration
├── scrapers/               # RSS feed parsers and content extractors
├── services/               # Gemini AI summarization and comparison services
├── utils/                  # Structured logging and formatting helpers
├── tests/                  # Pytest unit and integration test suite
├── circuit_breaker.py      # Resilient API failure isolation
├── get_chat_id.py          # Utility script to detect your Telegram Chat ID
├── health_server.py        # HTTP health check server for hosting platforms
├── run_bot.py              # Primary Telegram bot entry point
├── Dockerfile              # Multi-stage production container build
├── docker-compose.yml      # Local container orchestration
├── pyproject.toml          # Ruff and build configuration
├── requirements.txt        # Runtime dependencies
└── README.md               # Project documentation
```

---

## Prerequisites

- **Python**: `>= 3.11`
- **Telegram Bot Token**: Created via [@BotFather](https://t.me/BotFather)
- **Google Gemini API Key**: Acquired via Google AI Studio

---

## Installation & Quick Start

### 1. Clone & Setup Environment

```bash
# Clone the repository
git clone https://github.com/themanoj-025/SimAI-Telegram-Bot.git
cd SimAI-Telegram-Bot

# Create and activate virtual environment
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows: .venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Credentials

```bash
cp .env.example .env
```

Edit `.env` to include your credentials:
```env
TELEGRAM_BOT_TOKEN="your_bot_token_from_botfather"
TELEGRAM_CHAT_ID="your_channel_or_group_id"
GEMINI_API_KEY="your_gemini_api_key"
```

> [!TIP]
> If you don't know your Telegram Chat ID, run `python get_chat_id.py` and send a message to your bot in Telegram to print your chat ID.

### 3. Launch the Bot

```bash
python run_bot.py
```

On Windows, you can also launch via PowerShell:
```powershell
.\StartBot.ps1
```

---

## Configuration

| Environment Variable | Required | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `TELEGRAM_BOT_TOKEN` | **Yes** | — | Bot authentication token from @BotFather |
| `GEMINI_API_KEY` | **Yes** | — | API key for Gemini LLM summarization |
| `TELEGRAM_CHAT_ID` | No | — | Target chat or channel ID for auto-broadcasts |
| `DATABASE_PATH` | No | `bot_cache.db` | Path to SQLite deduplication database |
| `LOG_FILE` | No | `ai_daily_bot.log`| Local log file destination |

---

## Testing

```bash
# Run pytest test suite
pytest tests/ -v
```

---

## Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker compose up -d --build

# View running container logs
docker compose logs -f
```

### Cloud Platforms (Railway / Render)

The repository includes `railway.json`, `render.yaml`, and `Procfile`.
- **Worker Process**: `python run_bot.py`
- **Health Check Port**: `health_server.py` serves `/health` on port `8080` (or `PORT` environment variable).

---

## Roadmap

- [x] Automated aggregation across 16+ AI/ML sources
- [x] Gemini LLM-powered bulleted summaries
- [x] SQLite-based article deduplication
- [x] In-chat interactive queries and model comparison
- [ ] User-customizable subscription topics and filters <!-- TODO: Track via GitHub issue -->
- [ ] Multi-channel delivery routing <!-- TODO: Track via GitHub issue -->

---

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and development workflows.

---

## Security

Please report potential security vulnerabilities through [SECURITY.md](SECURITY.md).

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Support

- 🐛 **Issue Tracker**: [GitHub Issues](https://github.com/themanoj-025/SimAI-Telegram-Bot/issues)
- 💡 **Feature Requests**: Submit an issue or open a pull request on [GitHub](https://github.com/themanoj-025/SimAI-Telegram-Bot/pulls)
