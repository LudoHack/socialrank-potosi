import { createContext, useContext, useState, useEffect } from 'react'
import api from '../api/client'

const ProjectContext = createContext(null)

export function ProjectProvider({ children }) {
  const [projects, setProjects]       = useState([])
  const [activeProject, setActiveProject] = useState(null)
  const [loading, setLoading]         = useState(true)

  const loadProjects = async () => {
    try {
      const { data } = await api.get('/projects/')
      setProjects(data)
      // Restaurar proyecto activo desde localStorage
      const saved = localStorage.getItem('etno_active_project')
      if (saved) {
        const found = data.find(p => p.id === parseInt(saved))
        if (found) setActiveProject(found)
      } else if (data.length > 0) {
        setActiveProject(data[0])
      }
    } catch (e) {
      console.error('Error cargando proyectos', e)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadProjects() }, [])

  const selectProject = (project) => {
    setActiveProject(project)
    localStorage.setItem('etno_active_project', project.id)
  }

  return (
    <ProjectContext.Provider value={{ projects, activeProject, selectProject, loadProjects, loading }}>
      {children}
    </ProjectContext.Provider>
  )
}

export const useProject = () => useContext(ProjectContext)
