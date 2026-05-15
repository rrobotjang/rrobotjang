# Autonomous Mobility Fintech Interview Platform — Java Spring Boot Scaffold

## Implemented microservices

Each service now includes a runnable Spring Boot scaffold:
- `build.gradle`, `settings.gradle`
- `src/main/java/.../*Application.java`
- `src/main/java/.../StatusController.java`
- `src/main/resources/application.yml`
- `src/test/java/.../*ApplicationTests.java`

Services:
1. **api-gateway** (port 8080)
2. **auth-service** (port 8081)
3. **user-profile-service** (port 8082)
4. **interview-session-service** (port 8083)
5. **question-bank-service** (port 8084)
6. **coding-test-service** (port 8085)
7. **evaluation-service** (port 8086)
8. **payment-billing-service** (port 8087)
9. **notification-service** (port 8088)
10. **analytics-service** (port 8089)

## Default endpoints

- `GET /api/v1/status`
- `GET /actuator/health`

Example response:
```json
{
  "service": "auth-service",
  "status": "UP",
  "timestamp": "2026-05-15T10:00:00Z"
}
```

## Shared contracts (next implementation step)

- `POST /api/mock/start`
- `POST /api/mock/respond`
- `POST /api/code/submit`
- `POST /api/evaluation/score`
- `GET /api/results/{sessionId}`
- `GET /api/recommendations/{userId}`

## Event topics (Kafka, next implementation step)

- `interview.session.started`
- `interview.answer.submitted`
- `coding.submission.created`
- `evaluation.completed`
- `billing.subscription.renewed`

## MSA definition used in this repo

This scaffold treats each service as an independently deployable bounded context.
To be considered production MSA, we will enforce: database-per-service, contract versioning,
async event integration, and independent scaling/deployment per service.
