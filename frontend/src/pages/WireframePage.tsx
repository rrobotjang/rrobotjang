import React from 'react'

const box: React.CSSProperties = {
  border: '2px dashed #94a3b8',
  borderRadius: 8,
  padding: 12,
  marginBottom: 12,
  background: '#f8fafc'
}

export function WireframePage() {
  return (
    <div style={{ maxWidth: 980, margin: '0 auto', padding: 24, fontFamily: 'sans-serif' }}>
      <h1>Flight AI 화면 와이어프레임 (예상도)</h1>
      <div style={box}>
        <strong>[Header]</strong>
        <p>로고 | 검색내역 | 로그인/마이페이지</p>
      </div>

      <div style={{ ...box, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
        <div style={{ border: '1px solid #cbd5e1', padding: 10 }}>
          <strong>[검색 입력 패널]</strong>
          <p>출발지 / 도착지 / 날짜 / 예산 / 취향태그</p>
          <p>AI 검색 버튼</p>
        </div>
        <div style={{ border: '1px solid #cbd5e1', padding: 10 }}>
          <strong>[AI 추천 요약]</strong>
          <p>추천 이유 3줄 요약</p>
          <p>가격 전망(상승/하락) 뱃지</p>
        </div>
      </div>

      <div style={box}>
        <strong>[결과 리스트]</strong>
        <p>카드형 항공권 1..N (가격, 경유, 수하물, 환불규정)</p>
        <p>정렬: 최저가/최단시간/AI추천순</p>
      </div>

      <div style={{ ...box, display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 12 }}>
        <div style={{ border: '1px solid #cbd5e1', padding: 10 }}>
          <strong>[상세/선택 항공권]</strong>
          <p>여정 타임라인 + 요금 상세 + 정책</p>
        </div>
        <div style={{ border: '1px solid #cbd5e1', padding: 10 }}>
          <strong>[결제 패널]</strong>
          <p>탑승자 정보 입력</p>
          <p>결제수단 선택</p>
          <p>결제하기 버튼</p>
        </div>
      </div>
    </div>
  )
}
