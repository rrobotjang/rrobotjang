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
