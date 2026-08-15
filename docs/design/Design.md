# Design — AI Daily Telegram Bot: Message Design & UX

| Field | Value |
| --- | --- |
| Version | v0.1 |
| Last Updated | 2026-08-06 |
| Owner | Design Lead |
| Status | In Review |

---

## 1. Design Principles

1. **Scan-first** — headlines + links, no walls of text.
2. **Consistent structure** — every digest uses the same section headers.
3. **Reliability over flashiness** — formatting must never crash the bot.
4. **Honest sourcing** — each item shows its source.
5. **Efficient** — short summaries; full article is one tap away.

## 2. Brand & Visual Identity

- Voice: concise, informative, neutral.
- No custom images in v1; Telegram Markdown for emphasis.

## 3. Color System

N/A — Telegram client renders colors; we use Markdown bold/italics only.

## 4. Typography

N/A — Telegram native rendering. Use `*bold*` for section headers and item titles.

## 5. Spacing & Structure

- One section header line, then numbered items.
- Each item: `Title` (bold) + link + one-line summary.
- Digest ends with source attribution + timestamp.

## 6. Component Library

**Digest message anatomy (ASCII):**

```
*🤖 AI Daily Brief — 2026-08-06*
──────────────────────────
*1. NEWS*
1. [Title](url) — one-line summary
2. [Title](url) — one-line summary
──────────────────────────
*2. PAPERS*
...
*Sources: GitHub Trending · arXiv · X*
_Generated in 12.4s_
```

States: generating (typing), success (message), failure (error text).

## 7. Iconography

Emojis only (🤖 📰 📄 etc.) — native Unicode, no images.

## 8. Accessibility

- Plain Markdown renders in all Telegram clients.
- No color-only signaling (bold is the emphasis mechanism).

## 9. Responsive Behavior

N/A — Telegram handles all device sizes.

## 10. Motion & Micro-interactions

None in v1 (Telegram typing indicator only).

## 11. Dark Mode / Theming

N/A — client-managed.

## 12. Related Documents

| Document | Relationship |
| --- | --- |
| [AppFlow.md](AppFlow.md) | SCR-003…017 consume these formats |
| [PRD.md](../product/PRD.md) | UX requirements |
| [TechSpec.md](../technical/TechSpec.md) | Formatter component |
| [Schema.md](../technical/Schema.md) | Item fields |
| [ImplementationPlan.md](../project/ImplementationPlan.md) | Tasks |
| [Tracker.md](../project/Tracker.md) | Status |
| [Rules.md](../project/Rules.md) | Standards |
| [API.md](../technical/API.md) | Telegram message API |
| [SecurityAndCompliance.md](../technical/SecurityAndCompliance.md) | Secrets |
| [Testing.md](../technical/Testing.md) | Format tests |
| [Deployment.md](../technical/Deployment.md) | Deploy |
| [Glossary.md](../reference/Glossary.md) | Vocabulary |
| [RiskRegister.md](../project/RiskRegister.md) | Risks |
