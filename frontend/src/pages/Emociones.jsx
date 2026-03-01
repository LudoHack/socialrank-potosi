import { useState, useEffect } from 'react'
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer,
         BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell } from 'recharts'
import api from '../api/client'
import { useProject } from '../context/ProjectContext'
import { useRole } from '../context/RoleContext'

const TIPOS = ['ira', 'miedo', 'frustracion', 'esperanza', 'desconfianza', 'orgullo']
const COLORS = { ira: '#f76c6c', miedo: '#f7c948', frustracion: '#f7964a', esperanza: '#56c596', desconfianza: '#a78bfa', orgullo: '#4ecdc4' }

export default function Emociones() {
  const { activeProject } = useProject()
  const { isAdmin } = useRole()
  const [items, setItems]       = useState([])
  const [radar, setRadar]       = useState([])
  const [showForm, setShowForm] = useState(false)
  const [editItem, setEditItem] = useState(null)
  const [form, setForm] = useState({ tipo: 'ira', intensidad: 5, fuente: '', fecha: '', notas: '' })

  const load = () => {
    if (!activeProject) return
    api.get(`/emotions/${activeProject.id}`).then(r => setItems(r.data)).catch(console.error)
    api.get(`/emotions/${activeProject.id}/radar`).then(r => setRadar(r.data)).catch(console.error)
  }
  useEffect(() => { load() }, [activeProject])

  const openCreate = () => { setEditItem(null); setForm({ tipo: 'ira', intensidad: 5, fuente: '', fecha: '', notas: '' }); setShowForm(true) }
  const openEdit   = (i) => { setEditItem(i); setForm({ tipo: i.tipo, intensidad: i.intensidad, fuente: i.fuente || '', fecha: i.fecha || '', notas: i.notas || '' }); setShowForm(true) }

  const save = async () => {
    const payload = { ...form, project_id: activeProject.id, intensidad: parseFloat(form.intensidad) }
    if (editItem) await api.put(`/emotions/${editItem.id}`, payload)
    else           await api.post('/emotions/', payload)
    setShowForm(false); load()
  }
  const del = async (id) => { if (!confirm('¿Eliminar?')) return; await api.delete(`/emotions/${id}`); load() }

  if (!activeProject) return <div className="empty-state"><span className="icon">🗂️</span>Selecciona un proyecto.</div>

  return (
    <div>
      <div className="page-header">
        <div className="page-header-left">
          <h2>🎭 Módulo Emocional</h2>
          <p>Análisis avanzado del clima emocional colectivo</p>
        </div>
        {isAdmin && (
          <button className="btn btn-primary" onClick={openCreate}>+ Nuevo registro</button>
        )}
      </div>

      <div className="grid-2" style={{ marginBottom: 20 }}>
        <div className="card">
          <div className="card-title">Radar emocional promedio</div>
          {radar.some(r => r.valor > 0) ? (
            <ResponsiveContainer width="100%" height={240}>
              <RadarChart data={radar}>
                <PolarGrid stroke="#3a3f5c" />
                <PolarAngleAxis dataKey="tipo" tick={{ fill: '#8b92b8', fontSize: 12 }} />
                <Radar dataKey="valor" stroke="#a78bfa" fill="#a78bfa" fillOpacity={0.45}
                  dot={{ fill: '#a78bfa', r: 4 }} />
                <Tooltip contentStyle={{ background: '#1a1d27', border: '1px solid #3a3f5c', borderRadius: 8 }} labelStyle={{ color: '#e8eaf6', fontWeight: 600 }} itemStyle={{ color: '#c8cde8' }} />
              </RadarChart>
            </ResponsiveContainer>
          ) : <div className="empty-state" style={{ padding: 20 }}><span className="icon" style={{ fontSize: 28 }}>🎭</span>Sin datos aún</div>}
        </div>

        <div className="card">
          <div className="card-title">Intensidades actuales</div>
          {radar.some(r => r.valor > 0) ? (
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={radar} layout="vertical" margin={{ left: 0, right: 20, top: 5, bottom: 5 }}>
                <CartesianGrid horizontal={false} stroke="#3a3f5c" />
                <XAxis type="number" domain={[0, 10]} tick={{ fill: '#8b92b8', fontSize: 11 }} />
                <YAxis type="category" dataKey="tipo" tick={{ fill: '#e8eaf6', fontSize: 11 }} width={95} />
                <Tooltip contentStyle={{ background: '#1a1d27', border: '1px solid #3a3f5c', borderRadius: 8 }} labelStyle={{ color: '#e8eaf6', fontWeight: 600 }} itemStyle={{ color: '#c8cde8' }} />
                <Bar dataKey="valor" radius={[0, 4, 4, 0]} barSize={18}>
                  {radar.map((r, i) => <Cell key={i} fill={COLORS[r.tipo] || '#a78bfa'} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : <div className="empty-state" style={{ padding: 20 }}><span className="icon" style={{ fontSize: 28 }}>📊</span>Sin datos</div>}
        </div>
      </div>

      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Emoción</th>
              <th>Intensidad</th>
              <th>Fuente</th>
              <th>Fecha</th>
              <th>Notas</th>
              {isAdmin && <th></th>}
            </tr>
          </thead>
          <tbody>
            {items.map(i => (
              <tr key={i.id}>
                <td>
                  <span className="badge" style={{ background: `${COLORS[i.tipo]}22`, color: COLORS[i.tipo] || 'var(--accent)' }}>{i.tipo}</span>
                </td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    <div className="progress-bar" style={{ width: 70 }}>
                      <div className="progress-fill" style={{ width: `${i.intensidad * 10}%`, background: COLORS[i.tipo] || 'var(--accent)' }} />
                    </div>
                    <span style={{ fontSize: 12, fontWeight: 700, color: COLORS[i.tipo] }}>{i.intensidad}</span>
                  </div>
                </td>
                <td style={{ fontSize: 12, color: 'var(--muted)' }}>{i.fuente || '—'}</td>
                <td style={{ fontSize: 12, color: 'var(--muted)' }}>{i.fecha || '—'}</td>
                <td style={{ fontSize: 12, color: 'var(--muted)', maxWidth: 200 }}>{i.notas || '—'}</td>
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
        {!items.length && (
          <div className="empty-state">
            <span className="icon">🎭</span>
            {isAdmin ? 'Sin registros emocionales. Agrega el primero o importa desde Excel.' : 'Sin registros emocionales para este proyecto.'}
          </div>
        )}
      </div>

      {/* Modal (solo admin) */}
      {isAdmin && (
        <div className={`modal-overlay ${showForm ? 'open' : ''}`} onClick={e => e.target.className.includes('modal-overlay') && setShowForm(false)}>
          <div className="modal">
            <h3>{editItem ? 'Editar emoción' : 'Nuevo registro emocional'}</h3>
            <div className="form-row">
              <div className="form-group">
                <label>Emoción *</label>
                <select value={form.tipo} onChange={e => setForm({ ...form, tipo: e.target.value })}>
                  {TIPOS.map(t => <option key={t} value={t}>{t.charAt(0).toUpperCase() + t.slice(1)}</option>)}
                </select>
              </div>
              <div className="form-group">
                <label>Intensidad (1–10)</label>
                <input type="number" min={1} max={10} step={0.5} value={form.intensidad} onChange={e => setForm({ ...form, intensidad: e.target.value })} />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Fuente</label>
                <input value={form.fuente} onChange={e => setForm({ ...form, fuente: e.target.value })} placeholder="Ej: Twitter/X, Facebook, Instagram, TikTok, Telegram..." />
              </div>
              <div className="form-group">
                <label>Fecha</label>
                <input type="date" value={form.fecha} onChange={e => setForm({ ...form, fecha: e.target.value })} />
              </div>
            </div>
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label>Notas</label>
              <textarea value={form.notas} onChange={e => setForm({ ...form, notas: e.target.value })} placeholder="Observaciones sobre este registro emocional..." />
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
