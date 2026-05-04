# Flight AI Commerce Platform (React + FastAPI + PostgreSQL/pgvector)

프로덕션급 항공권 검색/추천/예약 확장을 위한 레포 구조입니다.

## 1) 핵심 아키텍처
- **검색 입력**: 출발지/도착지/날짜/예산 + 취향 태그.
- **RDB 정규화 저장**: 공급자(Amadeus) raw payload를 정규화 테이블에 저장.
- **벡터 검색**: `pgvector`로 의미 유사 항공편 검색.
- **Gen-AI 추천**: LLM이 규칙/설명 가능한 추천 문구 생성.
- **예약/결제 연계**: `flight_offers`의 `external_offer_id`를 결제/PNR 생성 파이프라인으로 전달.

## 2) 정규화 스키마 (핵심)
초기 MVP 핵심 테이블:
- `airports(id, iata_code, city, country)`
- `flight_offers(id, source, external_offer_id, origin_airport_id, destination_airport_id, departure_date, return_date, cabin_class, price_total, currency, seats_remaining, raw_payload, embedding, created_at)`

확장 권장 테이블:
- `users`, `user_preferences`, `search_queries`, `bookings`, `payments`, `tickets`, `price_forecasts`, `trip_recommendations`

정규화 원칙:
1. 공급자 raw는 `raw_payload`에 보관(감사/리플레이 용도)
2. 검색/필터 기준 필드는 원자 컬럼으로 분리
3. 결제/예약 키(`external_offer_id`)는 소스별 unique 인덱스
4. embedding은 `flight_offers` 또는 별도 `offer_embeddings`로 분리 가능


## 3-1) 왜 `text-embedding-3-large`가 적합한가
항공권 추천 도메인에서는 공항/도시/경유/환승시간/수하물/요금규정 같은 **의미적 유사도**가 중요합니다.

선정 이유:
1. **검색 품질 우선**: 다국어 질의(한/영), 짧은 키워드, 자연어 조건에서 고차원 임베딩이 유사도 분리에 유리
2. **RAG 안정성**: 유사 문서 회수(retrieval) 품질이 좋아 LLM 추천 근거 품질이 함께 개선
3. **도메인 확장성**: 향후 호텔/액티비티/여행 추천까지 같은 임베딩 스키마로 확장 가능
4. **운영 전략과 궁합**: 배치 임베딩 + Redis 캐시와 결합하면 온라인 지연을 제어 가능

운영 권장:
- 기본값은 `text-embedding-3-large`로 시작
- 비용 최적화가 필요하면
  - 쿼리 임베딩만 large 유지
  - 문서 임베딩은 small/증분 재임베딩으로 단계적 다운사이징
  - A/B(CTR, booking conversion, NDCG@k)로 모델 선택

## 3) Redis 캐싱 전략
- 키: `rec:{origin}:{destination}:{departure_date}:{budget}:{pref_hash}`
- TTL: 5~15분 (가격 변동 고려)
- 캐시 계층:
  1) 추천 응답 캐시
  2) Amadeus 토큰/메타 캐시
  3) 인기 라우트 프리컴퓨트 캐시

## 4) 추천 파이프라인 (FastAPI)
`backend/app/services/recommendation.py`의 핵심 흐름:
```python
async def recommend_pipeline(query, db):
    q_emb = await embed(query)              # 1) query embedding
    flights = await search_similar(db, q_emb, query)  # 2) RDB + vector search
    answer = await recommend_flights(query, flights)  # 3) LLM 판단/설명
    return answer
```

## 5) 배치/스케줄링
- `workers/amadeus_ingest.py`: 30분 cron 수집/적재
- `workers/embedding_batch.py`: 미임베딩 행 배치 생성

## 6) 가격 예측 모델 확장
- `ml/price_forecast.py`: baseline placeholder
- 다음 단계:
  - 특성: DTD(days-to-departure), carrier, seasonality, events
  - 모델: LightGBM/XGBoost + quantile prediction
  - serving: `/pricing/forecast` endpoint + `price_forecasts` 테이블 적재

## 7) 레포 구조
```
.
├── backend
│   ├── app
│   │   ├── api
│   │   ├── core
│   │   ├── db
│   │   ├── models
│   │   ├── schemas
│   │   ├── services
│   │   └── workers
│   └── requirements.txt
├── frontend
│   └── src
├── infra/sql
├── ml
├── docker-compose.yml
└── .env.example
```

## 8) 실행
```bash
docker compose up --build
```
- API: `http://localhost:8000/docs`
- UI: `http://localhost:3000`

## 9) 프로덕션 체크리스트
- [ ] Alembic migration 도입
- [ ] 결제(Stripe/토스) webhook idempotency
- [ ] 예약 lock/재시도 큐
- [ ] observability (OpenTelemetry + Prometheus)
- [ ] feature store + 사용자 취향 온라인 학습
