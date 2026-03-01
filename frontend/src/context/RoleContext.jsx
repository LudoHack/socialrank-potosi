/**
 * RoleContext — Controla el modo de la app: "admin" o "cliente"
 *
 * Modo ADMIN   → acceso completo: CRUD, subir Excel, gestión de proyectos
 * Modo CLIENTE → solo lectura: gráficos y análisis, sin botones de edición
 *
 * Contraseña por defecto: etnodb2026
 * (Cámbiala en la constante ADMIN_PASSWORD)
 */
import { createContext, useContext, useState } from 'react'

const ADMIN_PASSWORD = 'etnodb2026'

const RoleContext = createContext(null)

export function RoleProvider({ children }) {
  const [isAdmin, setIsAdmin] = useState(() =>
    localStorage.getItem('etno_role') === 'admin'
  )

  /** Intenta entrar en modo admin. Devuelve true si la contraseña es correcta. */
  const loginAdmin = (password) => {
    if (password === ADMIN_PASSWORD) {
      setIsAdmin(true)
      localStorage.setItem('etno_role', 'admin')
      return true
    }
    return false
  }

  /** Vuelve al modo cliente (solo lectura) */
  const logoutAdmin = () => {
    setIsAdmin(false)
    localStorage.removeItem('etno_role')
  }

  return (
    <RoleContext.Provider value={{ isAdmin, loginAdmin, logoutAdmin }}>
      {children}
    </RoleContext.Provider>
  )
}

export const useRole = () => useContext(RoleContext)
