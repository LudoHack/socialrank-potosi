import { useState, useEffect } from 'react'
import api from '../api/client'
import { useProject } from '../context/ProjectContext'
import { useRole } from '../context/RoleContext'

const TIPO_BADGE = { activo: 'badge-green', polarizado: 'badge-red', amplificador: 'badge-yellow', silencioso: 'badge-gray' }
const PLATAFORMA_ICON = { 'Twitter/X': '🐦', Facebook: '👥', WhatsApp: '💬', TikTok: '🎵', Instagram: '📸', YouTube: '▶️', Radio: '📻', TV: '📺', Prensa: '📰', 'Boca a boca': '🗣️' }

export default function Comunidades() {
  const { activeProject } = useProject()
  const { isAdmin } = useRole()
  const [items, setItems]       = useState([])
  const [showForm, setShowForm] = useState(false)
  const [editItem, setEditItem] = useState(null)
  const [form, setForm] = useState({ plataforma: '', nombre_grupo: '', tipo: 'activo', tamanio_estimado: '', descripcion: '', influencia: 5 })

  const load = () => activeProject && api.get(`/communities/${activeProject.id}`).then(r => setItems(r.data)).catch(console.error)
  useEffect(() => { load() }, [activeProject])

  const openCreate = () => { setEditItem(null); setForm({ plataforma: '', nombre_grupo: '', tipo: 'activo', tamanio_estimado: '', descripcion: '', influencia: 5 }); setShowForm(true) }
  const openEdit   = (i) => { setEditItem(i); setForm({ plataforma: i.plataforma || '', nombre_grupo: i.nombre_grupo || '', tipo: i.tipo || 'activo', tamanio_estimado: i.tamanio_estimado || '', descripcion: i.descripcion || '', influencia: i.influencia || 5 }); setShowForm(true) }

  const save = async () => {
    if (!form.nombre_grupo) return alert('El nombre es obligatorio')
    const payload = { ...form, project_id: activeProject.id, tamanio_estimado: form.tamanio_estimado ? parseInt(form.tamanio_estimado) : null, influencia: parseInt(form.influencia) }
    if (editItem) await api.put(`/communities/${editItem.id}`, payload)
    else           await api.post('/communities/', payload)
    setShowForm(false); load()
  }
  const del = async (id) => { if (!confirm('¿Eliminar?')) return; await api.delete(`/communities/${id}`); load() }

  // Agrupar por plataforma
  const byPlataforma = items.reduce((acc, i) => { const k = i.plataforma || 'Otra'; (acc[k] = acc[k] || []).push(i); return acc }, {})

  if (!activeProject) return <div className="empty-state"><span className="icon">🗂️</span>Selecciona un proyecto.</div>

  return (
    <div>
      <div className="page-header">
        <div className="page-header-left">
          <h2>🌐 Comunidades Digitales</h2>
          <p>Grupos, plataformas y redes de influencia</p>
        </div>
        {isAdmin && (
          <button className="btn btn-primary" onClick={openCreate}>+ Nueva comunidad</button>
        )}
      </div>

      {Object.keys(byPlataforma).length > 0 && (
        <div className="grid-2" style={{ marginBottom: 20 }}>
          {Object.entries(byPlataforma).map(([plat, comms]) => (
            <div key={plat} className="card">
              <div className="card-title">{PLATAFORMA_ICON[plat] || '🌐'} {plat} ({comms.length})</div>
              {comms.map(c => (
                <div key={c.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 0', borderBottom: '1px solid var(--border)' }}>
                  <div>
                    <div style={{ fontSize: 13, fontWeight: 600 }}>{c.nombre_grupo}</div>
                    <div style={{ display: 'flex', gap: 6, marginTop: 3 }}>
                      <span className={`badge ${TIPO_BADGE[c.tipo] || 'badge-gray'}`}>{c.tipo}</span>
                      {c.tamanio_estimado && <span style={{ fontSize: 11, color: 'var(--muted)' }}>~{c.tamanio_estimado.toLocaleString()}</span>}
                    </div>
                    {c.descripcion && <p style={{ fontSize: 11, color: 'var(--muted)', marginTop: 4, maxWidth: 320 }}>{c.descripcion}</p>}
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontSize: 11, color: 'var(--muted)' }}>Influencia</div>
                      <div className="progress-bar" style={{ width: 50, marginTop: 3 }}>
                        <div className="progress-fill" style={{ width: `${c.influencia * 10}%` }} />
                      </div>
                    </div>
                    {isAdmin && (
                      <>
                        <button className="btn btn-outline btn-sm" onClick={() => openEdit(c)}>✎</button>
                        <button className="btn btn-danger btn-sm" onClick={() => del(c.id)}>✕</button>
                      </>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ))}
        </div>
      )}

      {!items.length && (
        <div className="empty-state">
          <span className="icon">🌐</span>
          {isAdmin ? 'Sin comunidades registradas. Mapea los grupos digitales relevantes.' : 'Sin comunidades digitales registradas para este proyecto.'}
        </div>
      )}

      {/* Modal (solo admin) */}
      {isAdmin && (
        <div className={`modal-overlay ${showForm ? 'open' : ''}`} onClick={e => e.target.className.includes('modal-overlay') && setShowForm(false)}>
          <div className="modal">
            <h3>{editItem ? 'Editar comunidad' : 'Nueva comunidad digital'}</h3>
            <div className="form-row">
              <div className="form-group">
                <label>Plataforma</label>
                <select value={form.plataforma} onChange={e => setForm({ ...form, plataforma: e.target.value })}>
                  <option value="">Otra</option>
                  {Object.keys(PLATAFORMA_ICON).map(p => <option key={p} value={p}>{PLATAFORMA_ICON[p]} {p}</option>)}
                </select>
              </div>
              <div className="form-group">
                <label>Nombre del grupo *</label>
                <input value={form.nombre_grupo} onChange={e => setForm({ ...form, nombre_grupo: e.target.value })} placeholder="Ej: Padres por la educación" />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Tipo</label>
                <select value={form.tipo} onChange={e => setForm({ ...form, tipo: e.target.value })}>
                  <option value="activo">Activo</option>
                  <option value="polarizado">Polarizado</option>
                  <option value="amplificador">Amplificador</option>
                  <option value="silencioso">Silencioso</option>
                </select>
              </div>
              <div className="form-group">
                <label>Tamaño estimado</label>
                <input type="number" min={0} value={form.tamanio_estimado} onChange={e => setForm({ ...form, tamanio_estimado: e.target.value })} placeholder="N° de miembros" />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Influencia (1–10)</label>
                <input type="number" min={1} max={10} value={form.influencia} onChange={e => setForm({ ...form, influencia: e.target.value })} />
              </div>
            </div>
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label>Descripción</label>
              <textarea value={form.descripcion} onChange={e => setForm({ ...form, descripcion: e.target.value })} placeholder="Características del grupo, comportamiento, temas habituales..." />
            </div>
            <div className="modal-footer">
              <button className="btn btn-outline" onClick={() => setShowForm(false)}>Cancelar</button>
              <button className="btn btn-primary" onClick={save}>Guardar</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
