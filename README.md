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

## 10) Mockup 데이터 검증 & 시뮬레이션
- 샘플 데이터: `backend/mock_data/flight_offers.json`
- 시뮬레이터: `backend/app/simulation/mock_simulation.py`
- 실행:
```bash
cd backend
PYTHONPATH=. pytest -q tests/test_mock_simulation.py
PYTHONPATH=. python run_simulation.py
```
- 지표:
  - `budget_fit_count`: 예산 내 추천 가능 건수
  - `top1_price`: 추천 1순위 가격
  - `avg_price`: 추천 후보 평균 가격
  - `success_rate`: 예산 적합 비율


## 11) 화면 와이어프레임 예상도
- 구현 파일: `frontend/src/pages/WireframePage.tsx`
- 목적: 검색→추천→결제까지 단일 화면 흐름의 초기 IA/UX 합의용 목업
- 실행 후 `http://localhost:3000`에서 확인

## 12) 자연어 검색 + AI 판단 로직 설명
예시 입력:
- "싸고 덜 피곤한 비행"
- "야간 출발 싫어"

처리 흐름:
1. UI에서 자연어 문장을 `preferences`로 전달
2. `parse_natural_language_intent()`가 의도를 feature로 변환
   - `prefers_low_price`, `prefers_less_fatigue`, `avoids_night`, `avoid_stops`
3. `score_offer()`에서 **price vs duration trade-off + stop penalty**를 계산
4. 상위 점수순으로 추천 결과 반환

핵심 식(현재 휴리스틱):
- `score = price_weight*price_score + duration_score - stop_penalty (+ night_bonus)`
- 저가 선호면 `price_weight` 상승, 덜 피곤 선호면 `duration_score` 가중
- 경유 회피면 `stop_penalty` 강화

## 13) 확장(취향학습/가격예측/RAG 여행추천) 적용 여부를 어떻게 확인하나
**반드시 지표로 확인**합니다.

1) 사용자 취향 학습 적용 여부
- 온라인 지표: CTR, 저장/장바구니율, 예약전환율
- 오프라인 지표: NDCG@K, MRR, Recall@K
- 검증 방법: 개인화 ON/OFF A/B 실험 및 cohort 비교

2) 가격 예측 적용 여부
- 지표: MAE, MAPE, RMSE
- 비즈니스 지표: 예측 기반 알림 클릭률, 가격민감 사용자 전환율
- 검증 방법: 실제 체결가 대비 백테스트 + 시간축 walk-forward 검증

3) RAG 여행 추천 적용 여부
- 검색 품질: Context Precision/Recall, Answer Faithfulness
- 제품 지표: itinerary 저장률, 추천 클릭률, 재방문율
- 검증 방법: 골든셋 QA + human eval + 환각률(unsupported claim rate)

운영 권장:
- 기능마다 `feature_flag`와 실험 ID를 로그/이벤트에 남겨 대시보드에서 ON/OFF 성과를 분리 관측

## 14) 서버 모니터링 대시보드 + Alert + Telegram/Kakao 알림
추가 API:
- `GET /monitoring/dashboard`: 최근 요청 count / p95(ms) / error_rate
- `POST /monitoring/simulate-request`: 테스트용 메트릭 삽입
- `POST /monitoring/check-alert`: 임계치 초과 시 알림 전송

Alert 조건(기본):
- `error_rate >= 0.1` 또는 `p95_ms >= 1200`

알림 채널:
- Telegram Bot API (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`)
- Kakao Webhook (`KAKAO_WEBHOOK_URL`)

운영 팁:
- 실제 운영에서는 Prometheus/Grafana와 연동해 동일 지표를 대시보드화하고,
  Alertmanager를 통해 Telegram/Kakao 알림 라우팅을 권장.

## 15) Serverless MSA로 Scale-up 하는 방법
현재 구조를 **도메인 단위 MSA**로 분리 가능:
- Flight API (`/flight/*`)
- Payment API (`/payment/*`)
- Monitoring API (`/monitoring/*`)

### 적용 포인트
1. `backend/app/lambda_handlers/*`에 서비스별 FastAPI 앱 구성
2. `Mangum`으로 AWS Lambda + API Gateway에 연결
3. `infra/serverless/serverless.yml`로 함수별 배포 단위 분리

### 왜 scale-up에 유리한가
- 트래픽 패턴이 다른 서비스(검색/결제/모니터링)를 **독립 오토스케일**
- 장애 격리(결제 장애가 검색 API까지 전파되지 않음)
- 배포 독립성(Flight만 핫픽스 배포 가능)

### 권장 다음 단계
- 예약/결제는 SQS + DLQ + idempotency key 필수
- 추천 파이프라인은 비동기 배치(이벤트 기반) + Redis 캐시 계층화
- 관측성: CloudWatch + X-Ray + OpenTelemetry + central log
