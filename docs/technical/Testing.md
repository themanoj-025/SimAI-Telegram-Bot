# Testing — AI Daily Telegram Bot: Test Strategy

| Field | Value |
| --- | --- |
| Version | v0.1 |
| Last Updated | 2026-08-06 |
| Owner | QA Engineer |
| Status | In Review |

---

## 1. Test Pyramid

```mermaid
graph TD
    E2E[E2E: live bot smoke (real Telegram)]
    INT[Integration: command pipeline with mocked sources]
    UNIT[Unit: parsers, splitting, cache, format]
```

## 2. Strategy

| Layer | Tool | Scope |
| --- | --- | --- |
| Unit | pytest | Parser edge cases, message splitting, cache TTL, sanitization |
| Integration | pytest + mock HTTP | Command → report with stubbed scrapers; fallback path |
| E2E | Manual scripts | `test_all_commands.py`, `test_all_scrapers.py`, `test_indian_scraper.py` |

> Note: async tests currently fail without `pytest-asyncio` — see PROJECT_ANALYSIS.md. Add `pytest-asyncio` as dev dependency and re-run.

## 3. Critical Test Cases

| ID | Feature | Case | Expected |
| --- | --- | --- | --- |
| TC-001 | Splitting | 10,000-char digest | Parts ≤ 4096 chars, order preserved |
| TC-002 | Fallback | All sources fail | Curated fallback served, never empty |
| TC-003 | Cache | Cache hit returns items without fetch | No network call |
| TC-004 | Scrapers | Each of 16+ sources returns items | ≥ 1 item each |
| TC-005 | India scraper | India sources parse | Items with titles/links |
| TC-006 | Sanitization | Scraped text with markup | Safe plain text |
| TC-007 | Commands | All 17 commands return content | No crash |
| TC-008 | Summary | `/summary` returns condensed brief | Content served |

## 4. Test Data Strategy

- Fixture HTML/RSS snapshots per source.
- No live network in unit tests (mock HTTP).

## 5. CI Gates

- `pytest` green (with pytest-asyncio installed).
- gitleaks clean.
- Coverage ≥ 60%.

## 6. Related Documents

| Document | Relationship |
| --- | --- |
| [Rules.md](../project/Rules.md) | Test requirements |
| [PRD.md](../product/PRD.md) | Release criteria |
| [TechSpec.md](TechSpec.md) | Components |
| [AppFlow.md](../design/AppFlow.md) | Command tests |
| [Schema.md](Schema.md) | Cache tests |
| [API.md](API.md) | Telegram API tests |
| [Design.md](../design/Design.md) | Format tests |
| [ImplementationPlan.md](../project/ImplementationPlan.md) | TASK-3.3 |
| [Tracker.md](../project/Tracker.md) | Status |
| [SecurityAndCompliance.md](SecurityAndCompliance.md) | Security tests |
| [Deployment.md](Deployment.md) | Test env |
| [Glossary.md](../reference/Glossary.md) | Vocabulary |
| [RiskRegister.md](../project/RiskRegister.md) | Risks |
