# api-gateway

Spring Cloud Gateway service.

## Implemented routing
- `/api/auth/**` -> `auth-service`
- `/api/profile/**` -> `user-profile-service`

## Endpoints
- `GET /` (Interview Web UI)
- `GET /api/v1/status`
- `GET /actuator/health`
- `GET /swagger-ui.html`

## Run
```bash
gradle bootRun
```
