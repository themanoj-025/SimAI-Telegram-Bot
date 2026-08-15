# Startup Flow — AI-Telegram-News-Bot

## 1. Bot Boot

```
python run_bot.py              # Docker CMD / Procfile worker / Railway / Render
│
├─ 1. config/config.py loads env (TELEGRAM_BOT_TOKEN, channel IDs, RSS registries)
├─ 2. utils/logger configured
├─ 3. Telegram bot client initialized (python-telegram-bot)
├─ 4. Command handlers registered (via services/report_generator.py routing)
├─ 5. APScheduler started — 2-hour broadcast job (services/scheduler.py)
│      → scrapes → optional Gemini summary (services/summarizer.py)
│      → caches via utils/cache_manager.py (6h TTL)
└─ 6. Polling loop active (bot ready to serve commands)
```

## 2. Command Flow

1. User sends a command (e.g. `/news`, `/today`).
2. `run_bot.py` dispatches to `services/report_generator.py`.
3. Report generator calls the relevant `scrapers/*` (with cache checks).
4. Content formatted via `utils/telegram_utils.py` (split + markdown) and sent.

## 3. Scheduled Broadcast Flow

1. `services/scheduler.py` fires every 2 hours.
2. Scrapers fetch content (fallback to `scrapers/fallback_data.py` on failure).
3. `services/summarizer.py` optionally summarizes via Gemini.
4. Broadcast posted to the configured channel.

## 4. Docker / Deploy

- **Dockerfile** (prod/dev): `COPY run_bot.py` + modules; `CMD ["python",
  "run_bot.py"]`; liveness probe checks the `run_bot.py` process.
- **Procfile**: `worker: python run_bot.py` (Heroku-style).
- **railway.json** / **render.yaml**: `python run_bot.py` start command.
- **start_bot.bat** / **StartBot.ps1**: local Windows launchers.

## 5. CI (push/PR)

`ci.yml`: py_compile sweep → CLI test/verify scripts
(`python tests/test_all_scrapers.py`, `python tests/test_bot_logic.py`,
`python scripts/verify_async_scrapers.py` — each tolerant of network-dependent
steps) → Bandit → lychee → Docker build + Trivy. File-presence check for deploy
artifacts (`run_bot.py`, `Procfile`, `railway.json`, `render.yaml`, ...).

## 6. Failure Modes

| Failure | Behavior |
| --- | --- |
| Live scraper fails | Falls back to cached content or `fallback_data.py` (reliability tier) |
| Gemini API unavailable | Summarizer skipped; raw content broadcast instead |
| Cache miss + network down | Fallback content used |
| Bot token invalid | Boot fails loudly at startup |
