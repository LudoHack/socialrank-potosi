import { useState, useEffect, useMemo } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  Cell, LabelList, ResponsiveContainer
} from 'recharts'
import api from '../api/client'
import { useProject } from '../context/ProjectContext'
import { useRole } from '../context/RoleContext'

/* ─── Categorías semánticas ─────────────────────────────────────────────── */
const FUNC = {
  indecision:   { color: '#f7c948', icon: '🤔', label: 'Indecisión' },
  desconfianza: { color: '#f76c6c', icon: '😒', label: 'Desconfianza' },
  activacion:   { color: '#56c596', icon: '💪', label: 'Activación' },
  espanto:      { color: '#a78bfa', icon: '😨', label: 'Espanto' },
  economia:     { color: '#4ecdc4', icon: '💰', label: 'Economía cotidiana' },
  gestion:      { color: '#7c6af7', icon: '🏛️', label: 'Gestión' },
  emocion:      { color: '#f76c9a', icon: '💭', label: 'Emocional blando' },
  identidad:    { color: '#f7964a', icon: '🌍', label: 'Identidad local' },
}

const IMPACTO = {
  activa:  { color: '#56c596', label: 'Activa voto' },
  neutral: { color: '#7b82a8', label: 'Neutral' },
  espanta: { color: '#f76c6c', label: 'Espanta voto' },
}

const TT = {
  contentStyle: { background: '#1a1d27', border: '1px solid #3a3f5c', borderRadius: 8, color: '#e8eaf6', fontSize: 12 },
  labelStyle:   { color: '#e8eaf6', fontWeight: 600 },
  itemStyle:    { color: '#c8cde8' },
}

/* ─── KPI Card ───────────────────────────────────────────────────────────── */
function KPICard({ icon, label, value, sub, color }) {
  return (
    <div className="stat-card" style={{ flex: 1, minWidth: 140 }}>
      <div className="label">{icon} {label}</div>
      <div className="value" style={{ color: color || 'var(--accent)', fontSize: 28 }}>{value}</div>
      {sub && <div className="sub">{sub}</div>}
    </div>
  )
}

/* ─── Nube de términos ───────────────────────────────────────────────────── */
function WordCloud({ items, activeFuncion, onClickFuncion }) {
  const visible = activeFuncion ? items.filter(i => i.funcion_cultural === activeFuncion) : items
  if (!visible.length) return (
    <div className="empty-state" style={{ padding: 20 }}>
      <span className="icon">☁️</span>Sin términos en esta categoría
    </div>
  )
  const maxFreq = Math.max(...visible.map(i => i.frecuencia || 1))
  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10, padding: '12px 0', minHeight: 120, alignItems: 'center' }}>
      {[...visible]
        .sort((a, b) => (b.frecuencia || 1) - (a.frecuencia || 1))
        .map(i => {
          const cat  = FUNC[i.funcion_cultural] || { color: 'var(--muted)', label: '' }
          const size = 11 + Math.round(((i.frecuencia || 1) / maxFreq) * 22)
          return (
            <span
              key={i.id}
              onClick={() => onClickFuncion && onClickFuncion(i.funcion_cultural)}
              title={`${i.termino} — ${cat.label} · ${i.frecuencia} menciones${i.impacto_voto_blando ? ' · ' + (IMPACTO[i.impacto_voto_blando]?.label || '') : ''}`}
              style={{
                fontSize: size,
                fontWeight: size > 24 ? 800 : size > 18 ? 700 : 500,
                color: cat.color,
                cursor: 'pointer',
                transition: 'opacity 0.2s',
                letterSpacing: size > 20 ? '-0.5px' : 'normal',
                lineHeight: 1.3,
                userSelect: 'none',
              }}
            >
              {i.termino}
            </span>
          )
        })}
    </div>
  )
}

/* ─── Página principal ───────────────────────────────────────────────────── */
export default function Lenguaje() {
  const { activeProject } = useProject()
  const { isAdmin }       = useRole()

  const [items, setItems]           = useState([])
  const [showForm, setShowForm]     = useState(false)
  const [editItem, setEditItem]     = useState(null)
  const [activeFuncion, setActiveFuncion] = useState(null)
  const [form, setForm] = useState({
    termino: '', tipo: 'frase', frecuencia: 1,
    contexto: '', fecha_deteccion: '', funcion_cultural: '', impacto_voto_blando: ''
  })

  const load = () => {
    if (!activeProject) return
    api.get(`/language/${activeProject.id}`).then(r => setItems(r.data)).catch(console.error)
  }
  useEffect(() => { load() }, [activeProject])

  /* ── KPIs ─────────────────────────────────────────────────────────────── */
  const kpis = useMemo(() => {
    if (!items.length) return { pctInde: 0, pctActiva: 0, ratio: '—', emergentes: 0 }
    const total  = items.reduce((s, i) => s + (i.frecuencia || 1), 0)
    const inde   = items.filter(i => i.funcion_cultural === 'indecision').reduce((s, i) => s + (i.frecuencia || 1), 0)
    const activa = items.filter(i => i.funcion_cultural === 'activacion').reduce((s, i) => s + (i.frecuencia || 1), 0)
    const espant = items.filter(i => i.funcion_cultural === 'espanto').reduce((s, i) => s + (i.frecuencia || 1), 0)
    const hace7  = new Date(Date.now() - 7 * 24 * 3600 * 1000).toISOString().slice(0, 10)
    const emerg  = items.filter(i => i.fecha_deteccion && i.fecha_deteccion >= hace7).length
    return {
      pctInde:   total ? Math.round(inde  / total * 100) : 0,
      pctActiva: total ? Math.round(activa / total * 100) : 0,
      ratio:     espant > 0 ? (activa / espant).toFixed(2) : activa > 0 ? '∞' : '—',
      emergentes: emerg,
    }
  }, [items])

  /* ── Distribución por categoría ───────────────────────────────────────── */
  const distData = useMemo(() => {
    return Object.entries(FUNC)
      .map(([key, meta]) => ({
        key,
        label: meta.label,
        freq:  items.filter(i => i.funcion_cultural === key).reduce((s, i) => s + (i.frecuencia || 1), 0),
        color: meta.color,
      }))
      .filter(d => d.freq > 0)
      .sort((a, b) => b.freq - a.freq)
  }, [items])

  /* ── Tabla filtrada ───────────────────────────────────────────────────── */
  const filtered = useMemo(() => {
    if (!activeFuncion) return items
    return items.filter(i => i.funcion_cultural === activeFuncion)
  }, [items, activeFuncion])

  /* ── CRUD ─────────────────────────────────────────────────────────────── */
  const openCreate = () => {
    setEditItem(null)
    setForm({ termino: '', tipo: 'frase', frecuencia: 1, contexto: '', fecha_deteccion: '', funcion_cultural: '', impacto_voto_blando: '' })
    setShowForm(true)
  }
  const openEdit = (i) => {
    setEditItem(i)
    setForm({
      termino: i.termino, tipo: i.tipo || 'frase', frecuencia: i.frecuencia || 1,
      contexto: i.contexto || '', fecha_deteccion: i.fecha_deteccion || '',
      funcion_cultural: i.funcion_cultural || '', impacto_voto_blando: i.impacto_voto_blando || ''
    })
    setShowForm(true)
  }
  const save = async () => {
    if (!form.termino.trim()) return alert('El término es obligatorio')
    const payload = { ...form, project_id: activeProject.id, frecuencia: parseInt(form.frecuencia) || 1 }
    if (editItem) await api.put(`/language/${editItem.id}`, payload)
    else           await api.post('/language/', payload)
    setShowForm(false); load()
  }
  const del = async (id) => {
    if (!confirm('¿Eliminar término?')) return
    await api.delete(`/language/${id}`); load()
  }

  const toggleFuncion = (fn) => setActiveFuncion(prev => prev === fn ? null : fn)

  if (!activeProject) return <div className="empty-state"><span className="icon">🗂️</span>Selecciona un proyecto.</div>

  return (
    <div>
      {/* ── Header ─────────────────────────────────────────────────────── */}
      <div className="page-header">
        <div className="page-header-left">
          <h2>🗣️ Lenguaje y Códigos Culturales</h2>
          <p>Sensor semántico del voto blando · función cultural e impacto electoral</p>
        </div>
        {isAdmin && (
          <button className="btn btn-primary" onClick={openCreate}>+ Nuevo término</button>
        )}
      </div>

      {/* ── KPIs ───────────────────────────────────────────────────────── */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 20, flexWrap: 'wrap' }}>
        <KPICard icon="🤔" label="Indecisión"   value={`${kpis.pctInde}%`}   sub="del volumen total"         color={FUNC.indecision.color} />
        <KPICard icon="💪" label="Activación"   value={`${kpis.pctActiva}%`} sub="del volumen total"         color={FUNC.activacion.color} />
        <KPICard icon="⚖️" label="Act/Espanto"  value={kpis.ratio}            sub="ratio activación vs espanto" color={parseFloat(kpis.ratio) >= 1 ? '#56c596' : '#f76c6c'} />
        <KPICard icon="🆕" label="Emergentes"   value={kpis.emergentes}       sub="detectados últimos 7 días"  color="var(--accent)" />
      </div>

      {/* ── Nube + Distribución ────────────────────────────────────────── */}
      <div className="grid-2" style={{ marginBottom: 20 }}>

        {/* Nube de términos */}
        <div className="card">
          <div className="card-title" style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            Nube semántica
            {activeFuncion && (
              <span
                style={{ fontSize: 11, color: 'var(--muted)', cursor: 'pointer', textDecoration: 'underline', fontWeight: 400 }}
                onClick={() => setActiveFuncion(null)}
              >
                limpiar ✕
              </span>
            )}
          </div>
          {/* Chips de categoría */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 10 }}>
            {Object.entries(FUNC).map(([key, meta]) => (
              <span
                key={key}
                onClick={() => toggleFuncion(key)}
                style={{
                  fontSize: 11, padding: '3px 10px', borderRadius: 99, cursor: 'pointer',
                  background: activeFuncion === key ? meta.color + '33' : 'var(--surface2)',
                  color:      activeFuncion === key ? meta.color : 'var(--muted)',
                  border:     `1px solid ${activeFuncion === key ? meta.color : 'transparent'}`,
                  fontWeight: activeFuncion === key ? 700 : 400,
                  transition: 'all 0.15s',
                }}
              >
                {meta.icon} {meta.label}
              </span>
            ))}
          </div>
          <WordCloud items={items} activeFuncion={activeFuncion} onClickFuncion={toggleFuncion} />
        </div>

        {/* Bar chart distribución */}
        <div className="card">
          <div className="card-title">Distribución por función cultural</div>
          {distData.length ? (
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={distData} layout="vertical" margin={{ left: 10, right: 48 }}>
                <CartesianGrid horizontal={false} stroke="var(--border)" />
                <XAxis type="number" tick={{ fill: 'var(--muted)', fontSize: 11 }} />
                <YAxis type="category" dataKey="label" tick={{ fill: 'var(--text)', fontSize: 11 }} width={115} />
                <Tooltip {...TT} formatter={v => [v, 'Menciones']} />
                <Bar dataKey="freq" radius={[0, 4, 4, 0]}>
                  {distData.map((d, i) => <Cell key={i} fill={d.color} />)}
                  <LabelList dataKey="freq" position="right" style={{ fill: 'var(--muted)', fontSize: 11 }} />
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state" style={{ padding: 20 }}><span className="icon">📊</span>Sin datos</div>
          )}
        </div>
      </div>

      {/* ── Cards de categoría ─────────────────────────────────────────── */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(175px, 1fr))', gap: 12, marginBottom: 20 }}>
        {Object.entries(FUNC).map(([key, meta]) => {
          const terms = items.filter(i => i.funcion_cultural === key)
          const freq  = terms.reduce((s, i) => s + (i.frecuencia || 1), 0)
          const isAct = activeFuncion === key
          return (
            <div
              key={key}
              className="card"
              onClick={() => toggleFuncion(key)}
              style={{
                cursor: 'pointer',
                border:     `1.5px solid ${isAct ? meta.color : 'var(--border)'}`,
                background: isAct ? meta.color + '11' : 'var(--surface)',
                transition: 'all 0.2s',
                padding: '14px 16px',
              }}
            >
              <div style={{ fontSize: 22, marginBottom: 4 }}>{meta.icon}</div>
              <div style={{ fontWeight: 700, fontSize: 13, color: meta.color }}>{meta.label}</div>
              <div style={{ fontSize: 22, fontWeight: 800, color: 'var(--text)', margin: '4px 0' }}>{terms.length}</div>
              <div style={{ fontSize: 11, color: 'var(--muted)' }}>términos · {freq} menciones</div>
            </div>
          )
        })}
      </div>

      {/* ── Tabla de términos ──────────────────────────────────────────── */}
      <div className="card">
        <div className="card-title" style={{ marginBottom: 12 }}>
          Registro de términos
          {activeFuncion && (
            <span style={{ marginLeft: 8, fontSize: 11, color: FUNC[activeFuncion]?.color }}>
              · filtrando: {FUNC[activeFuncion]?.label}
            </span>
          )}
        </div>
        <table>
          <thead>
            <tr>
              <th>Término</th>
              <th>Tipo</th>
              <th>Frecuencia</th>
              <th>Función cultural</th>
              <th>Impacto voto</th>
              <th>Detectado</th>
              <th>Contexto</th>
              {isAdmin && <th></th>}
            </tr>
          </thead>
          <tbody>
            {filtered.map(i => {
              const cat = FUNC[i.funcion_cultural]      || { color: 'var(--muted)', icon: '', label: i.funcion_cultural || '—' }
              const imp = IMPACTO[i.impacto_voto_blando] || { color: 'var(--muted)', label: i.impacto_voto_blando || '—' }
              const maxFreq = items.length ? Math.max(...items.map(x => x.frecuencia || 1)) : 1
              return (
                <tr key={i.id}>
                  <td style={{ fontWeight: 600 }}>{i.termino}</td>
                  <td>
                    <span className="badge" style={{ background: 'var(--surface2)', color: 'var(--muted)' }}>
                      {i.tipo || 'frase'}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                      <div className="progress-bar" style={{ width: 50 }}>
                        <div className="progress-fill" style={{ width: `${Math.min(100, ((i.frecuencia || 1) / maxFreq) * 100)}%` }} />
                      </div>
                      <span style={{ fontSize: 12, fontWeight: 700 }}>{i.frecuencia || 1}</span>
                    </div>
                  </td>
                  <td>
                    <span className="badge" style={{ background: cat.color + '22', color: cat.color }}>
                      {cat.icon} {cat.label}
                    </span>
                  </td>
                  <td>
                    <span className="badge" style={{ background: imp.color + '22', color: imp.color }}>
                      {imp.label}
                    </span>
                  </td>
                  <td style={{ fontSize: 12, color: 'var(--muted)' }}>{i.fecha_deteccion || '—'}</td>
                  <td style={{ fontSize: 12, color: 'var(--muted)', maxWidth: 200 }}>{i.contexto || '—'}</td>
                  {isAdmin && (
                    <td style={{ whiteSpace: 'nowrap' }}>
                      <button className="btn btn-outline btn-sm" onClick={() => openEdit(i)}>Editar</button>{' '}
                      <button className="btn btn-danger btn-sm" onClick={() => del(i.id)}>✕</button>
                    </td>
                  )}
                </tr>
              )
            })}
          </tbody>
        </table>
        {!filtered.length && (
          <div className="empty-state">
            <span className="icon">🗣️</span>
            {isAdmin ? 'Sin términos. Agrega el primero o importa desde Excel.' : 'Sin términos registrados para este proyecto.'}
          </div>
        )}
      </div>

      {/* ── Modal admin ────────────────────────────────────────────────── */}
      {isAdmin && (
        <div
          className={`modal-overlay ${showForm ? 'open' : ''}`}
          onClick={e => e.target.className?.includes?.('modal-overlay') && setShowForm(false)}
        >
          <div className="modal">
            <h3>{editItem ? 'Editar término' : 'Nuevo término cultural'}</h3>

            <div className="form-row">
              <div className="form-group" style={{ flex: 2 }}>
                <label>Término / frase *</label>
                <input
                  value={form.termino}
                  onChange={e => setForm({ ...form, termino: e.target.value })}
                  placeholder="Ej: Todavía estoy viendo..."
                />
              </div>
              <div className="form-group">
                <label>Tipo</label>
                <select value={form.tipo} onChange={e => setForm({ ...form, tipo: e.target.value })}>
                  <option value="frase">Frase</option>
                  <option value="termino">Término</option>
                  <option value="expresion">Expresión</option>
                  <option value="hashtag">Hashtag</option>
                  <option value="emoji">Emoji</option>
                </select>
              </div>
              <div className="form-group">
                <label>Frecuencia</label>
                <input type="number" min={1} value={form.frecuencia} onChange={e => setForm({ ...form, frecuencia: e.target.value })} />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Función cultural *</label>
                <select value={form.funcion_cultural} onChange={e => setForm({ ...form, funcion_cultural: e.target.value })}>
                  <option value="">— Seleccionar —</option>
                  {Object.entries(FUNC).map(([k, v]) => (
                    <option key={k} value={k}>{v.icon} {v.label}</option>
                  ))}

                </select>
              </div>
              <div className="form-group">
                <label>Impacto voto blando</label>
                <select value={form.impacto_voto_blando} onChange={e => setForm({ ...form, impacto_voto_blando: e.target.value })}>
                  <option value="">— Seleccionar —</option>
                  <option value="activa">✅ Activa voto</option>
                  <option value="neutral">➖ Neutral</option>
                  <option value="espanta">❌ Espanta voto</option>
                </select>
              </div>
              <div className="form-group">
                <label>Fecha detección</label>
                <input type="date" value={form.fecha_deteccion} onChange={e => setForm({ ...form, fecha_deteccion: e.target.value })} />
              </div>
            </div>

            <div className="form-group" style={{ marginBottom: 0 }}>
              <label>Contexto / observaciones</label>
              <textarea
                value={form.contexto}
                onChange={e => setForm({ ...form, contexto: e.target.value })}
                placeholder="¿Dónde aparece? ¿Qué significa culturalmente?"
                rows={3}
              />
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
