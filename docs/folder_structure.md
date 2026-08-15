# Folder Structure — AI Daily Telegram Bot

Canonical layout after the v5.0 modernization pass. The structure follows the
target architecture ("adapt, don't force-fit"): one root entry point, a
small layered package (`config` / `scrapers` / `services` / `utils`), and a
docs suite.

## 1. Current tree (canonical)

```
AI-Telegram-News-Bot/
├── run_bot.py                      # ENTRY POINT: Telegram bot + scheduler
├── config/
│   ├── __init__.py
│   └── config.py                   # env config + curated RSS/YouTube registry
├── scrapers/
│   ├── __init__.py
│   ├── async_base_scraper.py       # async HTTP base (httpx)
│   ├── news_scraper.py             # RSS news feeds
│   ├── github_scraper.py           # GitHub trending
│   ├── twitter_scraper.py          # curated X/Twitter posts
│   ├── ai_features_scraper.py      # tools, startups, models, compare
│   ├── indian_news_scraper.py      # India-focused AI news
│   ├── extended_scrapers.py        # YouTube, blogs, jobs, learning
│   └── fallback_data.py            # curated offline content (reliability tier)
├── services/
│   ├── __init__.py
│   ├── report_generator.py         # command routing + formatting
│   ├── scheduler.py                # 2-hour APScheduler broadcast
│   └── summarizer.py               # Gemini summaries (optional)
├── utils/
│   ├── __init__.py
│   ├── cache_manager.py            # diskcache wrapper (6h TTL)
│   ├── logger.py                   # structured logging
│   └── telegram_utils.py           # message split + markdown helpers
├── tests/                          # CLI test scripts (moved from root, v6)
│   ├── test_all_commands.py        #   command-suite test script
│   ├── test_all_scrapers.py        #   scraper-suite test script
│   ├── test_bot_logic.py           #   bot-logic test script
│   ├── test_indian_scraper.py      #   Indian scraper test script
│   └── test_twitter.py             #   Twitter scraper test script
├── scripts/                        # operational verification tools (v6)
│   ├── verify_async_scrapers.py    #   async verification script
│   └── verify_fixes.py             #   fix verification script
├── get_chat_id.py                  # dev utility: resolve chat ID
├── list_models.py                  # dev utility: list AI models
├── docs/                           # documentation suite (see §2)
├── .github/                        # CI + community workflows & templates
├── Dockerfile                      # multi-stage (prod/dev)
├── docker-compose.yml  docker-compose.dev.yml  docker-compose.prod.yml
├── Makefile  Procfile  railway.json  render.yaml  runtime.txt
├── pyproject.toml  requirements.txt
├── README.md  PROJECT_OVERVIEW.md  PROJECT_ANALYSIS.md  AGENTS.md
├── StartBot.ps1  start_bot.bat
└── .env.example  .gitignore  .dockerignore  .editorconfig  .gitattributes  .vscode/
```

## 2. Docs tree

```
docs/
├── architecture.md · folder_structure.md · module_dependency.md
├── startup_flow.md · package_overview.md
├── migration/
│   ├── migration_summary.md       # ← v5.0 pass report (moved here, v6)
│   ├── old_tree_to_new_tree.md    # ← v6 restructure
│   └── file_move_ledger.md        # ← v6 restructure
├── community/   (CHANGELOG, CODE_OF_CONDUCT, CONTRIBUTING, SECURITY, SUPPORT)
├── design/      (AppFlow, Design)
├── product/     (PRD)
├── project/     (ImplementationPlan, RiskRegister, Rules, Tracker,
│                 analysis_report.md ← this pass)
├── reference/   (Glossary)
└── technical/   (API, Deployment, Schema, SecurityAndCompliance, TechSpec, Testing)
```

## 3. Change log (this pass)

| Old path | New path | Reason | Mechanism |
|---|---|---|---|
| `ai-daily-telegram-bot/` (3 files) | *removed* | First-commit bootstrap leftover; root `.gitignore`/`LICENSE`/`.gitattributes` are canonical; zero code/CI/Docker references | `git rm -r` |
| `AGENTS_FIX.md` | *removed* | Leftover v7.0 prompt scaffolding (16-repo duplicate); not referenced by code/CI/Docker | `git rm` |
| — | `docs/project/analysis_report.md` | Required Phase 1–2 artifact | added |
| — | `docs/architecture.md` | Required Phase 9 artifact | added |
| — | `docs/folder_structure.md` | Required Phase 9 artifact | added |
| — | `docs/migration_summary.md` | Required Phase 9 artifact | added |
| `docs/migration_summary.md` | `docs/migration/migration_summary.md` | v6: consolidate migration records under `docs/migration/` | `git mv` |
| `test_*.py` (5 files) | `tests/` | v6: canonical test home (realizes §5 recommendation) | `git mv` |
| `verify_*.py` (2 files) | `scripts/` | v6: operational verification tools (realizes §5 recommendation) | `git mv` |
| — | `docs/module_dependency.md`, `docs/startup_flow.md`, `docs/package_overview.md` | v6: Phase 6 deliverables | added |
| — | `docs/migration/old_tree_to_new_tree.md`, `docs/migration/file_move_ledger.md` | v6: Phase 6 deliverables | added |

Reference updates: `.dockerignore` (dropped `AGENTS_FIX.md` exclusion);
`PROJECT_OVERVIEW.md` (dropped `AGENTS_FIX.md` + the `ai-daily-telegram-bot/`
subtree from the tree listing).

## 4. Root allowlist compliance

| Root entry | Status |
|---|---|
| `run_bot.py` | ✔ entry point |
| `Dockerfile`, `docker-compose*.yml`, `Procfile`, `railway.json`, `render.yaml`, `runtime.txt` | ✔ container/deploy tooling |
| `Makefile`, `pyproject.toml`, `requirements.txt` | ✔ standard metadata |
| `README.md`, `PROJECT_OVERVIEW.md`, `PROJECT_ANALYSIS.md`, `AGENTS.md` | ✔ metadata / docs |
| `config/`, `scrapers/`, `services/`, `utils/`, `docs/`, `.github/` | ✔ top-level folders |
| `tests/`, `scripts/` | ✔ tests + operational verification scripts (moved from root in v6; CI paths updated to `tests/` and `scripts/`) |
| `get_chat_id.py`, `list_models.py` | ✔ dev utilities (flagged in analysis §6.4) |
| `StartBot.ps1`, `start_bot.bat` | ✔ platform scripts |
| `.env.example`, `.gitignore`, `.dockerignore`, `.editorconfig`, `.gitattributes`, `.vscode/` | ✔ config / metadata |

Result: **no stray files remain at root** — the bootstrap leftover folder and
the AI-prompt scaffold were removed; everything else is entry points,
metadata, tooling, or folders.

## 5. Why not more restructuring?

The package is already clean, layered, and acyclic; the target architecture's
`domain/repositories` subpackages would be an over-fit for ~15 small modules.
Two improvements were deferred in v5.0 because they change CI/test contracts:
moving the root test scripts into `tests/` and relocating the dev utilities into
`scripts/`. The **v6 restructure performed both relocations** (via `git mv`, with
CI paths updated) while preserving the scripts as runnable CLI tools. Still
deferred: converting the CLI test scripts to a `pytest` suite with
`pytest-asyncio` wiring (a test-refactor, out of scope for a structural move) —
see the follow-up backlog.
