# Web Deployment & App Package Submission Guide

요청하신 **"web에 배포하고 앱 패키지 제출"**를 위해, 즉시 제출 가능한 패키지 산출물 생성 절차를 추가했습니다.

## 1) 앱 패키지 생성

```bash
./scripts/build_release_bundle.sh
```

생성물:
- `dist/flight-ai-backend.zip`
- `dist/flight-ai-frontend.tar.gz`

## 2) 웹 배포(권장: Serverless + 정적 프론트)

### Backend (AWS Lambda / API Gateway)
1. AWS 자격증명 설정
2. `infra/serverless/serverless.yml` 환경변수 설정
3. 배포 실행

```bash
cd infra/serverless
npx serverless deploy
```

### Frontend (정적 호스팅)
- Vercel / Netlify / S3+CloudFront 중 하나 사용

예: Vercel
```bash
cd frontend
npm ci
npm run build
npx vercel --prod
```

## 3) 제출용 체크리스트
- 백엔드 패키지 zip 첨부
- 프론트 패키지 tar.gz 첨부
- 배포 URL 첨부
- API 엔드포인트(`/flight`, `/payment`, `/monitoring`) 동작 캡처 첨부

## 주의
현재 이 실행 환경에서는 외부 클라우드 계정 자격증명이 없어 실제 배포 URL 생성까지는 자동 완료할 수 없습니다.
대신, 배포 직전까지 필요한 패키징/절차는 모두 반영했습니다.
