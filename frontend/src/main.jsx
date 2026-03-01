import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import './index.css'
import { ProjectProvider } from './context/ProjectContext'
import { RoleProvider } from './context/RoleContext'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <RoleProvider>
        <ProjectProvider>
          <App />
        </ProjectProvider>
      </RoleProvider>
    </BrowserRouter>
  </React.StrictMode>
)
