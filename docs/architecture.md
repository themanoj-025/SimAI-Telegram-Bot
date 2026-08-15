# Architecture — AI Daily Telegram Bot

A concise, current map of how the AI-Telegram-News-Bot is built. The code
remains the source of truth; this is the canonical architecture reference
produced during the v5.0 modernization pass.

## 1. System at a glance

A Telegram bot that aggregates AI/ML news from 30+ curated sources (RSS,
arXiv, GitHub trending, X/Twitter, Indian outlets, YouTube channels), with
optional Gemini-powered summarization, a model-comparison feature, and a
2-hour scheduled auto-broadcast. A **reliability-first** design means every
fetch degrades gracefully: live source → disk cache → curated fallback — the
bot never fails silently.

## 2. Layered model

```
┌──────────────────────────────────────────────────────────────────────┐
│  Interface                                                           │
│   run_bot.py — 18 command handlers + free-text keyword router +      │
│               APScheduler auto-broadcast + 5× retry bootstrap        │
├──────────────────────────────────────────────────────────────────────┤
│  Application                                                         │
│   services/report_generator.py — command → scraper routing,          │
│               Telegram markdown formatting, compare/roadmap/         │
│               leaderboard generation                                 │
│   services/summarizer.py      — Gemini article summarization (opt.)  │
│   services/scheduler.py       — 2-hour broadcast loop                │
├──────────────────────────────────────────────────────────────────────┤
│  Domain / Data access (scrapers)                                     │
│   news_scraper · github_scraper · twitter_scraper ·                  │
│   ai_features_scraper · indian_news_scraper · extended_scrapers      │
│   async_base_scraper (httpx base) · fallback_data (curated tier)     │
├──────────────────────────────────────────────────────────────────────┤
│  Cross-cutting (utils)                                               │
│   cache_manager (diskcache, 6h TTL) · logger · telegram_utils        │
├──────────────────────────────────────────────────────────────────────┤
│  Configuration                                                       │
│   config/config.py — env vars + 30+ curated RSS/YouTube sources      │
└──────────────────────────────────────────────────────────────────────┘
```

Dependencies flow strictly downward and are acyclic: `run_bot` → services →
scrapers → config/utils.

## 3. Runtime flows

### 3.1 User command (`/daily`, `/news`, …)
1. Telegram delivers the update via long-polling to `run_bot.py`.
2. The matching `CommandHandler` (or the free-text keyword router) fires.
3. `report_generator.generate_report(category)`:
   - picks the scraper(s) for the category,
   - each scraper tries **live fetch → cache → fallback_data**,
   - results are formatted as Markdown,
4. `send_split_message` chunks the reply (4000 chars) to respect Telegram's
   limit.

### 3.2 Auto-broadcast (every 2 h)
1. `SchedulerService.start()` schedules the refresh callback.
2. Callback runs on a scheduler thread and hops onto the bot's event loop via
   `asyncio.run_coroutine_threadsafe`.
3. A fresh `"all"` report is generated with `force_refresh=True` and sent to
   `TELEGRAM_CHAT_ID`; skipped (with a warning) if the chat ID is unset.

### 3.3 Reliability tiers
```
Live source ──fail──▶ disk cache ──miss──▶ curated fallback_data
   (httpx/feedparser)   (6h TTL)            (always available)
```

### 3.4 Crash resilience
`run_bot.py` wraps `main()` in a 5-attempt loop with exponential backoff
(10 s · 2^(attempt−1)), exiting only on `SystemExit`/`KeyboardInterrupt` or
after the final attempt.

## 4. Configuration surface

| Env var | Purpose | Required |
|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | Yes |
| `TELEGRAM_CHAT_ID` | Auto-broadcast target; unset disables broadcast | No |
| `GEMINI_API_KEY` | `/summary` (Gemini); unset degrades feature | No |

Module constants: `CACHE_EXPIRY_HOURS=6`, `ARTICLES_PER_SECTION=5`,
`REQUEST_TIMEOUT=60`, `MAX_RETRIES=3`, `LOG_FILE=ai_daily_bot.log`.

## 5. Persistence

| Artifact | Location | Note |
|---|---|---|
| Scrape cache | `bot_cache.db` (diskcache, SQLite) | gitignored; TTL 6h; recreated on demand |
| Log | `ai_daily_bot.log` | gitignored |

## 6. Deployment

- **Docker**: multi-stage image (`prod` default, `dev` adds pytest/flake8),
  `python:3.13-slim` base (see analysis §6.2 for the 3.11/3.13 note), tini as
  PID 1, non-root `botuser`, cache volume at `/app/data`.
- **Compose**: base + dev/prod overrides.
- **PaaS**: Render (`render.yaml`), Railway (`railway.json`), Heroku
  (`Procfile`, `runtime.txt`).
- **CI** (`.github/workflows/ci.yml`): lint (flake8), syntax (`py_compile`),
  test (root script suites), link-check, deploy-file verification, Docker
  build + vulnerability scan. Auxiliary workflows: codeql, gitleaks, labeler,
  stale, welcome, maintenance.

## 7. Key design decisions

1. **Reliability-first** — the live → cache → curated ladder guarantees output
   under any network failure; the fallback tier is fully offline.
2. **Everything is a scraper** — one routing surface (`report_generator`)
   over uniform scraper interfaces keeps command handlers tiny.
3. **Scheduler thread-safety** — broadcast uses
   `run_coroutine_threadsafe` so the APScheduler thread never touches the
   bot's event loop directly.
4. **Config as source registry** — feed/channel lists live in
   `config/config.py` (candidates for externalization, see analysis §6.3).
5. **Crash self-healing** — the 5-attempt exponential-backoff bootstrap keeps
   a transient token/network failure from killing the bot permanently.
