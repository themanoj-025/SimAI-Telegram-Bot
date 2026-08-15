# Package Overview — AI-Telegram-News-Bot

Inventory of every module (post-restructure).

## 1. Entry Point

| Module | Responsibility | Entry point |
| --- | --- | --- |
| `run_bot.py` | Telegram bot + 2-hour scheduler bootstrap; command routing. | `python run_bot.py` (Docker, Procfile, Railway, Render) |

## 2. Modules (`config/`, `scrapers/`, `services/`, `utils/`)

| Module | Responsibility |
| --- | --- |
| `config/config.py` | Env config + curated RSS/YouTube registry. |
| `scrapers/async_base_scraper.py` | Async HTTP base (httpx). |
| `scrapers/news_scraper.py` | RSS news feeds. |
| `scrapers/github_scraper.py` | GitHub trending. |
| `scrapers/twitter_scraper.py` | Curated X/Twitter posts. |
| `scrapers/ai_features_scraper.py` | Tools, startups, models, compare. |
| `scrapers/indian_news_scraper.py` | India-focused AI news. |
| `scrapers/extended_scrapers.py` | YouTube, blogs, jobs, learning. |
| `scrapers/fallback_data.py` | Curated offline content (reliability tier). |
| `services/report_generator.py` | Command routing + formatting. |
| `services/scheduler.py` | 2-hour APScheduler broadcast. |
| `services/summarizer.py` | Gemini summaries (optional). |
| `utils/cache_manager.py` | diskcache wrapper (6h TTL). |
| `utils/logger.py` | Structured logging. |
| `utils/telegram_utils.py` | Message split + markdown helpers. |

## 3. Tests (`tests/` — moved from root, v6)

| Module | Responsibility |
| --- | --- |
| `tests/test_all_commands.py` | Command-suite test script. |
| `tests/test_all_scrapers.py` | Scraper-suite test script (CI-invoked). |
| `tests/test_bot_logic.py` | Bot-logic test script (CI-invoked). |
| `tests/test_indian_scraper.py` | Indian scraper test script. |
| `tests/test_twitter.py` | Twitter scraper test script. |

## 4. Operational Scripts (`scripts/` — moved from root, v6)

| Module | Responsibility |
| --- | --- |
| `scripts/verify_async_scrapers.py` | Async scraper verification (CI-invoked). |
| `scripts/verify_fixes.py` | Fix verification tool. |

## 5. Dev Utilities (root)

| Module | Responsibility |
| --- | --- |
| `get_chat_id.py` | Resolve a chat ID (dev aid). |
| `list_models.py` | List available AI models (dev aid). |
| `start_bot.bat` / `StartBot.ps1` | Local Windows launchers. |

## 6. Deploy & Infra

`Dockerfile`, `docker-compose*.yml`, `Makefile`, `Procfile`, `railway.json`,
`render.yaml`, `runtime.txt`, `.github/workflows/ci.yml`.

## 7. Documentation (`docs/`)

Root suite: `architecture.md`, `folder_structure.md`, `module_dependency.md`,
`startup_flow.md`, `package_overview.md`. Migration records: `migration/`.
Categorized: `community/`, `design/`, `product/`, `project/`, `reference/`,
`technical/`.

## 8. Test Coverage

CLI test/verify scripts (not pytest) — CI invokes them directly with network
tolerance. Converting to a pytest suite is a deferred follow-up (see ledger).
