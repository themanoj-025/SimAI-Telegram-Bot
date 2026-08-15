# Security Policy for AI-Telegram-News-Bot

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it privately. We do not have a dedicated security team, but we will respond to and address reported vulnerabilities as quickly as possible.

**How to report:**
- Open a private security advisory on GitHub (if this repository is public).
- Email **manojjana.0025@gmail.com** directly. This contact is also listed in our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- If neither channel works, open a standard issue with the label `security` and avoid including exploit details in public view.

**Expectations:**
- We will acknowledge receipt within 5 business days.
- We will provide an initial assessment and expected fix timeline within 10 business days.
- We ask that you do not publicly disclose the vulnerability until we have released a fix.

## Security Measures

### Implemented
- **Token isolation:** The Telegram bot token and Gemini API key are stored as environment variables, never hardcoded in source code.
- **No user data storage:** The bot does not store personally identifiable information (PII). It only caches scraped article content locally via `diskcache`.
- **API key isolation:** Gemini API key is loaded from environment variables only.
- **Error resilience:** Individual scraper failures do not crash the bot; they are logged and skipped.

### Not Implemented
- **No authentication layer:** The bot posts to configured Telegram chats — there is no user-facing authentication.
- **No rate limiting:** The bot does not implement rate limiting on outbound requests.
- **No input sanitization:** Not applicable since the bot is not user-facing.
- **No webhook mode:** The bot uses long-polling (not webhooks), which is less secure at scale.

## Dependencies

This project relies on several third-party packages (see `requirements.txt`). While we keep dependencies updated, you should periodically audit them for known vulnerabilities:

```bash
pip-audit -r requirements.txt
```

Key dependencies to watch:
- `python-telegram-bot` — Telegram API client (keep updated for API changes)
- `google-generativeai` — Google Gemini API client
- `diskcache`, `beautifulsoup4`, `feedparser`, `aiohttp`, `httpx`, `requests`

## Environment Security

The following environment variables should be kept secret and never committed:
- `TELEGRAM_BOT_TOKEN` — Controls access to your Telegram bot
- `GEMINI_API_KEY` — Controls access to your Gemini API billing

Rotate these keys immediately if they are accidentally exposed.

## Deployment Security

- **Railway/Render:** Secrets are managed through the platform's environment variable system.
- **Long-polling:** The bot uses polling rather than webhooks. Ensure the bot token has appropriate permissions.
- **Production:** Before deploying to production, review the `Procfile` and platform configurations to ensure no secrets are exposed.
