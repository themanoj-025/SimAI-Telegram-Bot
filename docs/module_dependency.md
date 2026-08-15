# Module Dependency — AI-Telegram-News-Bot

**No circular imports.** Graph is acyclic: entry point → services/scrapers → utils →
config.

## 1. Dependency Graph

```
  run_bot.py (entry — Telegram bot + 2-hour scheduler)
       │
       ├──► services/report_generator.py  ──► scrapers/* ──► utils/logger
       ├──► services/scheduler.py         ──► services/summarizer.py
       │                                        │
       │                                        ▼
       │                              utils/cache_manager.py (diskcache, 6h TTL)
       ▼
  utils/telegram_utils.py · utils/logger.py · config/config.py (leaf)
```

## 2. Dependency Matrix

| Module | Imports | Consumed by |
| --- | --- | --- |
| `run_bot.py` | `config`, `services.*` | `python run_bot.py` (Docker CMD, Procfile, Railway, Render) |
| `services/report_generator.py` | `scrapers.*`, `utils.*` | `run_bot.py` (command routing + formatting) |
| `services/scheduler.py` | `utils.cache_manager`, `services.summarizer` | `run_bot.py` (APScheduler broadcast) |
| `services/summarizer.py` | `utils.*`, LLM SDK (Gemini) | `services/scheduler.py` |
| `scrapers/*.py` | `utils.cache_manager`, `utils.logger`, `config` | `services/report_generator.py` |
| `utils/cache_manager.py` | diskcache | scrapers, scheduler |
| `utils/telegram_utils.py` | python-telegram-bot | `run_bot.py` |
| `utils/logger.py` | stdlib | everything |
| `config/config.py` | env (pydantic/dotenv) | everything (leaf) |
| `tests/test_*.py` | root modules via `sys.path.append(os.getcwd())` | CI (`python tests/test_*.py`) |
| `scripts/verify_*.py` | root modules | CI (`python scripts/verify_*.py`) |

## 3. Why This Shape

- **Entry → services → scrapers layering**: the bot entry only orchestrates; all
  content acquisition lives in `scrapers/`, formatting in `services/`, and shared
  plumbing in `utils/`.
- **Reliability tiering**: `scrapers/fallback_data.py` provides curated offline
  content — a leaf that keeps the bot functional when live scrapers fail.
- **CWD-based imports for test/verify scripts**: scripts in `tests/`/`scripts/` are
  invoked from the repo root and bootstrap `sys.path.append(os.getcwd())`, so their
  `from scrapers...` / `from services...` imports resolve regardless of location.

## 4. Change Warnings

- **Renaming a `scrapers/` module** breaks `report_generator.py` + the corresponding
  test script — grep first.
- **The scheduler and summarizer** must stay decoupled (scheduler never imports
  scraper internals directly).
- Keep `config/config.py` env-key names frozen — every module reads them (protocol
  constraint).
