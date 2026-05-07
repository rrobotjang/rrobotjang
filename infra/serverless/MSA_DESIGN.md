# Serverless MSA Design

이 서버리스 구성은 기능별 마이크로서비스(Flight / Payment / Monitoring)로 분리되어 있습니다.

## 서비스 분리

- **flight-api**: 항공권 추천/알림 도메인
- **payment-api**: 결제 승인/확정 도메인
- **monitoring-api**: 모니터링/헬스체크 도메인

각 서비스는 독립 Lambda 엔트리포인트(`app.lambda_handlers.<domain>.handler`)를 사용합니다.

## 배포 단위

`package.individually: true`를 사용해 함수별 아티팩트를 별도로 생성합니다.

장점:
- 변경된 도메인만 빠르게 배포 가능
- 서비스별 롤백 용이
- 함수별 패키지 크기 최적화에 유리

## 라우팅

- `/flight/{proxy+}` -> `flight-api`
- `/payment/{proxy+}` -> `payment-api`
- `/monitoring/{proxy+}` -> `monitoring-api`

## 확장 가이드

향후 완전한 MSA 전환 시 각 도메인을 별도 repo/서비스로 분리하고,
공통 모듈은 layer 또는 내부 패키지 레지스트리로 분리하는 것을 권장합니다.
