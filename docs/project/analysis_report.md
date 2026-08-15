# Analysis Report — Repository Inventory & Classification

Date: 2026-08-10 · Scope: entire AI-Telegram-News-Bot repository · Method:
file-by-file read + import-graph scan + content-hash duplicate scan +
reference scan.

This report is the written inventory required by Phase 1–2 of the repository
modernization pass (v5.0). It lists every top-level entry, its purpose, its
classification, and its intra-package dependencies. Nothing here changes
behavior — it is the evidence base for the restructuring documented in
[`docs/migration/migration_summary.md`](../migration/migration_summary.md).

---

## 1. Stack overview

| Dimension | Value |
|---|---|
| Language / runtime | Python ≥ 3.11 (image 3.13-slim — see §6 finding) |
| Package manager | `requirements.txt` (pip) + `pyproject.toml` (tool config only) |
| Application | Telegram bot (long-polling) via python-telegram-bot |
| Scheduler | APScheduler — 2-hour auto-broadcast |
| AI layer | Google Gemini summarization (optional) |
| Caching | `diskcache` (SQLite-backed) — live → cache → curated-fallback |
| Lint / test | flake8 (CI) · script-based tests at repo root (CI runs `python test_*.py`) |
| CI | GitHub Actions `ci.yml` + codeql, gitleaks, labeler, stale, welcome, maintenance |
| Deploy | Docker multi-stage (prod/dev) · Render (`render.yaml`) · Railway (`railway.json`) · Heroku (`Procfile`) |

## 2. Top-level inventory (root)

| Path | Purpose | Classification |
|---|---|---|
| `run_bot.py` | Bot entry point: 18 command handlers, scheduler, retry loop | Entry point |
| `config/config.py` | Env config + RSS feed registry (30+ curated sources) | Configuration |
| `scrapers/` | 8 scraper modules + fallback data (news, github, twitter, india, extended, ai_features, async base) | Domain / Data access |
| `services/` | `report_generator`, `scheduler`, `summarizer` | Application |
| `utils/` | `cache_manager`, `logger`, `telegram_utils` | Cross-cutting |
| `test_*.py` (5) + `verify_*.py` (2) | Script-style test/verification suites (root-level) | Tests |
| `get_chat_id.py`, `list_models.py` | Dev utilities | Tools |
| `docs/` | Documentation suite (community/design/product/project/reference/technical) | Docs |
| `.github/` | CI + community workflows, templates, CODEOWNERS, dependabot | Infrastructure |
| `Dockerfile`, `docker-compose*.yml` | Multi-stage image + dev/prod compose | Infrastructure |
| `Makefile`, `Procfile`, `railway.json`, `render.yaml`, `runtime.txt` | Build/deploy tooling | Infrastructure |
| `README.md`, `PROJECT_OVERVIEW.md`, `PROJECT_ANALYSIS.md`, `AGENTS.md` | Metadata / docs | Docs |
| `AGENTS_FIX.md` | **Leftover AI-prompt scaffolding (v7.0)** — removed this pass | Unclassified → removed |
| `ai-daily-telegram-bot/` | **Bootstrap leftover folder** (3 stale files) — removed this pass | Unclassified → removed |
| `StartBot.ps1`, `start_bot.bat` | Windows start scripts | Tools |
| `.env.example`, `.gitignore`, `.dockerignore`, `.editorconfig`, `.gitattributes`, `.vscode/` | Config / metadata | Configuration |

## 3. Package modules (domain & application)

| Module | Purpose | Depends on (intra-package) | Classification |
|---|---|---|---|
| `config/config.py` | Env config + RSS/YouTube source registry | — (leaf) | Configuration |
| `scrapers/async_base_scraper.py` | Async HTTP base class (httpx) | `config` | Data access |
| `scrapers/news_scraper.py` | RSS feed parsing (feedparser) | `async_base_scraper`, `fallback_data` | Data access |
| `scrapers/github_scraper.py` | GitHub trending | `async_base_scraper` | Data access |
| `scrapers/twitter_scraper.py` | Curated X/Twitter posts | — | Data access |
| `scrapers/ai_features_scraper.py` | Tools, startups, models, compare, leaderboard | `async_base_scraper` | Data access |
| `scrapers/indian_news_scraper.py` | India-focused news (IndiaAI, ET, IE, Inc42, NDTV…) | `async_base_scraper` | Data access |
| `scrapers/extended_scrapers.py` | YouTube, blogs, jobs, learning | `async_base_scraper` | Data access |
| `scrapers/fallback_data.py` | Curated offline content (reliability tier 3) | — (leaf) | Domain |
| `services/report_generator.py` | Command → scraper routing + Telegram formatting + compare/roadmap/leaderboard | all scrapers | Application |
| `services/scheduler.py` | APScheduler 2-hour broadcast | — | Infrastructure |
| `services/summarizer.py` | Gemini article summarization | `config` | Application |
| `utils/cache_manager.py` | diskcache wrapper (TTL 6h) | — | Cross-cutting |
| `utils/logger.py` | `setup_logger` with file + console | `config` | Cross-cutting |
| `utils/telegram_utils.py` | Message splitting, markdown | — | Cross-cutting |
| `run_bot.py` | Handlers, free-text router, retry (5× exp backoff) | config, services, utils | Entry point / API |

Graph is **acyclic**: `run_bot` → services → scrapers → `config`/utils.

## 4. Documentation suite

| Path | Purpose |
|---|---|
| `docs/community/` | CHANGELOG, CODE_OF_CONDUCT, CONTRIBUTING, SECURITY, SUPPORT |
| `docs/design/` | AppFlow, Design |
| `docs/product/` | PRD |
| `docs/project/` | ImplementationPlan, RiskRegister, Rules, Tracker (+ this report) |
| `docs/reference/` | Glossary |
| `docs/technical/` | API, Deployment, Schema, SecurityAndCompliance, TechSpec, Testing |

## 5. Findings summary (evidence for Phase 3)

| Scan | Method | Result |
|---|---|---|
| Duplicate folders | tree scan | **`ai-daily-telegram-bot/` removed** — first-commit bootstrap leftover: 3 files (`.gitattributes`, `.gitignore`, `LICENSE`) all differing from root versions; root `.gitignore`/`LICENSE` are canonical; no code, CI, Docker, or config references (only a stale line in `PROJECT_OVERVIEW.md` tree, updated) |
| Duplicate files | SHA-256 content hash | 0 duplicate-content groups among remaining files |
| Empty files | size == 0 walk | none |
| AI scaffolding | `AGENTS_FIX.md` (identical v7.0 prompt in 16 sibling repos) | **removed** — not referenced by code/CI/Docker (only `.dockerignore` exclusion + `PROJECT_OVERVIEW.md` tree line, both updated) |
| Hardcoded secrets | regex scan | none — env-backed (`TELEGRAM_BOT_TOKEN`, `GEMINI_API_KEY`) |
| Unused deps | import scan vs `requirements.txt` | all 9 pinned deps used; `diskcache` is imported by `cache_manager` |
| Tests | CI invocation `python test_*.py` | script-based; see §6 items 1–2 |

## 6. Needs Human Review

1. **Test layout mismatch** — `pyproject.toml` declares `testpaths = ["tests"]`
   and pytest-asyncio is *not* configured, but the actual suites are
   root-level `test_*.py` scripts invoked directly by CI (`python
   test_all_scrapers.py`, etc.). Async tests therefore fail under pytest and
   CI tolerates failures with `|| echo`. Recommend: move suites to `tests/`,
   add `pytest-asyncio` to `requirements.txt` + `[tool.pytest.ini_options]`,
   and make CI fail on real test failure.
2. **Python version mismatch** — Dockerfile uses `python:3.13-slim` while
   `runtime.txt` and the project target 3.11. Harmless today (code runs on
   both) but should be reconciled deliberately.
3. **`DATABASE_URL`-style unused config** — `config.py` hardcodes 30+
   YouTube channel IDs and RSS feeds; consider externalizing to a data file
   so the config module stays env-only.
4. **`get_chat_id.py` / `list_models.py` / `verify_fixes.py`** — dev-only
   utilities at root; candidates for `scripts/` if kept (no reference
   changes needed — they are never imported).
