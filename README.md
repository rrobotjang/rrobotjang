# rrobotjang - Interview Platform MSA

## Production-ready deployment (Render + GitHub Actions)

### 1) Auto-deploy config
- `render.yaml` defines 3 deployable services:
  - `rrobotjang-api-gateway`
  - `rrobotjang-auth-service`
  - `rrobotjang-user-profile-service`
- Health checks for each service:
  - `GET /actuator/health`

### 2) GitHub Actions CD on `main`
- Workflow: `.github/workflows/deploy-render.yml`
- Trigger:
  - push to `main`
  - manual `workflow_dispatch`
- Required GitHub Secrets:
  - `RENDER_DEPLOY_HOOK_API_GATEWAY`
  - `RENDER_DEPLOY_HOOK_AUTH_SERVICE`
  - `RENDER_DEPLOY_HOOK_USER_PROFILE_SERVICE`

### 3) Render environment variables
Set these in Render service dashboard:

#### auth-service
- `JWT_SECRET` (required, secure random >= 32 chars)

#### user-profile-service
- `DB_URL`
- `DB_USERNAME`
- `DB_PASSWORD`

#### api-gateway
- `AUTH_SERVICE_URL`
- `USER_PROFILE_SERVICE_URL`

> Note: `AUTH_SERVICE_URL` and `USER_PROFILE_SERVICE_URL` are wired in `render.yaml` via `fromService`.

---

## Local server run (no Docker)

### Quick start
```bash
./scripts/run_local_stack.sh
```

### Endpoints
- Gateway UI: `http://localhost:8080/`
- NGINX entrypoint: `http://localhost:8090/` (if nginx installed)
- NGINX health: `http://localhost:8090/nginx-health`

### Auth flow test
```bash
curl -s -X POST http://localhost:8081/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"dev"}'
```

---

## CI
- Workflow: `.github/workflows/services-ci.yml`
- Runs `gradle clean test` per service on push/PR changes in `services/**`

## Key paths
- NGINX config: `infra/nginx/nginx.conf`
- Local stack runner: `scripts/run_local_stack.sh`
- Local venv/doc guide: `docs/LOCAL_RUN_VENV.md`
- API Gateway web UI: `services/api-gateway/src/main/java/com/rrobotjang/apigateway/InterviewWebController.java`
