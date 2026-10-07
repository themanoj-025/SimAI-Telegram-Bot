# 🗂 AI Conversation Transcripts

> This directory holds **sanitized** conversation exports that materially
> shaped AI-Telegram-News-Bot's design. They are here for human and
> automated auditing.

## Redaction policy

Every export in this directory must have the following categories removed:

| Category | Removal method |
|---|---|
| API keys, tokens, credentials | Strip; use dummy values or `***REDACTED***` |
| Internal hostnames / IP addresses | Replace with `REDACTED-ORIGIN` |
| Private URLs | Replace with `https://example.internal/` |
| Email addresses / phone numbers | Remove the address entirely |
| Secrets inside file contents | Use a clearly-marked placeholder (never a real-looking key) |
| Raw prompt/response pairs | Keep only the sanitized transcript; the raw `.raw.json` export is ignored by `.gitignore` |

## What to include vs. exclude

- ✅ **Include:** a summary of the conversation, the key prompts and
  outcomes, any decisions that this transcript influenced.
- ❌ **Exclude:** any real credential, internal hostname, private URL,
  personal data, or unredacted API key.

## How to add a new transcript

1. Export your conversation from your AI tool of choice.
2. Sanitize it (see the policy above) with a script or manually.
3. Place the sanitized file in this directory, named like
   `YYYY-MM-DD-<session-name>.md` or `.json`.
4. Write a one-line `.md` summary in this same directory naming the files.
5. Run `git check-ignore -v docs/ai/transcripts/<file>` to confirm it is
   **not** ignored — this directory is tracked.

## Tools used

| Tool | Provider | Model | Interface |
|---|---|---|---|
| Claude | Anthropic | Opus / Sonnet | CLI agent + IDE |
| Cursor | Anysphere | Model 5 | IDE agent |

---

## Verification

```bash
# 1. Confirm every file here is tracked
ls -1 docs/ai/transcripts/ 2>/dev/null | wc -l

# 2. Confirm none are ignored by .gitignore
git check-ignore -v docs/ai/transcripts/*.md 2>/dev/null || echo "no transcripts tracked yet"
```
