import React from 'react'
import ReactDOM from 'react-dom/client'
import { SearchPage } from './pages/SearchPage'
import './styles.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <SearchPage />
  </React.StrictMode>
)

if ('serviceWorker' in navigator) {
  window.addEventListener('load', async () => {
    try {
      await navigator.serviceWorker.register('/sw.js')
    } catch (error) {
      console.error('service worker register failed', error)
    }
  })
}
