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

<p align="center">
  <strong>Stop drowning in AI news. Let the bot bring it to you.</strong>
  <br />
  Aggregates from 16+ sources, summarizes with Gemini, and delivers daily digests to your Telegram.
</p>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📋 Environment Variables](#-environment-variables)
- [🎯 Commands](#-commands)
- [🏗️ Architecture](#️-architecture)
- [🛡️ Reliability Strategy](#️-reliability-strategy)
- [📁 Project Structure](#-project-structure)
- [🧪 Testing](#-testing)
- [🚢 Deployment](#-deployment)
- [🔧 Development](#-development)
- [🗺️ Roadmap](#️-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [🙏 Acknowledgements](#-acknowledgements)
- [📬 Support](#-support)

---

## 📸 Screenshots

> _To add screenshots: run the bot, capture your screen, save images to `docs/assets/`, and reference them below._
>
> **Suggested screenshots:**
> - `/daily` brief delivered in Telegram
> - `/compare` model comparison output
> - Bot responding to a free-text query

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📰 **16+ News Sources** | GitHub trending, arXiv, RSS feeds, AI blogs, Twitter/X |
| 🇮🇳 **India Focus** | Dedicated Indian AI news coverage |
| 🤖 **AI Summaries** | Gemini-powered article summarization (optional) |
| 🔄 **Auto-Broadcast** | Scheduled delivery every 2 hours |
| 🛡️ **Reliability-First** | Falls back to cached/curated content on failure |
| 📊 **Model Compare** | Compare GPT-4o, Claude, and Gemini |
| 🎓 **Learning Paths** | Personalized AI learning roadmaps |
| 💬 **18 Commands** | Comprehensive command set for every need |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Telegram bot token from [@BotFather](https://t.me/BotFather)

### Option 1: Docker (Recommended)

```bash
# Clone and configure
git clone https://github.com/themanoj-025/SimAI-Telegram-Bot.git
cd SimAI-Telegram-Bot
cp .env.example .env
# Edit .env with your TELEGRAM_BOT_TOKEN

# Start with Docker
docker compose up -d

# View logs
docker compose logs -f
```

### Option 2: Local Development

```bash
# Clone and setup
git clone https://github.com/themanoj-025/SimAI-Telegram-Bot.git
cd SimAI-Telegram-Bot
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your TELEGRAM_BOT_TOKEN to .env

# Run the bot
python run_bot.py
```

---

## 📋 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | ✅ | — |
| `TELEGRAM_CHAT_ID` | Chat ID for auto-broadcast | ❌ | — |
| `GEMINI_API_KEY` | Google Gemini API key for summaries | ❌ | — |

> 💡 **Tip:** Get your chat ID by sending a message to your bot and visiting `https://api.telegram.org/bot<TOKEN>/getUpdates`

---

## 🎯 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Welcome message & command overview | `/start` |
| `/daily` | Full daily AI intelligence brief | `/daily` |
| `/summary` | AI-powered news summary | `/summary` |
| `/news` | Global AI/ML news | `/news` |
| `/papers` | Latest arXiv research papers | `/papers` |
| `/tools` | Trending AI tools & platforms | `/tools` |
| `/models` | Recent model releases | `/models` |
| `/compare` | Compare AI models | `/compare GPT-4o vs Claude` |
| `/blogs` | AI blog updates | `/blogs` |
| `/jobs` | AI job opportunities | `/jobs` |
| `/startups` | Startup & funding updates | `/startups` |
| `/trending` | Community trends | `/trending` |
| `/learn` | AI learning resources | `/learn` |
| `/india` | India-focused AI news | `/india` |
| `/youtube` | AI YouTube content | `/youtube` |
| `/twitter` | Curated X/Twitter posts | `/twitter` |
| `/roadmap` | AI learning paths | `/roadmap` |
| `/leaderboard` | Top AI models ranked | `/leaderboard` |

> 💡 **Tip:** You can also send free-text messages like "news", "tools", or "compare" and the bot will route them automatically!

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Telegram Platform                             │
│  ┌──────────┐    ┌──────────────┐    ┌────────────────────────┐ │
│  │  User    │───▶│  Bot API     │───▶│  long-polling worker   │ │
│  │ Commands │    │ (send/recv)  │    │  (python-telegram-bot) │ │
│  └──────────┘    └──────────────┘    └───────────▲────────────┘ │
└─────────────────────────────────────────────────┼───────────────┘
                                                  │
                                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI Daily Bot                                  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Report Generator                                        │   │
│  │  • Routes commands to scrapers                           │   │
│  │  • Formats Telegram output                               │   │
│  │  • Handles comparison & leaderboards                     │   │
│  └───────────────────────┬──────────────────────────────────┘   │
│                          │                                      │
│                          ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  16+ Scrapers                                            │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │   │
│  │  │ GitHub  │ │ arXiv   │ │ Twitter │ │ Indian  │       │   │
│  │  │ Trending│ │ Papers  │ │   X     │ │  News   │       │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘       │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │   │
│  │  │  News   │ │  Tools  │ │  Blogs  │ │  Jobs   │       │   │
│  │  │  RSS    │ │ & Start │ │         │ │         │       │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘       │   │
│  └───────────────────────┬──────────────────────────────────┘   │
│                          │                                      │
│                          ▼                                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Reliability Layer                                       │   │
│  │  Live Fetch → Cache → Curated Fallback                   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛡️ Reliability Strategy

The bot never fails silently. When live sources are unavailable:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│ Live Source  │────▶│   Cache     │────▶│ Curated Fallback│
│  (RSS/API)   │     │ (diskcache) │     │ (hardcoded)     │
└─────────────┘     └─────────────┘     └─────────────────┘
     │ Fail               │ Miss              │ Always Ready
     ▼                    ▼                   ▼
  Use Cache          Use Fallback         Return Data
```

---

## 📁 Project Structure

```
AI-Telegram-News-Bot/
├── run_bot.py                    # Entry point & command handlers
├── config/
│   └── config.py                 # Environment configuration
├── scrapers/
│   ├── async_base_scraper.py     # Base async HTTP class
│   ├── news_scraper.py           # RSS feed scraper
│   ├── github_scraper.py         # GitHub trending
│   ├── twitter_scraper.py        # X/Twitter posts
│   ├── ai_features_scraper.py    # Tools, startups, models
│   ├── indian_news_scraper.py    # India-focused news
│   ├── extended_scrapers.py      # YouTube, blogs, jobs
│   └── fallback_data.py          # Curated fallback content
├── services/
│   ├── report_generator.py       # Command → Report routing
│   ├── scheduler.py              # Auto-broadcast (2hr)
│   └── summarizer.py             # Gemini AI summaries
├── utils/
│   ├── cache_manager.py          # Disk caching
│   ├── logger.py                 # Structured logging
│   └── telegram_utils.py         # Message formatting
├── tests/                        # CLI test scripts
├── scripts/                      # Operational verification tools
├── docker-compose.yml            # Docker orchestration
├── Dockerfile                    # Multi-stage build
└── requirements.txt              # Dependencies
```

---

## 🧪 Testing

```bash
# Run command tests
python tests/test_all_commands.py

# Run scraper tests
python tests/test_all_scrapers.py

# Run Indian news scraper tests
python tests/test_indian_scraper.py
```

---

## 🚢 Deployment

### Docker

```bash
docker compose up -d
```

### Render

The `render.yaml` is pre-configured. Just connect your GitHub repo.

### Railway

The `railway.json` is pre-configured. Deploy with one click.

### Heroku

```bash
git push heroku main
```

---

## 🔧 Development

### Add a New Scraper

1. Create a new file in `scrapers/`
2. Implement the scraper class with `fetch_<type>(count)` method
3. Register it in `services/report_generator.py`
4. Add the command handler in `run_bot.py`

### Add a New Command

1. Add the command to the `COMMANDS` list in `run_bot.py`
2. Create a handler function
3. Register with `application.add_handler(CommandHandler("cmd", handler))`

---

## 🗺️ Roadmap

- [x] Multi-source aggregation (16+)
- [x] Gemini AI summarization
- [x] Auto-broadcast scheduler
- [x] Docker deployment
- [x] CI/CD pipeline
- [ ] Webhook support (vs. long-polling)
- [ ] User preference storage
- [ ] Custom news filters
- [ ] Sentiment analysis
- [ ] Multi-language support

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](docs/community/CONTRIBUTING.md).

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push and open a PR

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [python-telegram-bot](https://python-telegram-bot.org/) - Telegram Bot API
- [Google Gemini](https://ai.google.dev/) - AI Summarization
- [feedparser](https://feedparser.readthedocs.io/) - RSS parsing
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing

---

## 📬 Support

- 🐛 [Report Bug](https://github.com/themanoj-025/SimAI-Telegram-Bot/issues)
- 💡 [Request Feature](https://github.com/themanoj-025/SimAI-Telegram-Bot/issues)
- ⭐ [Star the Repo](https://github.com/themanoj-025/SimAI-Telegram-Bot)

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/themanoj-025">themanoj-025</a>
</p>

<p align="center">
  If you find this bot useful, please give it a ⭐ star!
</p>
---

## ⭐ Star History

[![Last Commit](https://img.shields.io/github/last-commit/themanoj-025/SimAI-Telegram-Bot?style=flat-square)](https://github.com/themanoj-025/SimAI-Telegram-Bot)
[![Contributors](https://img.shields.io/github/contributors/themanoj-025/SimAI-Telegram-Bot?style=flat-square)](https://github.com/themanoj-025/SimAI-Telegram-Bot/graphs/contributors)

[![Star History Chart](https://api.star-history.com/svg?repos=themanoj-025/SimAI-Telegram-Bot&type=Date)](https://star-history.com/#SimAI-Telegram-Bot&Date)
