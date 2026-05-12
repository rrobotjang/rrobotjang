import { useState } from 'react'
import axios from 'axios'

export function SearchPage() {
  const [answer, setAnswer] = useState('')
  const [nl, setNl] = useState('싸고 덜 피곤한 비행, 야간 출발 싫어')

  const onSearch = async () => {
    const payload = {
      origin: 'ICN',
      destination: 'NRT',
      departure_date: '2026-08-01',
      budget: 500,
      preferences: [nl]
    }
    const res = await axios.post('http://localhost:8000/flight/recommend', payload)
    setAnswer(JSON.stringify(res.data, null, 2))
  }

  return (
    <div className="container">
      <div className="card">
        <h1>AI 자연어 항공권 검색</h1>
        <p>PWA 설치 가능 + 반응형 UI 샘플</p>
        <textarea value={nl} onChange={(e) => setNl(e.target.value)} rows={3} />
        <div className="actions">
          <button onClick={onSearch}>자연어로 추천 받기</button>
        </div>
        <pre>{answer}</pre>
      </div>
    </div>
  )
}
