import { useState, useEffect } from 'react'
import api from '../api/client'
import { useProject } from '../context/ProjectContext'
import { useRole } from '../context/RoleContext'

const EMOC_COLOR = { ira: '#f76c6c', miedo: '#f7c948', frustracion: '#f7964a', esperanza: '#56c596', desconfianza: '#a78bfa', orgullo: '#4ecdc4' }
const CANALES_LIST = ['Twitter/X', 'Facebook', 'WhatsApp', 'TikTok', 'Instagram', 'YouTube', 'Radio', 'TV', 'Prensa', 'Boca a boca']

export default function Arquetipos() {
  const { activeProject } = useProject()
  const { isAdmin } = useRole()
  const [items, setItems]       = useState([])
  const [showForm, setShowForm] = useState(false)
  const [editItem, setEditItem] = useState(null)
  const [form, setForm] = useState({ nombre: '', descripcion: '', peso_relativo: 0, emocion_dominante: '', canales: [], valores_clave: '', miedos: '' })

  const load = () => activeProject && api.get(`/archetypes/${activeProject.id}`).then(r => setItems(r.data)).catch(console.error)
  useEffect(() => { load() }, [activeProject])

  const openCreate = () => { setEditItem(null); setForm({ nombre: '', descripcion: '', peso_relativo: 0, emocion_dominante: '', canales: [], valores_clave: '', miedos: '' }); setShowForm(true) }
  const openEdit   = (i) => { setEditItem(i); setForm({ nombre: i.nombre, descripcion: i.descripcion || '', peso_relativo: i.peso_relativo || 0, emocion_dominante: i.emocion_dominante || '', canales: i.canales || [], valores_clave: i.valores_clave || '', miedos: i.miedos || '' }); setShowForm(true) }

  const toggleCanal = (c) => setForm(f => ({ ...f, canales: f.canales.includes(c) ? f.canales.filter(x => x !== c) : [...f.canales, c] }))

  const save = async () => {
    if (!form.nombre) return alert('El nombre es obligatorio')
    const payload = { ...form, project_id: activeProject.id, peso_relativo: parseFloat(form.peso_relativo) }
    if (editItem) await api.put(`/archetypes/${editItem.id}`, payload)
    else           await api.post('/archetypes/', payload)
    setShowForm(false); load()
  }
  const del = async (id) => { if (!confirm('¿Eliminar?')) return; await api.delete(`/archetypes/${id}`); load() }

  const totalPeso = items.reduce((s, i) => s + (i.peso_relativo || 0), 0)

  if (!activeProject) return <div className="empty-state"><span className="icon">🗂️</span>Selecciona un proyecto.</div>

  return (
    <div>
      <div className="page-header">
        <div className="page-header-left">
          <h2>👤 Arquetipos</h2>
          <p>Perfiles culturales del votante / audiencia objetivo</p>
        </div>
        {isAdmin && (
          <button className="btn btn-primary" onClick={openCreate}>+ Nuevo arquetipo</button>
        )}
      </div>

      {totalPeso > 0 && (
        <div className="card" style={{ marginBottom: 20 }}>
          <div className="card-title">Distribución del público ({totalPeso.toFixed(0)}% mapeado)</div>
          <div style={{ display: 'flex', height: 24, borderRadius: 6, overflow: 'hidden', gap: 2 }}>
            {items.map((a, i) => (
              <div key={i} title={`${a.nombre}: ${a.peso_relativo}%`}
                style={{ flex: a.peso_relativo, background: EMOC_COLOR[a.emocion_dominante] || `hsl(${i * 60},60%,55%)`, minWidth: a.peso_relativo > 2 ? undefined : 0, transition: 'flex .3s' }} />
            ))}
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginTop: 10 }}>
            {items.map((a, i) => (
              <span key={i} style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 11 }}>
                <span style={{ width: 10, height: 10, borderRadius: 50, background: EMOC_COLOR[a.emocion_dominante] || `hsl(${i * 60},60%,55%)`, display: 'inline-block' }} />
                {a.nombre} ({a.peso_relativo}%)
              </span>
            ))}
          </div>
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(300px,1fr))', gap: 16 }}>
        {items.map(a => (
          <div key={a.id} className="card" style={{ borderTop: `3px solid ${EMOC_COLOR[a.emocion_dominante] || 'var(--accent)'}` }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 10 }}>
              <div>
                <h3 style={{ fontSize: 15, fontWeight: 700 }}>{a.nombre}</h3>
                <span style={{ fontSize: 11, color: EMOC_COLOR[a.emocion_dominante] || 'var(--muted)' }}>
                  {a.emocion_dominante || '—'} · {a.peso_relativo}%
                </span>
              </div>
              {isAdmin && (
                <div style={{ display: 'flex', gap: 6 }}>
                  <button className="btn btn-outline btn-sm" onClick={() => openEdit(a)}>✎</button>
                  <button className="btn btn-danger btn-sm" onClick={() => del(a.id)}>✕</button>
                </div>
              )}
            </div>
            {a.descripcion && <p style={{ fontSize: 12, color: 'var(--muted)', marginBottom: 10 }}>{a.descripcion}</p>}
            {a.valores_clave && (
              <div style={{ marginBottom: 6 }}>
                <span style={{ fontSize: 11, color: 'var(--accent)', fontWeight: 600 }}>VALORES: </span>
                <span style={{ fontSize: 12 }}>{a.valores_clave}</span>
              </div>
            )}
            {a.miedos && (
              <div style={{ marginBottom: 8 }}>
                <span style={{ fontSize: 11, color: 'var(--accent4)', fontWeight: 600 }}>MIEDOS: </span>
                <span style={{ fontSize: 12 }}>{a.miedos}</span>
              </div>
            )}
            {(a.canales || []).length > 0 && (
              <div className="tag-list">
                {(a.canales || []).map((c, i) => <span key={i} className="tag">{c}</span>)}
              </div>
            )}
          </div>
        ))}
      </div>
      {!items.length && (
        <div className="empty-state">
          <span className="icon">👤</span>
          {isAdmin ? 'Sin arquetipos. Define los perfiles de tu audiencia.' : 'Sin arquetipos definidos para este proyecto.'}
        </div>
      )}

      {/* Modal (solo admin) */}
      {isAdmin && (
        <div className={`modal-overlay ${showForm ? 'open' : ''}`} onClick={e => e.target.className.includes('modal-overlay') && setShowForm(false)}>
          <div className="modal" style={{ maxWidth: 580 }}>
            <h3>{editItem ? 'Editar arquetipo' : 'Nuevo arquetipo'}</h3>
            <div className="form-row">
              <div className="form-group">
                <label>Nombre *</label>
                <input value={form.nombre} onChange={e => setForm({ ...form, nombre: e.target.value })} placeholder="Ej: El desencantado urbano" />
              </div>
              <div className="form-group">
                <label>% del público</label>
                <input type="number" min={0} max={100} value={form.peso_relativo} onChange={e => setForm({ ...form, peso_relativo: e.target.value })} />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Emoción dominante</label>
                <select value={form.emocion_dominante} onChange={e => setForm({ ...form, emocion_dominante: e.target.value })}>
                  <option value="">—</option>
                  {Object.keys(EMOC_COLOR).map(t => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>
            </div>
            <div className="form-group" style={{ marginBottom: 12 }}>
              <label>Descripción</label>
              <textarea value={form.descripcion} onChange={e => setForm({ ...form, descripcion: e.target.value })} placeholder="Quién es este arquetipo..." />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Valores clave</label>
                <input value={form.valores_clave} onChange={e => setForm({ ...form, valores_clave: e.target.value })} placeholder="Seguridad, familia, trabajo..." />
              </div>
              <div className="form-group">
                <label>Miedos</label>
                <input value={form.miedos} onChange={e => setForm({ ...form, miedos: e.target.value })} placeholder="Desempleo, inseguridad..." />
              </div>
            </div>
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label>Canales de comunicación</label>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 4 }}>
                {CANALES_LIST.map(c => (
                  <button key={c} type="button"
                    className={`btn btn-sm ${form.canales.includes(c) ? 'btn-primary' : 'btn-outline'}`}
                    onClick={() => toggleCanal(c)}>{c}</button>
                ))}
              </div>
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
