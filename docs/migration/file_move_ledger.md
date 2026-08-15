# File Move Ledger — AI-Telegram-News-Bot

Restructure date: **2026-08-11** (v6) · Method: `git mv` · Branch: `main`
(local commits, no push).

## Moved Files

| # | Old Path | New Path | Category | Reason | Risk | Verified? |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `test_all_commands.py` | `tests/test_all_commands.py` | Test → `tests/` | Canonical test home (realizes v5.0 §5 recommendation) | Low (CWD bootstrap present) | ✅ runs from root |
| 2 | `test_all_scrapers.py` | `tests/test_all_scrapers.py` | Test → `tests/` | Same | Low | ✅ CI path updated |
| 3 | `test_bot_logic.py` | `tests/test_bot_logic.py` | Test → `tests/` | Same | Low | ✅ CI path updated |
| 4 | `test_indian_scraper.py` | `tests/test_indian_scraper.py` | Test → `tests/` | Same | Low | ✅ |
| 5 | `test_twitter.py` | `tests/test_twitter.py` | Test → `tests/` | Same | Low | ✅ |
| 6 | `verify_async_scrapers.py` | `scripts/verify_async_scrapers.py` | Script → `scripts/` | Operational verification tool (v5.0 §6 recommendation) | Low | ✅ CI path updated |
| 7 | `verify_fixes.py` | `scripts/verify_fixes.py` | Script → `scripts/` | Same | Low | ✅ |
| 8 | `docs/migration_summary.md` | `docs/migration/migration_summary.md` | Meta → Docs | Consolidate migration records | Low (0 refs) | ✅ |

## New Files

| Path | Reason |
| --- | --- |
| `tests/__init__.py` | Package marker (future pytest conversion + tidy layout). |
| `docs/module_dependency.md`, `docs/startup_flow.md`, `docs/package_overview.md` | Phase 6 deliverables. |
| `docs/migration/old_tree_to_new_tree.md`, `docs/migration/file_move_ledger.md` | Phase 6 deliverables. |

## Files Updated (reference paths)

| Path | Changes |
| --- | --- |
| `.github/workflows/ci.yml` | Test/verify script paths → `tests/` + `scripts/` (3 lines). |
| `.github/copilot-instructions.md` | 2 command paths. |
| `.github/PULL_REQUEST_TEMPLATE.md` | 3 checkbox paths. |
| `docs/community/CONTRIBUTING.md` | 3 command paths. |
| `docs/folder_structure.md` | Tree (tests/, scripts/), docs tree, change log, allowlist, §5. |

## Files Deliberately NOT MOVED (contract analysis)

| Path | Why it stays | Risk if moved |
| --- | --- | --- |
| `run_bot.py` | Entry — Docker CMD, Procfile, railway.json, render.yaml, liveness probe | High |
| `config/` `scrapers/` `services/` `utils/` | Importable top-level modules; ~25 internal imports + CI import checks | High (no benefit — flat-module layout is canonical for bots) |
| `get_chat_id.py` / `list_models.py` | Dev utilities; referenced by docs/CI file-presence check | Low |
| `ai_daily_bot.log`, `bot_cache.db` | Untracked + gitignored runtime artifacts — out of scope | — |

## Flagged (follow-up backlog)

| Item | Flag |
| --- | --- |
| Convert CLI test scripts to a `pytest` suite (`pytest-asyncio` for scrapers) | Deferred by design (test refactor, not structural). |
| `test_indian_scraper.py` / `test_twitter.py` / `verify_fixes.py` not wired into CI | Pre-existing — consider adding to the CI test matrix. |
| `get_chat_id.py` / `list_models.py` → `scripts/` | Cosmetic; root dev utilities are acceptable, but a future `scripts/dev/` home is an option. |

## Deletions

None in this restructure.
