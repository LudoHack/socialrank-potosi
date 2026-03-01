import { useState } from 'react'
import api from '../api/client'
import { useProject } from '../context/ProjectContext'
import { useRole } from '../context/RoleContext'
import ExcelUpload from '../components/Upload/ExcelUpload'

export default function Proyectos() {
  const { projects, activeProject, selectProject, loadProjects } = useProject()
  const { isAdmin } = useRole()

  const [showForm, setShowForm]     = useState(false)
  const [showUpload, setShowUpload] = useState(null) // project id
  const [editItem, setEditItem]     = useState(null)
  const [form, setForm] = useState({ nombre: '', cliente: '', contexto_pais: '', fecha_inicio: '', descripcion: '' })
  const [saving, setSaving] = useState(false)

  if (!isAdmin) {
    return (
      <div className="empty-state" style={{ marginTop: 60 }}>
        <span className="icon">🔐</span>
        <p style={{ marginTop: 10, color: 'var(--muted)', fontSize: 14 }}>
          Esta sección es exclusiva de administradores.<br />
          Usa el botón <strong>🔐 Admin</strong> en el menú lateral para ingresar.
        </p>
      </div>
    )
  }

  const openCreate = () => {
    setEditItem(null)
    setForm({ nombre: '', cliente: '', contexto_pais: '', fecha_inicio: '', descripcion: '' })
    setShowForm(true)
  }
  const openEdit = (p) => {
    setEditItem(p)
    setForm({ nombre: p.nombre, cliente: p.cliente || '', contexto_pais: p.contexto_pais || '', fecha_inicio: p.fecha_inicio || '', descripcion: p.descripcion || '' })
    setShowForm(true)
  }

  const saveProject = async () => {
    if (!form.nombre) return alert('El nombre es obligatorio')
    setSaving(true)
    try {
      if (editItem) await api.put(`/projects/${editItem.id}`, form)
      else           await api.post('/projects/', form)
      await loadProjects()
      setShowForm(false)
    } catch (e) { alert(e.message) }
    finally { setSaving(false) }
  }

  const deleteProject = async (id) => {
    if (!confirm('¿Eliminar este proyecto y todos sus datos?')) return
    await api.delete(`/projects/${id}`)
    await loadProjects()
  }

  return (
    <div>
      <div className="page-header">
        <div className="page-header-left">
          <h2>🗂️ Proyectos</h2>
          <p>Gestión de proyectos de investigación etnográfica</p>
        </div>
        <button className="btn btn-primary" onClick={openCreate}>+ Nuevo proyecto</button>
      </div>

      <div style={{ display: 'grid', gap: 16 }}>
        {projects.map(p => (
          <div
            key={p.id}
            className="card"
            style={{ borderLeft: activeProject?.id === p.id ? '3px solid var(--accent)' : '3px solid transparent' }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 10 }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <h3 style={{ fontSize: 16, fontWeight: 700 }}>{p.nombre}</h3>
                  {activeProject?.id === p.id && <span className="badge badge-purple">Activo</span>}
                </div>
                {p.cliente && (
                  <p style={{ fontSize: 13, color: 'var(--muted)', marginTop: 2 }}>
                    {p.cliente} {p.contexto_pais && `· ${p.contexto_pais}`}
                  </p>
                )}
                {p.descripcion && (
                  <p style={{ fontSize: 12, color: 'var(--muted)', marginTop: 6, maxWidth: 500 }}>
                    {p.descripcion}
                  </p>
                )}
                <div style={{ display: 'flex', gap: 10, marginTop: 10, flexWrap: 'wrap' }}>
                  <span className="badge badge-purple">📖 {p.stats?.narrativas} narrativas</span>
                  <span className="badge badge-teal">🎭 {p.stats?.emociones} emociones</span>
                  <span className="badge badge-yellow">👤 {p.stats?.arquetipos} arquetipos</span>
                  {p.stats?.riesgos_activos > 0 && (
                    <span className="badge badge-red">⚠️ {p.stats.riesgos_activos} riesgos</span>
                  )}
                </div>
              </div>

              <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                <button className="btn btn-teal btn-sm" onClick={() => selectProject(p)}>Activar</button>
                <button className="btn btn-outline btn-sm" onClick={() => setShowUpload(p.id)}>📂 Subir Excel</button>
                <button className="btn btn-outline btn-sm" onClick={() => openEdit(p)}>Editar</button>
                <button className="btn btn-danger btn-sm" onClick={() => deleteProject(p.id)}>✕</button>
              </div>
            </div>

            {showUpload === p.id && (
              <div style={{ marginTop: 16, borderTop: '1px solid var(--border)', paddingTop: 16 }}>
                <ExcelUpload projectId={p.id} onSuccess={() => { loadProjects(); setShowUpload(null) }} />
                <button className="btn btn-outline btn-sm" onClick={() => setShowUpload(null)}>Cerrar</button>
              </div>
            )}
          </div>
        ))}
        {!projects.length && (
          <div className="empty-state">
            <span className="icon">🗂️</span>Sin proyectos. Crea el primero.
          </div>
        )}
      </div>

      {/* Modal nuevo/editar proyecto */}
      <div
        className={`modal-overlay ${showForm ? 'open' : ''}`}
        onClick={e => e.target.className.includes('modal-overlay') && setShowForm(false)}
      >
        <div className="modal">
          <h3>{editItem ? 'Editar proyecto' : 'Nuevo proyecto'}</h3>
          <div className="form-row">
            <div className="form-group">
              <label>Nombre del proyecto *</label>
              <input value={form.nombre} onChange={e => setForm({ ...form, nombre: e.target.value })} placeholder="Ej: Elecciones Municipales 2026" />
            </div>
            <div className="form-group">
              <label>Cliente</label>
              <input value={form.cliente} onChange={e => setForm({ ...form, cliente: e.target.value })} placeholder="Nombre del cliente" />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>País / región</label>
              <input value={form.contexto_pais} onChange={e => setForm({ ...form, contexto_pais: e.target.value })} placeholder="Ej: Chile" />
            </div>
            <div className="form-group">
              <label>Fecha de inicio</label>
              <input type="date" value={form.fecha_inicio} onChange={e => setForm({ ...form, fecha_inicio: e.target.value })} />
            </div>
          </div>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label>Descripción / objetivo</label>
            <textarea value={form.descripcion} onChange={e => setForm({ ...form, descripcion: e.target.value })} placeholder="Objetivo de la investigación..." />
          </div>
          <div className="modal-footer">
            <button className="btn btn-outline" onClick={() => setShowForm(false)}>Cancelar</button>
            <button className="btn btn-primary" onClick={saveProject} disabled={saving}>
              {saving ? 'Guardando...' : 'Guardar'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
