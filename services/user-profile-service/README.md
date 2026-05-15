# user-profile-service

User profile service backed by PostgreSQL with local caching.

## Features
- PostgreSQL persistence (JPA + Flyway)
- Local in-memory cache (Caffeine) for profile reads
- Cache eviction on profile upsert

## Endpoints
- `POST /api/profile`
- `GET /api/profile/{userId}`
- `GET /api/profile/me`
- `GET /api/v1/status`

## Environment
- `DB_URL` (default `jdbc:postgresql://localhost:5432/user_profile_db`)
- `DB_USERNAME` (default `user_profile`)
- `DB_PASSWORD` (default `user_profile_pw`)

## Run
```bash
gradle bootRun
```
