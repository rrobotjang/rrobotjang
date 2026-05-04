import { useState } from 'react'
import axios from 'axios'

export function SearchPage() {
  const [answer, setAnswer] = useState('')

  const onSearch = async () => {
    const payload = {
      origin: 'ICN',
      destination: 'NRT',
      departure_date: '2026-08-01',
      budget: 500,
      preferences: ['short_layover', 'morning_departure']
    }
    const res = await axios.post('http://localhost:8000/rag/recommend', payload)
    setAnswer(res.data.answer)
  }

  return (
    <div style={{ padding: 24 }}>
      <h1>AI 항공권 검색</h1>
      <button onClick={onSearch}>추천 받기</button>
      <p>{answer}</p>
    </div>
  )
}
