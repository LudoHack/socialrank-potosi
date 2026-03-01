import { useState, useEffect } from 'react'
import api from '../api/client'
import { useProject } from '../context/ProjectContext'
import { useRole } from '../context/RoleContext'

const NIVEL_STYLE = {
  rojo:     { dot: 'dot-rojo',    badge: 'badge-red',    label: '🔴 CRÍTICO',  bg: 'rgba(247,108,108,.08)', border: 'var(--accent4)' },
  amarillo: { dot: 'dot-amarillo',badge: 'badge-yellow', label: '🟡 ATENCIÓN', bg: 'rgba(247,201,72,.08)',  border: 'var(--accent3)' },
  verde:    { dot: 'dot-verde',   badge: 'badge-green',  label: '🟢 BAJO',     bg: 'rgba(86,197,150,.08)',  border: 'var(--success)' },
}

export default function Riesgos() {
  const { activeProject } = useProject()
  const { isAdmin } = useRole()
  const [items, setItems]       = useState([])
  const [showForm, setShowForm] = useState(false)
  const [editItem, setEditItem] = useState(null)
  const [form, setForm] = useState({ tema: '', descripcion: '', nivel: 'amarillo', velocidad_crecimiento: 3, fecha_deteccion: '', activo: true })

  const load = () => activeProject && api.get(`/risks/${activeProject.id}`).then(r => setItems(r.data)).catch(console.error)
  useEffect(() => { load() }, [activeProject])

  const openCreate = () => { setEditItem(null); setForm({ tema: '', descripcion: '', nivel: 'amarillo', velocidad_crecimiento: 3, fecha_deteccion: '', activo: true }); setShowForm(true) }
  const openEdit   = (i) => { setEditItem(i); setForm({ tema: i.tema, descripcion: i.descripcion || '', nivel: i.nivel || 'amarillo', velocidad_crecimiento: i.velocidad_crecimiento || 3, fecha_deteccion: i.fecha_deteccion || '', activo: i.activo }); setShowForm(true) }

  const save = async () => {
    if (!form.tema) return alert('El tema es obligatorio')
    const payload = { ...form, project_id: activeProject.id, velocidad_crecimiento: parseInt(form.velocidad_crecimiento) }
    if (editItem) await api.put(`/risks/${editItem.id}`, payload)
    else           await api.post('/risks/', payload)
    setShowForm(false); load()
  }
  const del = async (id) => { if (!confirm('¿Eliminar?')) return; await api.delete(`/risks/${id}`); load() }

  const rojos     = items.filter(i => i.nivel === 'rojo')
  const amarillos = items.filter(i => i.nivel === 'amarillo')
  const verdes    = items.filter(i => i.nivel === 'verde')

  const RiskCard = ({ r }) => {
    const s = NIVEL_STYLE[r.nivel] || NIVEL_STYLE.amarillo
    return (
      <div style={{ background: s.bg, border: `1px solid ${s.border}`, borderRadius: 10, padding: 14, marginBottom: 10 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div style={{ flex: 1 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
              <span className={s.dot} />
              <span style={{ fontWeight: 700, fontSize: 14 }}>{r.tema}</span>
            </div>
            {r.descripcion && <p style={{ fontSize: 12, color: 'var(--muted)', marginBottom: 6 }}>{r.descripcion}</p>}
            <div style={{ display: 'flex', gap: 10, alignItems: 'center', flexWrap: 'wrap' }}>
              <span style={{ fontSize: 11, color: 'var(--muted)' }}>Velocidad: {'🔥'.repeat(r.velocidad_crecimiento || 0)}</span>
              {r.fecha_deteccion && <span style={{ fontSize: 11, color: 'var(--muted)' }}>📅 {r.fecha_deteccion}</span>}
            </div>
          </div>
          {isAdmin && (
            <div style={{ display: 'flex', gap: 6, flexShrink: 0 }}>
              <button className="btn btn-outline btn-sm" onClick={() => openEdit(r)}>✎</button>
              <button className="btn btn-danger btn-sm" onClick={() => del(r.id)}>✕</button>
            </div>
          )}
        </div>
      </div>
    )
  }

  if (!activeProject) return <div className="empty-state"><span className="icon">🗂️</span>Selecciona un proyecto.</div>

  return (
    <div>
      <div className="page-header">
        <div className="page-header-left">
          <h2>⚠️ Riesgos y Crisis</h2>
          <p>Semáforo de amenazas activas al discurso</p>
        </div>
        {isAdmin && (
          <button className="btn btn-primary" onClick={openCreate}>+ Nuevo riesgo</button>
        )}
      </div>

      {/* Resumen semáforo */}
      <div className="stats-grid" style={{ marginBottom: 20 }}>
        <div className="stat-card" style={{ borderLeft: '3px solid var(--accent4)' }}>
          <div className="label">🔴 Críticos</div>
          <div className="value" style={{ color: 'var(--accent4)' }}>{rojos.length}</div>
          <div className="sub">acción inmediata</div>
        </div>
        <div className="stat-card" style={{ borderLeft: '3px solid var(--accent3)' }}>
          <div className="label">🟡 En atención</div>
          <div className="value" style={{ color: 'var(--accent3)' }}>{amarillos.length}</div>
          <div className="sub">monitoreo cercano</div>
        </div>
        <div className="stat-card" style={{ borderLeft: '3px solid var(--success)' }}>
          <div className="label">🟢 Controlados</div>
          <div className="value" style={{ color: 'var(--success)' }}>{verdes.length}</div>
          <div className="sub">bajo control</div>
        </div>
      </div>

      <div className="grid-2">
        <div>
          {rojos.length > 0 && (
            <div className="card" style={{ marginBottom: 16, borderLeft: '3px solid var(--accent4)' }}>
              <div className="card-title">🔴 Riesgos críticos</div>
              {rojos.map(r => <RiskCard key={r.id} r={r} />)}
            </div>
          )}
          {amarillos.length > 0 && (
            <div className="card" style={{ borderLeft: '3px solid var(--accent3)' }}>
              <div className="card-title">🟡 En atención</div>
              {amarillos.map(r => <RiskCard key={r.id} r={r} />)}
            </div>
          )}
        </div>
        <div>
          {verdes.length > 0 && (
            <div className="card" style={{ borderLeft: '3px solid var(--success)' }}>
              <div className="card-title">🟢 Controlados</div>
              {verdes.map(r => <RiskCard key={r.id} r={r} />)}
            </div>
          )}
        </div>
      </div>
      {!items.length && (
        <div className="empty-state">
          <span className="icon">✅</span>
          {isAdmin ? 'Sin riesgos registrados.' : '¡Sin riesgos activos en este momento!'}
        </div>
      )}

      {/* Modal (solo admin) */}
      {isAdmin && (
        <div className={`modal-overlay ${showForm ? 'open' : ''}`} onClick={e => e.target.className.includes('modal-overlay') && setShowForm(false)}>
          <div className="modal">
            <h3>{editItem ? 'Editar riesgo' : 'Nuevo riesgo / crisis'}</h3>
            <div className="form-group" style={{ marginBottom: 12 }}>
              <label>Tema / descripción corta *</label>
              <input value={form.tema} onChange={e => setForm({ ...form, tema: e.target.value })} placeholder="Ej: Escándalo de corrupción emergente" />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Nivel</label>
                <select value={form.nivel} onChange={e => setForm({ ...form, nivel: e.target.value })}>
                  <option value="verde">🟢 Verde — Bajo</option>
                  <option value="amarillo">🟡 Amarillo — Atención</option>
                  <option value="rojo">🔴 Rojo — Crítico</option>
                </select>
              </div>
              <div className="form-group">
                <label>Velocidad de crecimiento (1–5)</label>
                <input type="number" min={1} max={5} value={form.velocidad_crecimiento} onChange={e => setForm({ ...form, velocidad_crecimiento: e.target.value })} />
              </div>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Fecha de detección</label>
                <input type="date" value={form.fecha_deteccion} onChange={e => setForm({ ...form, fecha_deteccion: e.target.value })} />
              </div>
            </div>
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label>Descripción detallada</label>
              <textarea value={form.descripcion} onChange={e => setForm({ ...form, descripcion: e.target.value })} placeholder="Qué está pasando, quiénes están involucrados, dónde circula..." />
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
