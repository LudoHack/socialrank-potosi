import { useState } from 'react'
import { NavLink } from 'react-router-dom'
import { useProject } from '../../context/ProjectContext'
import { useRole } from '../../context/RoleContext'
import {
  LayoutDashboard, Target, BookOpen, Activity, Users, MessageSquare,
  Globe2, AlertTriangle, TrendingUp, Bot, Lightbulb, FolderOpen,
  Landmark, ShieldCheck, LogOut, Lock, X, ChevronRight, Zap
} from 'lucide-react'
import './Sidebar.css'

const NAV_CLIENTE = [
  { to: '/centro',          icon: Zap,             label: 'Centro de Comando',  highlight: true },
  { to: '/dashboard',       icon: LayoutDashboard,  label: 'Dashboard' },
  { divider: true, label: 'ANÁLISIS' },
  { to: '/narrativas',      icon: BookOpen,         label: 'Narrativas' },
  { to: '/emociones',       icon: Activity,         label: 'Emociones' },
  { to: '/arquetipos',      icon: Users,            label: 'Arquetipos' },
  { to: '/lenguaje',        icon: MessageSquare,    label: 'Lenguaje' },
  { to: '/comunidades',     icon: Globe2,           label: 'Comunidades' },
  { to: '/riesgos',         icon: AlertTriangle,    label: 'Riesgos' },
  { to: '/evolucion',       icon: TrendingUp,       label: 'Evolución' },
  { divider: true, label: 'INTELIGENCIA IA' },
  { to: '/simulacion',      icon: Bot,              label: 'Simulación IA' },
  { to: '/recomendaciones', icon: Lightbulb,        label: 'Recomendaciones IA' },
]

const NAV_ADMIN_EXTRA = [
  { divider: true, label: 'ADMINISTRACIÓN' },
  { to: '/proyectos', icon: FolderOpen, label: 'Proyectos' },
]

export default function Sidebar() {
  const { activeProject } = useProject()
  const { isAdmin, loginAdmin, logoutAdmin } = useRole()

  const [showLogin, setShowLogin] = useState(false)
  const [password, setPassword]   = useState('')
  const [error, setError]         = useState('')

  const NAV = isAdmin ? [...NAV_CLIENTE, ...NAV_ADMIN_EXTRA] : NAV_CLIENTE

  const handleLogin = () => {
    const ok = loginAdmin(password)
    if (ok) {
      setShowLogin(false)
      setPassword('')
      setError('')
    } else {
      setError('Contraseña incorrecta')
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleLogin()
  }

  return (
    <>
      <aside className="sidebar">
        {/* Brand */}
        <div className="sidebar-brand">
          <div className="brand-logo">
            <Landmark size={18} strokeWidth={2} />
          </div>
          <div className="brand-text">
            <h1>Social Rank</h1>
            <p>Bolivia · Potosí</p>
          </div>
        </div>

        {/* Nav */}
        <nav className="sidebar-nav">
          {NAV.map((item, i) =>
            item.divider ? (
              <div key={i} className="nav-section-label">
                {item.label && <span>{item.label}</span>}
              </div>
            ) : (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  'nav-link' +
                  (isActive ? ' active' : '') +
                  (item.highlight ? ' nav-highlight' : '')
                }
              >
                <span className="nav-icon">
                  <item.icon size={15} strokeWidth={2} />
                </span>
                <span className="nav-label">{item.label}</span>
                {item.highlight && (
                  <span className="nav-badge-live">LIVE</span>
                )}
              </NavLink>
            )
          )}
        </nav>

        {/* Role */}
        <div className="sidebar-role">
          {isAdmin ? (
            <div className="role-row">
              <span className="role-dot dot-verde" />
              <ShieldCheck size={12} style={{ color: 'var(--success)', flexShrink: 0 }} />
              <span className="role-label">Administrador</span>
              <button className="role-exit-btn" onClick={logoutAdmin} title="Salir">
                <LogOut size={10} /> Salir
              </button>
            </div>
          ) : (
            <div className="role-row">
              <span className="role-dot dot-azul" />
              <span className="role-label">Vista Cliente</span>
              <button
                className="role-exit-btn role-admin-btn"
                onClick={() => { setShowLogin(true); setError('') }}
                title="Acceso administrador"
              >
                <Lock size={10} /> Admin
              </button>
            </div>
          )}
        </div>

        {/* Project footer */}
        <div className="sidebar-footer">
          <div className="project-label">Proyecto activo</div>
          <div className="project-name">
            {activeProject ? activeProject.nombre : '— Sin proyecto —'}
          </div>
          {activeProject?.cliente && (
            <div className="project-client">{activeProject.cliente}</div>
          )}
        </div>
      </aside>

      {/* Modal admin login */}
      {showLogin && (
        <div
          className="modal-overlay open"
          onClick={e => e.target.className.includes('modal-overlay') && setShowLogin(false)}
        >
          <div className="modal" style={{ maxWidth: 360 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 6 }}>
              <Lock size={18} style={{ color: 'var(--gold)' }} />
              <h3>Acceso Administrador</h3>
            </div>
            <p style={{ fontSize: 13, color: 'var(--muted)', marginBottom: 18 }}>
              Ingresa la contraseña para acceder a las herramientas de gestión y carga de datos.
            </p>
            <div className="form-group">
              <label>Contraseña</label>
              <input
                type="password"
                autoFocus
                value={password}
                onChange={e => { setPassword(e.target.value); setError('') }}
                onKeyDown={handleKeyDown}
                placeholder="Contraseña de administrador"
              />
            </div>
            {error && (
              <p style={{ fontSize: 12, color: 'var(--red)', marginTop: -8, marginBottom: 12, display: 'flex', alignItems: 'center', gap: 5 }}>
                <AlertTriangle size={12} /> {error}
              </p>
            )}
            <div className="modal-footer">
              <button
                className="btn btn-outline"
                onClick={() => { setShowLogin(false); setPassword(''); setError('') }}
              >
                <X size={13} /> Cancelar
              </button>
              <button className="btn btn-primary" onClick={handleLogin}>
                <ChevronRight size={13} /> Ingresar
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
