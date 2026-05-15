# Production E2E blueprint (PostgreSQL + caching + JWT/Auth)

## Goal
Reduce service load using local cache while keeping auth/JWT and persistence production-ready.

## Architecture
- `api-gateway` routes external traffic.
- `auth-service` issues/validates JWT.
- `user-profile-service` uses PostgreSQL as source of truth + Caffeine local cache.

## Request flow
1. Client sends JWT to gateway.
2. Gateway routes to downstream service.
3. `user-profile-service` reads profile:
   - cache hit: return fast
   - cache miss: read PostgreSQL, cache result for 5 minutes
4. Profile update evicts cache entry immediately.

## Database (PostgreSQL)
- Service DB: `user_profile_db`
- Migration tool: Flyway
- Table: `user_profiles(user_id, email, display_name)`

## JWT/Auth safety notes
- `auth-service` validates Bearer tokens in `JwtAuthFilter`.
- Keep secret in environment/secret manager, not in code.
- In production, rotate keys and move to asymmetric signing (RS256).

## Deploy checklist
- Use managed PostgreSQL and private network access.
- Set env vars: `DB_URL`, `DB_USERNAME`, `DB_PASSWORD`, `JWT_SECRET`.
- Configure autoscaling + health checks `/actuator/health`.
- Enable metrics/logging/tracing in APM.
