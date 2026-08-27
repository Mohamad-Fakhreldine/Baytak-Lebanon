import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'

import './styles/style.css'
import './styles/popup.css'
import './styles/hamburger-menu.css'
import 'choices.js/public/assets/styles/choices.min.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)