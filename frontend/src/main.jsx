import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import CompareReviews from './CompareReviews.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <CompareReviews />
  </StrictMode>,
)
