# Local server startup (virtual environment, no Docker)

## 1) Create Python virtual environment (runner only)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

> The venv is used for local helper scripts. Services themselves run with Java/Gradle.

## 2) Prerequisites

- Java 17+
- Gradle installed on host (`gradle -v`)

## 3) Start services directly on host

Single service:

```bash
cd services/auth-service
gradle bootRun
```

Multiple services (helper script):

```bash
source .venv/bin/activate
python scripts/dev_local.py --services auth-service api-gateway
```

## 4) Verify

- Auth: `http://localhost:8081/api/v1/status`
- Gateway: `http://localhost:8080/api/v1/status`

## 5) JWT quick test

```bash
curl -s -X POST http://localhost:8081/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"dev"}'
```

Then call validate with Bearer token.


## 6) GitHub Actions CI

- Workflow: `.github/workflows/services-ci.yml`
- Trigger: push/PR when `services/**` changes
- Runs `gradle clean test` for each service in a matrix

This means CI validation works in GitHub Actions. Hosting/deploy still needs separate deploy steps.

## 7) NGINX reverse proxy (recommended for local integration)

Use NGINX as a single local entrypoint in front of services.

- Config file: `infra/nginx/nginx.conf`
- Listen port: `8090`
- Routes:
  - `/` -> api-gateway (`:8080`)
  - `/api/auth/` -> auth-service (`:8081`)
  - `/api/profile/` -> user-profile-service (`:8082`)

Run full local stack (services + nginx):

```bash
./scripts/run_local_stack.sh
```

Health check:

```bash
curl http://localhost:8090/nginx-health
```
