# Old Tree → New Tree — AI-Telegram-News-Bot

Restructure performed **2026-08-11** (v6, Principal Architect protocol). Realizes the
relocations the v5.0 pass deliberately deferred (root test/verify scripts →
`tests/` + `scripts/`), consolidates migration records, and completes the Phase 6
documentation suite. **No business-logic or entry-point changes.**

## Before (2026-08-10)

```
AI-Telegram-News-Bot/
├── run_bot.py
├── config/ · scrapers/ · services/ · utils/
├── test_all_commands.py · test_all_scrapers.py · test_bot_logic.py      ← root
├── test_indian_scraper.py · test_twitter.py · verify_async_scrapers.py  ← root
├── verify_fixes.py                                                      ← root
├── get_chat_id.py · list_models.py · start_bot.bat · StartBot.ps1
├── docs/
│   ├── architecture.md · folder_structure.md · migration_summary.md
│   ├── community/ design/ product/ project/ reference/ technical/
├── .github/workflows/ · .vscode/
├── Dockerfile · docker-compose*.yml · Makefile · Procfile · railway.json · render.yaml
├── pyproject.toml · requirements.txt · runtime.txt
├── README.md · PROJECT_OVERVIEW.md · PROJECT_ANALYSIS.md · AGENTS.md
└── .gitignore · .dockerignore · .editorconfig · .gitattributes
```

## After (2026-08-11)

```
AI-Telegram-News-Bot/
├── run_bot.py                     (unchanged — entry contract)
├── config/ · scrapers/ · services/ · utils/   (unchanged)
├── tests/                         (NEW — 5 CLI test scripts moved here)
│   ├── test_all_commands.py · test_all_scrapers.py · test_bot_logic.py
│   └── test_indian_scraper.py · test_twitter.py
├── scripts/                       (NEW — 2 verification tools moved here)
│   ├── verify_async_scrapers.py · verify_fixes.py
├── get_chat_id.py · list_models.py · start_bot.bat · StartBot.ps1 (unchanged)
├── docs/
│   ├── architecture.md · folder_structure.md (kept + updated)
│   ├── module_dependency.md       (NEW)
│   ├── startup_flow.md            (NEW)
│   ├── package_overview.md        (NEW)
│   ├── migration/
│   │   ├── migration_summary.md   (MOVED from docs/)
│   │   ├── old_tree_to_new_tree.md (NEW — this file)
│   │   └── file_move_ledger.md    (NEW)
│   ├── community/ design/ product/ project/ reference/ technical/ (unchanged)
├── .github/workflows/ · .vscode/  (unchanged)
├── Dockerfile · docker-compose*.yml · Makefile · Procfile · railway.json · render.yaml (unchanged)
├── pyproject.toml · requirements.txt · runtime.txt   (unchanged)
├── README.md · PROJECT_OVERVIEW.md · PROJECT_ANALYSIS.md · AGENTS.md   (unchanged)
└── .gitignore · .dockerignore · .editorconfig · .gitattributes         (unchanged)
```

## Summary

| Kind | Count |
| --- | --- |
| Files moved (`git mv`) | 8 (5 test → `tests/`, 2 verify → `scripts/`, 1 migration record → `docs/migration/`) |
| New files | 6 (`tests/__init__.py` + 5 docs) |
| Docs updated | `folder_structure.md`, `CONTRIBUTING.md`, `ci.yml`, `copilot-instructions.md`, `PULL_REQUEST_TEMPLATE.md` |
| Business logic changed | 0 |
| Entry points changed | 0 (`run_bot.py` untouched) |
| Deleted | 0 |
