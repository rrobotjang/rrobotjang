# Lighthouse PWA Checklist

## 1) Installability
- [x] Web App Manifest 존재 (`public/manifest.webmanifest`)
- [x] `name`, `short_name`, `start_url`, `display`, `icons`, `theme_color` 포함
- [x] Service Worker 등록 (`src/main.tsx`)

## 2) Offline support
- [x] `offline.html` 제공
- [x] Service Worker precache (`/`, `/offline.html`, manifest, icons)
- [x] Navigation 요청 실패 시 offline fallback 반환

## 3) Cache strategy
- [x] 정적 리소스: cache-first
- [x] 문서 탐색: network-first + runtime cache fallback
- [x] cache versioning 및 activate 시 구버전 cache 정리

## 4) Responsive / mobile
- [x] viewport meta
- [x] mobile-first CSS + media query

## 5) Remaining steps to reach "near-perfect" Lighthouse
1. HTTPS 배포 환경에서 실제 Lighthouse 실행
2. 아이콘을 PNG(192/512)로 추가해 플랫폼 호환성 강화
3. 서비스워커에 stale-while-revalidate 도입(필요 시)
4. API 응답 캐시 TTL 정책 추가
5. 실제 기기 설치/재실행 시나리오 검증
