# RiskRegister — AI Daily Telegram Bot: Known Risks

| Field | Value |
| --- | --- |
| Version | v0.1 |
| Last Updated | 2026-08-06 |
| Owner | PM / Eng Lead |
| Status | In Review |

---

| Risk | Likelihood | Impact | Score | Mitigation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 Source outages | High | Medium | 6 | Cache + curated fallback (REQ-004) | Eng | Mitigating |
| R-002 Oversize message crash | Medium | High | 6 | Message splitting (REQ-007) | Eng | Mitigating |
| R-003 Telegram rate-limit ban | Medium | Medium | 4 | Bounded retries, backoff | Eng | Open |
| R-004 Token leak | Low | Critical | 8 | Env-only + gitleaks + rotation | Security | Mitigating |
| R-005 Gemini quota/cost | Medium | Low | 2 | Optional, deterministic fallback | PM | Accepted |
| R-006 Scraping blocked by sources | Medium | Medium | 4 | Rotate sources, cache aggressively | Eng | Open |
| R-007 Scraped-content injection | Low | Medium | 3 | Sanitization + escape | Security | Mitigating |
| R-008 Schedule missed (no chat id) | Low | Low | 1 | Config validation + logs | Eng | Accepted |

## Risk Matrix

```mermaid
quadrantChart
    title AI Telegram Bot Risk Matrix
    x-axis Low Likelihood --> High Likelihood
    y-axis Low Impact --> High Impact
    quadrant-1 Monitor
    quadrant-2 Critical - Mitigate
    quadrant-3 Accept
    quadrant-4 Manage
    R-001: [0.8, 0.5]
    R-002: [0.5, 0.75]
    R-003: [0.55, 0.45]
    R-004: [0.15, 0.9]
    R-005: [0.55, 0.2]
    R-006: [0.6, 0.45]
    R-007: [0.25, 0.5]
    R-008: [0.2, 0.15]
```

## Related Documents

| Document | Relationship |
| --- | --- |
| [PRD.md](../product/PRD.md) | Top-3 risks |
| [TechSpec.md](../technical/TechSpec.md) | Technical risks |
| [SecurityAndCompliance.md](../technical/SecurityAndCompliance.md) | R-004/R-007 |
| [AppFlow.md](../design/AppFlow.md) | Fallback flow |
| [Design.md](../design/Design.md) | Format |
| [Schema.md](../technical/Schema.md) | Cache |
| [ImplementationPlan.md](ImplementationPlan.md) | Mitigations |
| [Tracker.md](Tracker.md) | Risk status |
| [Rules.md](Rules.md) | Standards |
| [API.md](../technical/API.md) | R-003 |
| [Testing.md](../technical/Testing.md) | Test coverage |
| [Deployment.md](../technical/Deployment.md) | Rollback |
| [Glossary.md](../reference/Glossary.md) | Vocabulary |
