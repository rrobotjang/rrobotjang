# Autonomous Mobility Fintech Interview Platform — Service Scaffold

## Microservices

1. **api-gateway**: Single entrypoint, JWT validation, rate limiting, routing.
2. **auth-service**: Sign-up/login, OAuth, token lifecycle, role management.
3. **user-profile-service**: Candidate profile, target companies, skill graph.
4. **interview-session-service**: Mock interview orchestration, turn-by-turn state.
5. **question-bank-service**: Domain-tagged technical/behavioral question catalog.
6. **coding-test-service**: Problem delivery, starter code, test-case execution metadata.
7. **evaluation-service**: LLM scoring pipeline (communication, technical depth, clarity).
8. **payment-billing-service**: Subscription, wallet, in-app credits, invoice lifecycle.
9. **notification-service**: Email/push/webhook for reminders and result publishing.
10. **analytics-service**: Session analytics, weak-skill heatmap, readiness score trends.

## Shared contracts

- `POST /api/mock/start`
- `POST /api/mock/respond`
- `POST /api/code/submit`
- `POST /api/evaluation/score`
- `GET /api/results/{sessionId}`
- `GET /api/recommendations/{userId}`

## Event topics (Kafka)

- `interview.session.started`
- `interview.answer.submitted`
- `coding.submission.created`
- `evaluation.completed`
- `billing.subscription.renewed`

## Baseline non-functional goals

- P95 API latency < 300ms (non-LLM paths).
- Strong idempotency for payment and code-submission endpoints.
- Zero raw card-data storage (tokenization-only model).
- End-to-end traceability with correlation IDs.
