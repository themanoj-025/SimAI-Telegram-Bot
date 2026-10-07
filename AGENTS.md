# AGENTS.md — AI-Telegram-News-Bot

> Canonical project instructions. Pointers like `CLAUDE.md` or
> `.github/copilot-instructions.md` should say "See AGENTS.md".

---

## Project overview

**AI-Telegram-News-Bot** — a Telegram news aggregation bot that fetches
top headlines from multiple news APIs and delivers them to users via
Telegram. Core components:

- **Bot** (`run_bot.py`) — py-tgbot polling loop, command dispatch.
- **Scheduler** (`services/scheduler.py`) — periodic headline refresh.
- **Cache** (`utils/cache.py`) — Redis + SQLite cache for dedup/TTL.
- **LLM gateway** (`services/llm_gateway.py`) — optional headline
  summarisation.
- **Health server** (`health_server.py`) — `/healthz` + `/readyz`.

Stack: Python 3.11+ · Telebot · requests/httpx · redis · sqlite3.

---

## Exact commands

```bash
# Install
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Env
cp .env.example .env   # set TELEGRAM_TOKEN, NEWS_API_KEY, REDIS_URL

# Lint / typecheck / test
make lint
pre-commit run --all-files
python -m mypy . --ignore-missing-imports
python -m pytest tests/ -v --cov=. --cov-fail-under=70

# Run
python run_bot.py
```

---

## Folder map

| Path | Purpose |
|------|---------|
| `bot/` | Telegram bot commands and handlers |
| `services/` | Scheduler, LLM gateway, cache, queue |
| `utils/` | Cache helpers, logging, config |
| `tests/` | pytest suite (unit + integration) |
| `.github/workflows/` | CI (ruff, mypy, pytest, gitleaks, trivy) |

## Do / don't

- **Do** keep the cache layer behind an interface so the Redis backend
  is swappable with SQLite.
- **Do not** commit `secrets/` or `*.pem` — the `.gitignore` enforces it.
- **Do not** call the LLM gateway without the activity logger attached.

## Security rules

- No secrets in the repository; `gitleaks` CI gate is exit-code `1` on hit.
- Rate-limit the bot's API calls per chat to avoid abuse.

## AI-assistance convention

Commits authored by AI must carry the trailer:

```text
AI-Assisted: yes | no | partial
```

See `.gitmessage` for the template. Do not rewrite historic commits
retroactively.
