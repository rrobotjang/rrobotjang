# Interview Q&A (50) for Full-Stack + AI Engineer + Mobility Fintech Domain

## 1) Tell me about yourself.
I’m a backend and AI-focused engineer who enjoys building production systems where reliability and intelligence meet. Recently, I’ve focused on autonomous mobility and fintech intersections, especially event-driven services, secure payments, and AI-based evaluation workflows.

## 2) Why do you want to work at a Big Tech company?
I want to solve problems at massive scale with strong engineering standards. Big Tech environments push architecture quality, observability, and execution speed, which aligns with how I like to build systems.

## 3) Describe a challenging backend problem you solved.
I designed a resilient asynchronous workflow where partial failures were common. I used idempotency keys, retry policies with backoff, and compensating transactions to keep ledger state consistent.

## 4) How do you design a scalable REST API?
I start with resource modeling, strict versioning, and stateless handlers. Then I add pagination, caching, rate limits, observability, and contract tests to preserve reliability at scale.

## 5) How do you handle concurrency in Java services?
I combine proper transaction boundaries, optimistic locking where suitable, and queue-based decoupling for hot paths. For distributed flows, I use idempotent consumers and deduplication keys.

## 6) Explain eventual consistency vs strong consistency.
Strong consistency guarantees immediate read correctness after write, while eventual consistency allows temporary divergence for higher availability and scale. I choose based on business risk and user expectations.

## 7) What is your approach to database indexing?
I profile real query patterns first, then design targeted indexes for high-frequency filters and joins. I verify with execution plans and monitor index write overhead over time.

## 8) How do you secure APIs?
I use short-lived JWTs, scope-based authorization, mTLS for service-to-service traffic, secret rotation, and input validation. I also enforce audit logging and anomaly alerts.

## 9) How do you prevent duplicate payment processing?
I enforce idempotency keys at the API layer and store request fingerprints with final status. Retries return the original outcome instead of creating a new transaction.

## 10) Explain the Outbox pattern.
The Outbox pattern writes domain state and event records in one local transaction, then publishes events asynchronously. This avoids inconsistencies between DB commits and message publishing.

## 11) How would you design a coding-test platform backend?
I’d separate problem management, submission ingestion, execution orchestration, and scoring services. I’d sandbox execution, capture telemetry, and use asynchronous pipelines for fair and scalable evaluation.

## 12) How do you evaluate code submissions fairly?
I score across correctness, complexity, robustness, and readability with transparent rubrics. I also normalize runtime environments and randomize hidden tests to reduce leakage.

## 13) How do you monitor microservices?
I instrument logs, metrics, and traces with shared correlation IDs. Then I define SLIs/SLOs and alert on user-impacting symptoms, not only infrastructure thresholds.

## 14) Describe your testing strategy.
I pyramid tests: unit tests for logic, integration tests for contracts and data, and end-to-end tests for core journeys. For critical flows, I add chaos and load tests.

## 15) How do you handle schema changes without downtime?
I use backward-compatible migrations, dual-read/write transitions when necessary, and phased rollouts. I never couple deployment safety to one-shot destructive schema updates.

## 16) What is your frontend architecture approach in Svelte?
I prefer feature-based modules, store-driven state, and clear UI/domain separation. I keep components small and make async states explicit: loading, success, empty, error.

## 17) How do you optimize frontend performance?
I reduce bundle size via code splitting, cache API responses, and virtualize large lists. I also track Web Vitals and fix regressions with performance budgets.

## 18) How do you design for accessibility?
I use semantic markup, keyboard navigation, focus management, and sufficient color contrast. Accessibility checks are included in CI, not treated as a final-step task.

## 19) Explain CI/CD practices you follow.
Each PR runs lint, tests, security checks, and build verification. Deployments are automated with staged rollouts and rapid rollback capability.

## 20) How do you work with product managers?
I translate product goals into measurable technical outcomes and discuss trade-offs early. I keep scope honest and expose risks with mitigation plans.

## 21) How do you estimate engineering tasks?
I estimate by complexity, risk, and unknowns, not by optimism. I break work into milestones with clear acceptance criteria and review points.

## 22) What is your incident response style?
Stabilize first, diagnose second, optimize third. I communicate timelines clearly, assign an incident commander, and produce blameless postmortems with concrete follow-ups.

## 23) Tell me about a production outage you handled.
A dependency timeout cascaded across services. I added circuit breakers, tuned timeouts by hop, and introduced fallback behavior, reducing repeated outage risk.

## 24) How do you design rate limiting?
I apply token-bucket limits per user and endpoint, with stricter tiers for expensive operations. I expose headers so clients can adapt before hard failures.

## 25) How do you choose between SQL and NoSQL?
If consistency, joins, and transactional integrity dominate, I choose SQL. If flexible schemas and horizontal write scale dominate, I evaluate NoSQL.

## 26) Explain CAP theorem in practice.
Under partition, you choose consistency or availability characteristics by endpoint. I often isolate critical operations for stronger guarantees and allow eventual behavior elsewhere.

## 27) What is your approach to system design interviews?
I clarify requirements, define constraints, propose a baseline architecture, and then pressure-test bottlenecks. I explicitly discuss trade-offs, failure modes, and evolution path.

## 28) How do you design a notification system?
I separate template management, event triggers, preference controls, and channel delivery workers. Retries, deduplication, and observability are essential.

## 29) How do you prevent prompt injection in AI workflows?
I isolate system policies, sanitize retrieved context, and restrict tool permissions. I also monitor anomalous prompt patterns and apply output validation gates.

## 30) How do you evaluate LLM outputs?
I combine rubric-based human review with automated checks for format, correctness proxies, and policy compliance. For stable tasks, I maintain benchmark sets and regression gates.

## 31) What is RAG and when do you use it?
RAG augments LLMs with retrieved context from trusted sources. I use it when answers must reference current, domain-specific, or auditable knowledge.

## 32) How do you reduce hallucinations?
I constrain output schema, improve retrieval quality, and force citation-backed responses where possible. I also return uncertainty explicitly when confidence is low.

## 33) How do you design an AI interview evaluator?
I decompose scoring into communication, correctness, depth, and structure. The model outputs structured JSON with evidence snippets and confidence fields.

## 34) How do you handle AI latency?
I stream partial outputs, cache reusable context, and route lightweight tasks to smaller models. I also set strict timeout budgets and graceful fallback behavior.

## 35) Explain feature flags.
Feature flags decouple deploy from release and enable controlled experiments. I use them for progressive rollout, fast rollback, and safer migration paths.

## 36) How do you store secrets securely?
I use a dedicated secret manager with rotation, least privilege, and short-lived credentials. Secrets never belong in source control or client bundles.

## 37) What is your logging philosophy?
Logs should explain user impact and system intent, not just stack traces. I enforce structured logs with stable keys for queryability.

## 38) How do you mentor junior engineers?
I coach through design reviews, pair sessions, and actionable feedback. I focus on first principles so they can make independent decisions over time.

## 39) How do you prioritize technical debt?
I prioritize debt that increases incident risk, slows delivery, or blocks strategic features. I frame debt work in terms of measurable business impact.

## 40) Explain tokenization in fintech.
Tokenization replaces sensitive payment credentials with non-sensitive tokens. This reduces breach impact and helps keep PCI scope manageable.

## 41) How do you design V2I payment flow?
Vehicle identity and payment token are validated first, then authorization is reserved and later captured on service completion. Every step is idempotent and auditable.

## 42) How do you ensure auditability in payments?
I use immutable ledger records, correlation IDs across events, and timestamped state transitions. Reconciliation jobs verify provider records against internal books.

## 43) How do you approach fraud detection?
I combine real-time rules with anomaly scoring and feedback loops from confirmed outcomes. High-risk events trigger step-up verification.

## 44) How would you design MaaS billing?
I model trip lifecycle events, pricing rules, adjustments, and settlement windows. Billing is asynchronous, replayable, and traceable from trip to invoice.

## 45) How do you handle multi-tenant architecture?
I isolate tenant data and apply tenant-aware authorization checks everywhere. I also enforce per-tenant rate limits and noisy-neighbor protections.

## 46) What coding interview habits help you succeed?
I restate the problem, clarify constraints, outline approach, and code incrementally with tests. I narrate trade-offs and validate edge cases before finalizing.

## 47) How do you explain trade-offs under pressure?
I present options with cost, risk, and time-to-delivery, then choose based on stated priorities. Clear reasoning beats pretending there is a perfect answer.

## 48) What makes you effective in cross-functional teams?
I communicate early, document decisions, and resolve ambiguity fast. I focus on shared outcomes instead of local optimization.

## 49) Where do you want to grow next?
I want deeper ownership of end-to-end AI production systems, including evaluation science and reliability engineering. I also want to mentor broader teams.

## 50) Why should we hire you?
I bring strong backend fundamentals, practical AI integration experience, and a reliability-first mindset for high-stakes domains. I can ship quickly while maintaining long-term architectural quality.
