import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import CompareReviews from './CompareReviews.jsx'
import Summary from './Summary.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Summary />
    <CompareReviews />
  </StrictMode>,
)
