# auth-service

JWT issuing and validation service.

## Endpoints
- `POST /api/auth/login` (public)
- `GET /api/auth/validate` (JWT required)
- `GET /api/v1/status`
- `GET /actuator/health`

## JWT
- Header: `Authorization: Bearer <token>`
- Secret from `security.jwt.secret` in `application.yml`

## Run
```bash
gradle bootRun
```
