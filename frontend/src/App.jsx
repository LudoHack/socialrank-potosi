import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout/Layout'
import CentroComando from './pages/CentroComando'
import Dashboard from './pages/Dashboard'
import Narrativas from './pages/Narrativas'
import Emociones from './pages/Emociones'
import Arquetipos from './pages/Arquetipos'
import Lenguaje from './pages/Lenguaje'
import Comunidades from './pages/Comunidades'
import Riesgos from './pages/Riesgos'
import Simulacion from './pages/Simulacion'
import Evolucion from './pages/Evolucion'
import Recomendaciones from './pages/Recomendaciones'
import Proyectos from './pages/Proyectos'
import IVB from './pages/IVB'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/"               element={<Navigate to="/centro" replace />} />
        <Route path="/centro"         element={<CentroComando />} />
        <Route path="/dashboard"      element={<Dashboard />} />
        <Route path="/ivb"            element={<IVB />} />
        <Route path="/narrativas"     element={<Narrativas />} />
        <Route path="/emociones"      element={<Emociones />} />
        <Route path="/arquetipos"     element={<Arquetipos />} />
        <Route path="/lenguaje"       element={<Lenguaje />} />
        <Route path="/comunidades"    element={<Comunidades />} />
        <Route path="/riesgos"        element={<Riesgos />} />
        <Route path="/simulacion"     element={<Simulacion />} />
        <Route path="/evolucion"      element={<Evolucion />} />
        <Route path="/recomendaciones" element={<Recomendaciones />} />
        <Route path="/proyectos"      element={<Proyectos />} />
      </Routes>
    </Layout>
  )
}
