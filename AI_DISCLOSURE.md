# ✦ AI Assistance Disclosure

## Summary

AI-Telegram-News-Bot was built with substantial AI assistance. The core
architecture — the Telegram bot polling loop, the scheduler, the cache,
and the LLM gateway — was drafted end-to-end by AI. Human maintainers
then reviewed every design decision, tightened the security posture, and
wrote the tests and documentation by hand.

## Tools & Models Used

| Tool | Provider / Model | Interface | Approx. dates used |
|---|---|---|---|
| **Claude / Opus** | Anthropic | CLI agent + web chat | 2025-11 → 2026-09 |
| **Cursor** | Anthropic (via IDE) | IDE agent | 2026-03 → 2026-09 |
| **GitHub Copilot** | GitHub | IDE completion | 2025-11 → 2026-09 |

## Scope — What AI Did vs. What Humans Did

- **AI:**
  - First draft of the bot command handlers and message pipeline
  - Scaffolding for the scheduler, cache, and LLM gateway
  - Initial drafts of `README.md`, `CONTRIBUTING.md`, and the design docs
- **Human:**
  - All architecture decisions (command set, cache strategy, LLM usage)
  - Security review — threat modelling, secrets handling, rate limiting
  - All production tests, CI workflows, and the Dockerfile
  - The open-source stewardship

## Estimated AI-Assisted Share

Roughly **60–75% of lines in `bot/`, `services/`, and `utils/`** follow
AI-generated boilerplate. The business logic, security controls, and
tests are mostly human-authored. This is an estimate, not a measured
statistic — the exact ratio was never instrumented.

## Human Review Process

- Every PR is reviewed line-by-line by the maintainer.
- Security review by maintainer: secrets handling, rate limiting,
  payload validation, and gitleaks/bandit findings.
- Automated gates: pre-commit (ruff + mypy), pytest (≥ 70% coverage
  floor), gitleaks, trivy, and an AI-disclosure metadata check.

## Known Limitations & Risks

- **LLM hallucination:** the bot can summarise a headline incorrectly.
  The LLM gateway guards this with an offline deterministic fallback.
- **API-rate-limit drift:** Telegram and the news APIs both have
  rate limits; the scheduler respects `Retry-After` headers.
- **License-contamination risk:** upstream training data may contain code
  copies. The CI gitleaks/bandit gates catch obvious secrets.

## How to Verify

- `git log --all --oneline --grep="assistant\|ai\|gen"` and the
  `Co-authored-by:` trailers in recent commits.
- `cat docs/audit/*` — per-repo audit reports.
- `git log --all --oneline --grep="ai-assisted\|LLM\|llm"` — the commit
  history trail.

## Last Updated

2026-10-06 · Maintained by `themanoj-025 <code.me.025@gmail.com>`
