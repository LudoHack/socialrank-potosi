import { useState, useEffect } from 'react'
import api from '../api/client'
import { useProject } from '../context/ProjectContext'
import { useRole } from '../context/RoleContext'

const TIPO_BADGE = { dominante: 'badge-red', emergente: 'badge-yellow', contrarrelato: 'badge-teal' }

export default function Narrativas() {
  const { activeProject } = useProject()
  const { isAdmin } = useRole()
  const [items, setItems]       = useState([])
  const [showForm, setShowForm] = useState(false)
  const [editItem, setEditItem] = useState(null)
  const [search, setSearch]     = useState('')
  const [filter, setFilter]     = useState('')
  const [form, setForm] = useState({ texto: '', tipo: 'dominante', actor_politico: '', fecha_deteccion: '', peso: 5 })

  const load = () => activeProject && api.get(`/narratives/${activeProject.id}`).then(r => setItems(r.data)).catch(console.error)
  useEffect(() => { load() }, [activeProject])

  const openCreate = () => { setEditItem(null); setForm({ texto: '', tipo: 'dominante', actor_politico: '', fecha_deteccion: '', peso: 5 }); setShowForm(true) }
  const openEdit   = (i) => { setEditItem(i); setForm({ texto: i.texto, tipo: i.tipo || 'dominante', actor_politico: i.actor_politico || '', fecha_deteccion: i.fecha_deteccion || '', peso: i.peso || 5 }); setShowForm(true) }

  const save = async () => {
    if (!form.texto) return alert('El texto es obligatorio')
    const payload = { ...form, project_id: activeProject.id, peso: parseFloat(form.peso) }
    if (editItem) await api.put(`/narratives/${editItem.id}`, payload)
    else           await api.post('/narratives/', payload)
    setShowForm(false); load()
  }
  const del = async (id) => { if (!confirm('¿Eliminar?')) return; await api.delete(`/narratives/${id}`); load() }

  const filtered = items.filter(i =>
    (!filter || i.tipo === filter) &&
    (!search || i.texto.toLowerCase().includes(search.toLowerCase()) || (i.actor_politico || '').toLowerCase().includes(search.toLowerCase()))
  )

  if (!activeProject) return <div className="empty-state"><span className="icon">🗂️</span>Selecciona un proyecto primero.</div>

  return (
    <div>
      <div className="page-header">
        <div className="page-header-left">
          <h2>📖 Narrativas y Relatos</h2>
          <p>Historias dominantes, emergentes y contrarrelatos en circulación</p>
        </div>
        {isAdmin && (
          <button className="btn btn-primary" onClick={openCreate}>+ Nueva narrativa</button>
        )}
      </div>

      <div style={{ display: 'flex', gap: 10, marginBottom: 16, flexWrap: 'wrap' }}>
        <input style={{ flex: 1, minWidth: 200 }} placeholder="🔍 Buscar narrativa..." value={search} onChange={e => setSearch(e.target.value)} />
        <select value={filter} onChange={e => setFilter(e.target.value)} style={{ minWidth: 160 }}>
          <option value="">Todos los tipos</option>
          <option value="dominante">Dominante</option>
          <option value="emergente">Emergente</option>
          <option value="contrarrelato">Contrarrelato</option>
        </select>
      </div>

      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Narrativa</th>
              <th>Tipo</th>
              <th>Actor</th>
              <th>Fecha</th>
              <th>Peso</th>
              {isAdmin && <th></th>}
            </tr>
          </thead>
          <tbody>
            {filtered.map(i => (
              <tr key={i.id}>
                <td style={{ maxWidth: 350 }}>
                  <div style={{ fontWeight: 600, marginBottom: 2 }}>
                    {i.texto.slice(0, 100)}{i.texto.length > 100 ? '…' : ''}
                  </div>
                </td>
                <td><span className={`badge ${TIPO_BADGE[i.tipo] || 'badge-gray'}`}>{i.tipo}</span></td>
                <td style={{ color: 'var(--muted)', fontSize: 12 }}>{i.actor_politico || '—'}</td>
                <td style={{ color: 'var(--muted)', fontSize: 12 }}>{i.fecha_deteccion || '—'}</td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <div className="progress-bar" style={{ width: 60 }}>
                      <div className="progress-fill" style={{ width: `${i.peso * 10}%` }} />
                    </div>
                    <span style={{ fontSize: 11, color: 'var(--muted)' }}>{i.peso}</span>
                  </div>
                </td>
                {isAdmin && (
                  <td style={{ whiteSpace: 'nowrap' }}>
                    <button className="btn btn-outline btn-sm" onClick={() => openEdit(i)}>Editar</button>{' '}
                    <button className="btn btn-danger btn-sm" onClick={() => del(i.id)}>✕</button>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
        {!filtered.length && (
          <div className="empty-state">
            <span className="icon">📖</span>
            {isAdmin ? 'Sin narrativas registradas. Agrega la primera o sube un Excel.' : 'Sin narrativas registradas para este proyecto.'}
          </div>
        )}
      </div>

      {/* Modal (solo admin) */}
      {isAdmin && (
        <div className={`modal-overlay ${showForm ? 'open' : ''}`} onClick={e => e.target.className.includes('modal-overlay') && setShowForm(false)}>
          <div className="modal" style={{ maxWidth: 600 }}>
            <h3>{editItem ? 'Editar narrativa' : 'Nueva narrativa'}</h3>
            <div className="form-group" style={{ marginBottom: 12 }}>
              <label>Texto de la narrativa *</label>
              <textarea rows={4} value={form.texto} onChange={e => setForm({ ...form, texto: e.target.value })} placeholder="Describe la narrativa en circulación..." />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Tipo</label>
                <select value={form.tipo} onChange={e => setForm({ ...form, tipo: e.target.value })}>
                  <option value="dominante">Dominante</option>
                  <option value="emergente">Emergente</option>
                  <option value="contrarrelato">Contrarrelato</option>
                </select>
              </div>
              <div className="form-group">
                <label>Actor político</label>
                <input value={form.actor_politico} onChange={e => setForm({ ...form, actor_politico: e.target.value })} placeholder="Candidato / grupo / medio..." />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Fecha de detección</label>
                <input type="date" value={form.fecha_deteccion} onChange={e => setForm({ ...form, fecha_deteccion: e.target.value })} />
              </div>
              <div className="form-group">
                <label>Peso / relevancia (1–10)</label>
                <input type="number" min={1} max={10} step={0.5} value={form.peso} onChange={e => setForm({ ...form, peso: e.target.value })} />
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
