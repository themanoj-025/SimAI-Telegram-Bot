# AI Daily Telegram Bot

> Automated Telegram bot that aggregates, summarizes, and delivers daily AI/ML news digests from 16+ sources with reliability-first architecture.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-2CA5E0)](https://core.telegram.org/bots)
[![CI](https://img.shields.io/badge/CI-passing-brightgreen)](https://github.com/themanoj-025/ai_daily_telegram_bot/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Table of Contents

- [1. Executive Summary](#1-executive-summary)
- [2. Tech Stack & Core Technologies](#2-tech-stack--core-technologies)
- [3. High-Level Architecture](#3-high-level-architecture)
- [4. Complete Folder Structure Tree](#4-complete-folder-structure-tree)
- [5. Exhaustive File-by-File & Folder-by-Folder Breakdown](#5-exhaustive-file-by-file--folder-by-folder-breakdown)
- [6. Data Models & Schemas](#6-data-models--schemas)
- [7. API Surface](#7-api-surface)
- [8. Configuration & Environment Variables](#8-configuration--environment-variables)
- [9. Build, Run & Deployment Instructions](#9-build-run--deployment-instructions)
- [10. Data & Control Flow Walkthroughs](#10-data--control-flow-walkthroughs)
- [11. Dependency Graph Summary](#11-dependency-graph-summary)
- [12. Testing Strategy](#12-testing-strategy)
- [13. Known Issues, Technical Debt & Assumptions](#13-known-issues-technical-debt--assumptions)
- [14. Glossary](#14-glossary)
- [15. Appendix](#15-appendix)

---

## 1. Executive Summary

**AI Daily Telegram Bot** is an automated Telegram bot that aggregates, summarizes, and delivers daily AI/ML news digests from multiple sources including GitHub trending, news RSS feeds, Twitter/X, Indian news sources, and AI model comparison sites. The bot is designed with a **reliability-first architecture**: if live sources fail, it falls back to cached or curated content instead of crashing.

**Target users**: AI/ML enthusiasts, researchers, developers, and teams who want a daily curated AI news digest delivered directly to their Telegram chat.

**What problem it solves**: Keeping up with the rapidly evolving AI/ML landscape is overwhelming. This bot automates the aggregation and summarization of AI news from 16+ sources, delivering a curated daily brief that saves users hours of manual scanning.

**Why it exists**: The AI/ML field moves too fast for manual tracking. This bot provides a single point of access to all major AI news sources, with intelligent summarization and categorized delivery via Telegram.

*Note: The reliability-first architecture and multi-source aggregation approach are explicitly documented in the README and code. The target user profile is inferred from the bot's feature set and command structure.*

---

## 2. Tech Stack & Core Technologies

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Language | Python | 3.11+ | Primary language |
| Telegram SDK | python-telegram-bot | ≥22.8 | Bot framework and Telegram API integration |
| Task Scheduler | APScheduler | ≥3.11.3 | Scheduled auto-broadcast (2-hour interval) |
| RSS Parsing | feedparser | ≥6.0.14 | News RSS feed parsing |
| HTML Parsing | BeautifulSoup4 | ≥4.15.0 | Web scraping and HTML content extraction |
| HTTP Client | httpx | ≥0.28.1 | Async HTTP requests for API calls |
| Sync HTTP | requests | ≥2.34.2 | Synchronous HTTP requests |
| XML Parser | lxml | ≥6.1.1 | Fast XML/HTML parsing backend |
| AI Summarization | Google Gemini API | ≥0.8.6 | Optional AI-powered article summarization |
| Environment | python-dotenv | ≥1.2.2 | .env file loading |
| Caching | diskcache | — | Local disk-based caching (inferred from requirements) |
| Containerization | Docker | — | Multi-stage builds (prod/dev) |
| CI/CD | GitHub Actions | — | Lint, test, security scans |

---

## 3. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Telegram Platform                                 │
│  ┌──────────┐    ┌──────────────┐    ┌────────────────────────┐    │
│  │  User    │───▶│  Bot API     │───▶│  long-polling worker   │    │
│  │ Commands │    │ (send/recv)  │    │  (python-telegram-bot) │    │
│  └──────────┘    └──────────────┘    └───────────▲────────────┘    │
└─────────────────────────────────────────────────┼───────────────────┘
                                                  │
                                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    AI Telegram News Bot                              │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  run_bot.py — Application Entry Point                        │   │
│  │  • Registers 18 command handlers                             │   │
│  │  • Sets up message handler for free-text queries              │   │
│  │  • Configures APScheduler for 2-hour auto-broadcast           │   │
│  │  • Retry logic: 5 attempts with exponential backoff          │   │
│  └───────────────────────┬──────────────────────────────────────┘   │
│                          │                                          │
│                          ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Report Generator (services/report_generator.py)              │   │
│  │  • Routes commands to appropriate scraper                     │   │
│  │  • Formats output for Telegram (Markdown)                     │   │
│  │  • Handles compare, roadmap, leaderboard features             │   │
│  └───────────────────────┬──────────────────────────────────────┘   │
│                          │                                          │
│                          ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Scrapers (16+ sources across 6 modules)                      │   │
│  │                                                                │   │
│  │  news_scraper.py      — AI news RSS feeds                     │   │
│  │  github_scraper.py    — GitHub trending repos                  │   │
│  │  twitter_scraper.py   — AI posts from X/Twitter               │   │
│  │  ai_features_scraper.py — AI tools, startups, models          │   │
│  │  indian_news_scraper.py — India-focused AI news               │   │
│  │  extended_scrapers.py — YouTube, blogs, jobs, learning        │   │
│  │  async_base_scraper.py — Async HTTP base class                │   │
│  │  fallback_data.py     — Curated fallback content              │   │
│  └───────────────────────┬──────────────────────────────────────┘   │
│                          │                                          │
│                          ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Utilities                                                    │   │
│  │                                                                │   │
│  │  cache_manager.py   — diskcache wrapper for source caching    │   │
│  │  logger.py          — Structured logging setup                │   │
│  │  telegram_utils.py  — Message splitting, formatting           │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Services                                                     │   │
│  │                                                                │   │
│  │  scheduler.py       — APScheduler for auto-broadcast          │   │
│  │  summarizer.py      — Gemini AI article summarization         │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

**Architectural Pattern**: **Pipeline/Scraper Pattern** with a **Reliability Layer**. The system follows a simple request-response pattern where Telegram commands trigger scraping pipelines, with a multi-tier fallback system (live → cached → curated fallback).

The pattern is justified by: the `run_bot.py` entry point routes commands to `ReportGenerator`, which orchestrates scrapers, which fetch from external sources with graceful degradation.

---

## 4. Complete Folder Structure Tree

```
AI-Telegram-News-Bot/
├── .dockerignore                    # Docker build context exclusions
├── .editorconfig                    # Editor configuration
├── .env.example                     # Environment variable template
├── .gitattributes                   # Git attributes
├── .github/
│   ├── CODEOWNERS                   # Code ownership
│   ├── copilot-instructions.md      # AI assistant instructions
│   ├── dependabot.yml               # Dependency update automation
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md            # Bug report template
│   │   └── feature_request.md       # Feature request template
│   ├── labeler.yml                  # Auto-labeling config
│   ├── PULL_REQUEST_TEMPLATE.md     # PR template
│   └── workflows/
│       ├── ci.yml                   # CI pipeline
│       ├── codeql.yml               # Code security analysis
│       ├── gitleaks.yml             # Secret detection
│       ├── labeler.yml              # Label automation
│       ├── maintenance.yml          # Maintenance tasks
│       ├── stale.yml                # Stale issue management
│       └── welcome.yml              # New contributor welcome
├── .gitignore                       # Git ignore rules
├── .vscode/
│   └── settings.json                # VS Code settings
├── AGENTS.md                        # AI agent instructions
├── config/
│   ├── __init__.py
│   └── config.py                    # Configuration (env vars, feed URLs)
├── docker-compose.dev.yml           # Docker Compose dev overrides
├── docker-compose.prod.yml          # Docker Compose production overrides
├── docker-compose.yml               # Docker Compose base definition
├── Dockerfile                       # Multi-stage Docker build
├── docs/
│   ├── community/
│   │   ├── CHANGELOG.md             # Release notes
│   │   ├── CODE_OF_CONDUCT.md       # Community guidelines
│   │   ├── CONTRIBUTING.md          # Contribution guide
│   │   ├── SECURITY.md              # Security policy
│   │   └── SUPPORT.md               # Support information
│   ├── design/
│   │   ├── AppFlow.md               # Application flow
│   │   └── Design.md                # System design
│   ├── product/
│   │   └── PRD.md                   # Product requirements
│   ├── project/
│   │   ├── ImplementationPlan.md    # Implementation roadmap
│   │   ├── RiskRegister.md          # Risk assessment
│   │   ├── Rules.md                 # Project rules
│   │   └── Tracker.md               # Progress tracker
│   ├── reference/
│   │   └── Glossary.md              # Domain terminology
│   └── technical/
│       ├── API.md                   # API documentation
│       ├── Deployment.md            # Deployment guide
│       ├── Schema.md                # Data schema
│       ├── SecurityAndCompliance.md # Security notes
│       ├── TechSpec.md              # Technical spec
│       └── Testing.md               # Testing docs
├── get_chat_id.py                   # Utility to get Telegram chat ID
├── LICENSE                          # MIT License
├── list_models.py                   # List available AI models
├── Makefile                         # Convenience commands
├── Procfile                         # Heroku/Railway deployment
├── PROJECT_ANALYSIS.md              # Repository audit
├── PROJECT_OVERVIEW.md              # This file
├── pyproject.toml                   # Python tool config
├── railway.json                     # Railway deployment config
├── README.md                        # Project README
├── render.yaml                      # Render deployment config
├── requirements.txt                 # Python dependencies
├── runtime.txt                      # Python runtime version
├── run_bot.py                       # Bot entry point
├── scrapers/
│   ├── __init__.py
│   ├── ai_features_scraper.py       # AI tools, startups, models
│   ├── async_base_scraper.py        # Async HTTP base class
│   ├── extended_scrapers.py         # YouTube, blogs, jobs, learning
│   ├── fallback_data.py             # Curated fallback content
│   ├── github_scraper.py            # GitHub trending repos
│   ├── indian_news_scraper.py       # India-focused AI news
│   ├── news_scraper.py              # AI news RSS feeds
│   └── twitter_scraper.py           # AI posts from X/Twitter
├── services/
│   ├── __init__.py
│   ├── report_generator.py          # Report generation & routing
│   ├── scheduler.py                 # APScheduler auto-broadcast
│   └── summarizer.py                # Gemini AI summarization
├── StartBot.ps1                     # Windows PowerShell start script
├── start_bot.bat                    # Windows batch start script
├── tests/
│   ├── __init__.py
│   ├── test_all_commands.py         # Command test suite
│   ├── test_all_scrapers.py         # Scraper test suite
│   ├── test_bot_logic.py            # Bot logic tests
│   ├── test_indian_scraper.py       # Indian scraper tests
│   └── test_twitter.py              # Twitter scraper tests
├── utils/
│   ├── __init__.py
│   ├── cache_manager.py             # Disk cache management
│   ├── logger.py                    # Structured logging
│   └── telegram_utils.py            # Telegram message utilities
├── scripts/
│   ├── verify_async_scrapers.py     # Async scraper verification
│   └── verify_fixes.py              # Fix verification script
```

---

## 5. Exhaustive File-by-File & Folder-by-Folder Breakdown

### Root Files

#### `AI-Telegram-News-Bot/run_bot.py`
- **File type**: Python script (entry point)
- **Purpose**: Main bot entry point. Registers all command handlers, sets up APScheduler for auto-broadcast, and starts Telegram long-polling.
- **Key exports**: `main()` function
- **Key functions**:
  - `start_command(update, context)` — Welcome message with command overview
  - `help_command(update, context)` — Displays help (delegates to start_command)
  - `daily_command(update, context)` — Full daily intelligence report
  - `summary_command(update, context)` — AI-powered news summary via Gemini
  - `compare_command(update, context)` — Compare AI models (GPT-4o vs Claude vs Gemini)
  - `roadmap_command(update, context)` — AI learning path generation
  - `leaderboard_command(update, context)` — Top AI models ranked
  - `generic_command(update, context, category)` — Routes to report generator
  - `handle_message(update, context)` — Free-text message routing
  - `make_broadcast_callback(app, chat_id, loop_holder)` — Creates scheduler callback
  - `main()` — Application setup, handler registration, scheduler init
- **Important logic**:
  - Registers 18 BotCommand entries for Telegram menu
  - Auto-broadcast every 2 hours via APScheduler
  - Retry logic: 5 attempts with exponential backoff (10s * 2^(attempt-1))
  - Free-text messages are keyword-matched to commands
  - Cleanup on shutdown: `post_stop` callback
- **Side effects**: Connects to Telegram API, starts long-polling, runs scheduler
- **Dependencies**: `config.config.Config`, `services.report_generator.ReportGenerator`, `services.scheduler.SchedulerService`, `services.summarizer.Summarizer`, `utils.logger`, `utils.telegram_utils`

#### `AI-Telegram-News-Bot/get_chat_id.py`
- **File type**: Python script
- **Purpose**: Utility to retrieve a Telegram chat ID by sending a message and reading the response.

#### `AI-Telegram-News-Bot/list_models.py`
- **File type**: Python script
- **Purpose**: Lists available AI models for comparison features.

#### `AI-Telegram-News-Bot/scripts/verify_async_scrapers.py`
- **File type**: Python script
- **Purpose**: Verification script for async scraper functionality.

#### `AI-Telegram-News-Bot/scripts/verify_fixes.py`
- **File type**: Python script
- **Purpose**: Verification script for recent fixes.

---

### `AI-Telegram-News-Bot/config/` — Configuration Module

#### `AI-Telegram-News-Bot/config/config.py`
- **File type**: Python module
- **Purpose**: Centralized configuration loading from environment variables and `.env` file.
- **Key exports**: `Config` class
- **Configuration values** (inferred from .env.example):
  - `TELEGRAM_BOT_TOKEN` — Required. Bot token from BotFather
  - `TELEGRAM_CHAT_ID` — Optional. For scheduled broadcasts
  - `GEMINI_API_KEY` — Optional. For AI-powered summaries
- **Dependencies**: `python-dotenv`

---

### `AI-Telegram-News-Bot/scrapers/` — News Source Scrapers

#### `AI-Telegram-News-Bot/scrapers/__init__.py`
- **File type**: Python package marker

#### `AI-Telegram-News-Bot/scrapers/async_base_scraper.py`
- **File type**: Python module
- **Purpose**: Base class for async HTTP scrapers. Provides common HTTP client setup, error handling, and retry logic.

#### `AI-Telegram-News-Bot/scrapers/news_scraper.py`
- **File type**: Python module
- **Purpose**: Scrapes AI/ML news from RSS feeds and news websites.
- **Key exports**: `NewsScraper` class with `fetch_news(count)` method

#### `AI-Telegram-News-Bot/scrapers/github_scraper.py`
- **File type**: Python module
- **Purpose**: Scrapes GitHub trending repositories in AI/ML categories.
- **Key exports**: `GitHubScraper` class

#### `AI-Telegram-News-Bot/scrapers/twitter_scraper.py`
- **File type**: Python module
- **Purpose**: Scrapes curated AI posts from X/Twitter without API access.
- **Key exports**: `TwitterScraper` class

#### `AI-Telegram-News-Bot/scrapers/ai_features_scraper.py`
- **File type**: Python module
- **Purpose**: Scrapes AI tools, startups, model releases, and comparison data.
- **Key exports**: `AIFeaturesScraper` class

#### `AI-Telegram-News-Bot/scrapers/indian_news_scraper.py`
- **File type**: Python module
- **Purpose**: Scrapes India-focused AI/ML news sources.
- **Key exports**: `IndianNewsScraper` class

#### `AI-Telegram-News-Bot/scrapers/extended_scrapers.py`
- **File type**: Python module
- **Purpose**: Scrapes YouTube AI content, blog posts, job listings, and learning resources.
- **Key exports**: Multiple scraper classes for different content types

#### `AI-Telegram-News-Bot/scrapers/fallback_data.py`
- **File type**: Python module
- **Purpose**: Provides curated fallback content when live sources fail. Contains pre-written AI news items, tool descriptions, and model information.
- **Key exports**: Fallback data dictionaries/lists

---

### `AI-Telegram-News-Bot/services/` — Service Layer

#### `AI-Telegram-News-Bot/services/__init__.py`
- **File type**: Python package marker

#### `AI-Telegram-News-Bot/services/report_generator.py`
- **File type**: Python module
- **Purpose**: Central orchestrator that routes commands to appropriate scrapers and formats output for Telegram.
- **Key exports**: `ReportGenerator` class
- **Key methods**:
  - `generate_report(category)` — Main report generation
  - `generate_compare(query)` — AI model comparison
  - `generate_roadmap(role)` — Learning path generation
  - `generate_leaderboard(filter_term)` — Model leaderboard
  - `cleanup()` — Cleanup resources

#### `AI-Telegram-News-Bot/services/scheduler.py`
- **File type**: Python module
- **Purpose**: APScheduler-based service for periodic auto-broadcast of AI news.
- **Key exports**: `SchedulerService` class
- **Key methods**:
  - `start()` — Start the scheduler with 2-hour interval

#### `AI-Telegram-News-Bot/services/summarizer.py`
- **File type**: Python module
- **Purpose**: Gemini AI-powered article summarization. Optional feature that uses Google's Gemini API to generate concise summaries of news articles.
- **Key exports**: `Summarizer` class
- **Key methods**:
  - `summarize_articles(articles)` — Summarize a list of articles

---

### `AI-Telegram-News-Bot/utils/` — Utility Modules

#### `AI-Telegram-News-Bot/utils/__init__.py`
- **File type**: Python package marker

#### `AI-Telegram-News-Bot/utils/cache_manager.py`
- **File type**: Python module
- **Purpose**: Disk-based caching wrapper (likely using `diskcache`) to persist scraped data between runs.

#### `AI-Telegram-News-Bot/utils/logger.py`
- **File type**: Python module
- **Purpose**: Structured logging setup with configurable levels and formatters.
- **Key exports**: `setup_logger(name)` function

#### `AI-Telegram-News-Bot/utils/telegram_utils.py`
- **File type**: Python module
- **Purpose**: Telegram message utilities including message splitting for oversized messages and Markdown formatting helpers.
- **Key exports**: `send_split_message(update, text)` function

---

### `AI-Telegram-News-Bot/tests/` — Test Files

| File | Purpose |
|------|---------|
| `test_all_commands.py` | Tests all bot command handlers |
| `test_all_scrapers.py` | Tests all scraper modules |
| `test_bot_logic.py` | Tests bot routing and logic |
| `test_indian_scraper.py` | Tests Indian news scraper specifically |
| `test_twitter.py` | Tests Twitter scraper specifically |

**Note**: Tests use `pytest-asyncio` for async test support. The PROJECT_ANALYSIS.md shows test failures due to missing `pytest-asyncio` plugin configuration.

---

### `AI-Telegram-News-Bot/docker-compose.yml` (inferred)
- **Purpose**: Docker Compose definition for running the bot in containers.

#### `AI-Telegram-News-Bot/Dockerfile`
- **File type**: Dockerfile (multi-stage)
- **Purpose**: Multi-stage build with `prod` and `dev` targets.
- **Key details**: Based on `python:3.13-slim`, uses tini for PID-1, non-root `botuser`, healthcheck via process scanning, volume for SQLite cache at `/app/data`.
- **Build targets**: `prod` (default), `dev` (adds pytest, flake8)

---

### `AI-Telegram-News-Bot/docs/` — Documentation

| Path | Purpose |
|------|---------|
| `docs/community/CHANGELOG.md` | Release notes |
| `docs/community/CODE_OF_CONDUCT.md` | Community guidelines |
| `docs/community/CONTRIBUTING.md` | Contribution guide |
| `docs/community/SECURITY.md` | Security policy |
| `docs/community/SUPPORT.md` | Support information |
| `docs/design/AppFlow.md` | Application flow diagrams |
| `docs/design/Design.md` | System design document |
| `docs/product/PRD.md` | Product requirements |
| `docs/project/ImplementationPlan.md` | Implementation roadmap |
| `docs/project/RiskRegister.md` | Risk assessment |
| `docs/project/Rules.md` | Project conventions |
| `docs/project/Tracker.md` | Progress tracking |
| `docs/reference/Glossary.md` | Domain terminology |
| `docs/technical/API.md` | API documentation |
| `docs/technical/Deployment.md` | Deployment guide |
| `docs/technical/Schema.md` | Data schema |
| `docs/technical/SecurityAndCompliance.md` | Security notes |
| `docs/technical/TechSpec.md` | Technical specification |
| `docs/technical/Testing.md` | Testing documentation |

---

## 6. Data Models & Schemas

### News Article (Inferred)

```python
{
    "title": str,           # Article headline
    "url": str,             # Source URL
    "summary": str,         # Brief description
    "source": str,          # Source name (e.g., "TechCrunch", "arXiv")
    "published": datetime,  # Publication date
    "category": str,        # Category (news, paper, tool, etc.)
}
```

### Telegram Bot Command

```python
BotCommand(
    command="daily",           # Command name
    description="Full daily intelligence report"  # Help text
)
```

### Cached Data

- Stored on disk via `diskcache` (SQLite-backed)
- Key: source identifier + date
- Value: Serialized article list
- TTL: Likely 2-4 hours (matching auto-broadcast interval)

---

## 7. API Surface

This bot does not expose a REST API. It operates as a **Telegram Bot** with command-based interaction.

### Telegram Commands

| Command | Description | Handler |
|---------|-------------|---------|
| `/start` | Welcome message and command overview | `start_command` |
| `/help` | Display help information | `help_command` |
| `/daily` | Full daily intelligence report | `daily_command` |
| `/summary` | AI-powered news summary (Gemini) | `summary_command` |
| `/news` | Global AI news | `generic_command("news")` |
| `/papers` | Latest AI research papers | `generic_command("papers")` |
| `/blogs` | AI blog updates | `generic_command("blogs")` |
| `/tools` | Trending AI tools | `generic_command("tools")` |
| `/jobs` | AI job opportunities | `generic_command("jobs")` |
| `/startups` | Startup and funding updates | `generic_command("startups")` |
| `/models` | Model release updates | `generic_command("models")` |
| `/trending` | AI community trends | `generic_command("trending")` |
| `/learn` | AI learning resources | `generic_command("learn")` |
| `/india` | India-focused AI news | `generic_command("india")` |
| `/youtube` | AI YouTube updates | `generic_command("youtube")` |
| `/twitter` | Curated AI posts from X | `generic_command("twitter")` |
| `/compare` | Compare AI models | `compare_command` |
| `/roadmap` | AI learning paths | `roadmap_command` |
| `/leaderboard` | Top AI models ranked | `leaderboard_command` |

### Free-Text Message Handling

The bot also handles free-text messages via keyword matching:
- "summary" → summary command
- "daily"/"report" → daily command
- "tool" → tools command
- "job" → jobs command
- "leaderboard" → leaderboard command
- "compare"/"vs" → compare command
- "roadmap" → roadmap command
- "news" → news command
- "youtube"/"video" → youtube command
- "twitter"/"x"/"tweet" → twitter command

---

## 8. Configuration & Environment Variables

| Variable | Purpose | Default | Required | Consumed By | Example |
|----------|---------|---------|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from BotFather | `""` | **Yes** | `config/config.py` → `run_bot.py` | `"123456789:ABCdefGHIjklMNOpqrSTUvwxYZ"` |
| `TELEGRAM_CHAT_ID` | Default chat ID for auto-broadcast | `""` | No (disables auto-broadcast) | `config/config.py` → `run_bot.py` | `"-1001234567890"` |
| `GEMINI_API_KEY` | Google Gemini API key for summaries | `""` | No (disables /summary) | `config/config.py` → `services/summarizer.py` | `"AIzaSy..."` |

---

## 9. Build, Run & Deployment Instructions

### Prerequisites

- Python 3.11+
- Telegram bot token from @BotFather
- (Optional) Google Gemini API key for AI summaries

### Local Development

```bash
# 1. Clone and setup
git clone https://github.com/themanoj-025/ai_daily_telegram_bot.git
cd ai_daily_telegram_bot
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your Telegram bot token

# 4. Run the bot
python run_bot.py
```

### Docker

```bash
# Build and run
docker compose up --build

# Or with Docker directly
docker build -t ai-news-bot .
docker run -e TELEGRAM_BOT_TOKEN=your_token ai-news-bot
```

### Deployment Platforms

- **Render**: `render.yaml` included
- **Railway**: `railway.json` included
- **Heroku**: `Procfile` included

### Running Tests

```bash
# Note: Requires pytest-asyncio for async test support
pip install pytest pytest-asyncio
python tests/test_all_commands.py
python tests/test_all_scrapers.py
python tests/test_indian_scraper.py
```

---

## 10. Data & Control Flow Walkthroughs

### Flow 1: User Sends `/daily` Command

1. User sends `/daily` in Telegram
2. `run_bot.py` receives update via long-polling
3. `daily_command()` is called
4. Sends "Fetching updates..." reply
5. `report_generator.generate_report("all")` is called
6. ReportGenerator orchestrates multiple scrapers:
   - `NewsScraper.fetch_news()` — RSS feeds
   - `GitHubScraper.fetch_trending()` — GitHub trending
   - `AIFeaturesScraper.fetch_tools()` — AI tools
   - `IndianNewsScraper.fetch_news()` — Indian news
   - (and more for each category)
7. Each scraper: checks cache → if miss, fetches live → falls back to curated data
8. ReportGenerator formats combined output as Markdown
9. `send_split_message()` sends the report (splitting if >4096 chars)
10. User receives the daily AI intelligence brief

### Flow 2: Auto-Broadcast (Every 2 Hours)

1. APScheduler triggers `broadcast_callback` every 2 hours
2. Callback runs in scheduler thread, uses `asyncio.run_coroutine_threadsafe` to run async code on the bot's event loop
3. `report_generator.generate_report("all", force_refresh=True)` generates fresh content
4. Report is sent to the configured `TELEGRAM_CHAT_ID`
5. If `TELEGRAM_CHAT_ID` is not set, auto-broadcast is skipped

### Flow 3: Source Failure Fallback

1. Scraper attempts live fetch from source (e.g., RSS feed)
2. Request fails (network error, rate limit, etc.)
3. Scraper checks disk cache for recent data
4. If cache hit: returns cached data
5. If cache miss: returns curated fallback data from `fallback_data.py`
6. User receives content without knowing the source failed

---

## 11. Dependency Graph Summary

### Internal Module Dependencies

```
run_bot.py
  ├── config/config.py
  ├── services/report_generator.py
  │   ├── scrapers/news_scraper.py
  │   ├── scrapers/github_scraper.py
  │   ├── scrapers/twitter_scraper.py
  │   ├── scrapers/ai_features_scraper.py
  │   ├── scrapers/indian_news_scraper.py
  │   ├── scrapers/extended_scrapers.py
  │   ├── scrapers/async_base_scraper.py
  │   └── scrapers/fallback_data.py
  ├── services/scheduler.py
  ├── services/summarizer.py
  │   └── (google-generativeai)
  ├── utils/logger.py
  └── utils/telegram_utils.py
      └── utils/cache_manager.py
```

### External Package Purposes

| Package | Purpose | Used By |
|---------|---------|---------|
| `python-telegram-bot` | Telegram Bot API framework | `run_bot.py` |
| `feedparser` | RSS feed parsing | `scrapers/news_scraper.py` |
| `beautifulsoup4` | HTML parsing | `scrapers/*.py` |
| `lxml` | Fast XML/HTML parser | `scrapers/*.py` |
| `httpx` | Async HTTP client | `scrapers/async_base_scraper.py` |
| `requests` | Sync HTTP client | `scrapers/*.py` |
| `apscheduler` | Task scheduling | `services/scheduler.py` |
| `google-generativeai` | Gemini API client | `services/summarizer.py` |
| `python-dotenv` | .env loading | `config/config.py` |

---

## 12. Testing Strategy

### Test Types

| File | Type | Coverage |
|------|------|----------|
| `test_all_commands.py` | Integration | All 18 bot command handlers |
| `test_all_scrapers.py` | Unit | All scraper modules |
| `test_bot_logic.py` | Unit | Bot routing and logic |
| `test_indian_scraper.py` | Unit | Indian news scraper |
| `test_twitter.py` | Unit | Twitter scraper |

### Known Issues

- Tests require `pytest-asyncio` plugin for async function support
- Current test configuration doesn't include the async plugin, causing failures

---

## 13. Known Issues, Technical Debt & Assumptions

### Known Issues

1. **Test failures**: All async tests fail because `pytest-asyncio` is not configured in `pyproject.toml`. The test scripts now live in `tests/` (v6 restructure) and remain runnable as CLI scripts (`python tests/test_*.py`); converting them to a pytest suite with `pytest-asyncio` is a deferred follow-up.
2. **Python 3.13 in Dockerfile**: The Dockerfile uses `python:3.13-slim` but `runtime.txt` and `requirements.txt` target Python 3.11.

### Technical Debt

1. **No data persistence layer**: News data is only cached to disk; there's no database for historical tracking.
2. **Hardcoded feed URLs**: RSS feed URLs are likely hardcoded in scraper modules.
3. **No rate limiting on scrapers**: Multiple scrapers hitting the same sources could trigger rate limits.
4. **Telegram message length limit**: Messages are split at 4000 chars, but this could lose formatting.

### Assumptions

1. **Telegram bot is pre-created**: The bot must be created via @BotFather before running.
2. **Network access**: Scrapers require internet access to fetch live data.
3. **Disk writable**: The bot needs writable disk for caching (SQLite via diskcache).
4. **Gemini API optional**: The `/summary` command requires a Gemini API key, but the bot works without it.

---

## 14. Glossary

| Term | Definition |
|------|-----------|
| **Auto-broadcast** | Scheduled delivery of AI news to a configured chat every 2 hours |
| **BotFather** | Telegram's official bot for creating and managing bots |
| **Long-polling** | Telegram's method for receiving updates (vs. webhooks) |
| **Scraper** | Module that fetches data from external sources (RSS, web, API) |
| **Fallback data** | Curated content served when live sources fail |
| **diskcache** | Python library for disk-based caching using SQLite |
| **APScheduler** | Advanced Python Scheduler for periodic tasks |
| **Gemini** | Google's AI model used for article summarization |

---

## 15. Appendix

### Deployment Configurations

- **`render.yaml`**: Render platform deployment config
- **`railway.json`**: Railway platform deployment config
- **`Procfile`**: Heroku deployment config

### Windows Scripts

- **`StartBot.ps1`**: PowerShell script to start the bot on Windows
- **`start_bot.bat`**: Batch script to start the bot on Windows

### `.github/workflows/`

| Workflow | Purpose |
|----------|---------|
| `ci.yml` | Main CI pipeline (lint, test, security) |
| `codeql.yml` | GitHub CodeQL security analysis |
| `gitleaks.yml` | Secret detection in code |
| `labeler.yml` | Auto-label PRs based on changed files |
| `maintenance.yml` | Automated maintenance tasks |
| `stale.yml` | Mark and close stale issues/PRs |
| `welcome.yml` | Welcome new contributors |

---

*This document was generated as part of a comprehensive project documentation effort. Last updated: August 8, 2026.*
