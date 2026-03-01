import { useState, useEffect } from 'react'
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell, LabelList,
  ResponsiveContainer,
} from 'recharts'
import api from '../api/client'
import { useProject } from '../context/ProjectContext'

/* ── Tooltip dark (igual que Dashboard) ─────────────────────────────────── */
const TT = {
  contentStyle: { background: '#1a1d27', border: '1px solid #3a3f5c', borderRadius: 8, color: '#e8eaf6', fontSize: 12 },
  labelStyle:   { color: '#e8eaf6', fontWeight: 600 },
  itemStyle:    { color: '#c8cde8' },
}

/* ── Color por valor 0-100 ──────────────────────────────────────────────── */
const valColor = v => v > 70 ? '#f76c6c' : v > 50 ? '#f7964a' : v > 35 ? '#f7c948' : '#56c596'

/* ─────────────────────────────────────────────────────────────────────────
   GAUGE — indicador de zona horizontal con marcador
──────────────────────────────────────────────────────────────────────── */
const ZONES = [
  { label: 'Voto Duro',    width: 30, color: '#56c596' },
  { label: 'Semi-blando',  width: 25, color: '#f7c948' },
  { label: 'Alto riesgo',  width: 20, color: '#f7964a' },
  { label: 'Extremo',      width: 25, color: '#f76c6c' },
]

function GaugeIVB({ value = 0, color = '#f7c948' }) {
  const zoneName = value > 75 ? 'Extremo' : value > 55 ? 'Alto riesgo' : value > 30 ? 'Semi-blando' : 'Voto Duro'

  return (
    <div style={{ width: '100%', maxWidth: 460, margin: '0 auto', padding: '8px 0 4px' }}>

      {/* Score grande */}
      <div style={{ textAlign: 'center', marginBottom: 14 }}>
        <span style={{ fontSize: 84, fontWeight: 900, color, lineHeight: 1, letterSpacing: -2 }}>
          {value}
        </span>
        <span style={{ fontSize: 22, fontWeight: 700, color: 'var(--muted)', marginLeft: 6 }}>/100</span>
        <div style={{
          display: 'inline-block', marginLeft: 12, verticalAlign: 'middle',
          background: color + '22', border: `1px solid ${color}`,
          borderRadius: 20, padding: '3px 14px', fontSize: 12, fontWeight: 700, color,
        }}>
          {zoneName}
        </div>
      </div>

      {/* Barra de zonas con marcador */}
      <div style={{ position: 'relative', padding: '0 8px' }}>

        {/* Barra coloreada */}
        <div style={{ display: 'flex', borderRadius: 8, overflow: 'hidden', height: 28 }}>
          {ZONES.map(z => (
            <div key={z.label} style={{ width: `${z.width}%`, background: z.color }} />
          ))}
        </div>

        {/* Marcador (aguja vertical) */}
        <div style={{
          position: 'absolute',
          top: -6,
          left: `calc(${value}% - 2px)`,
          width: 4,
          height: 40,
          background: '#ffffff',
          borderRadius: 3,
          boxShadow: '0 0 6px rgba(0,0,0,.7)',
          transition: 'left 1s cubic-bezier(.4,0,.2,1)',
        }} />

        {/* Escala numérica */}
        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 5, fontSize: 10, color: 'var(--muted)' }}>
          {[0, 30, 55, 75, 100].map(n => (
            <span key={n} style={{ width: 0, textAlign: 'center', transform: 'translateX(-50%)' }}>{n}</span>
          ))}
        </div>

        {/* Etiquetas de zona */}
        <div style={{ display: 'flex', marginTop: 14 }}>
          {ZONES.map(z => (
            <div key={z.label} style={{ width: `${z.width}%`, textAlign: 'center', fontSize: 10, color: z.color, fontWeight: 700, lineHeight: 1.3 }}>
              {z.label}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

/* ── Sub-índice card ────────────────────────────────────────────────────── */
function SubCard({ code, data }) {
  const pct   = data.valor
  const color = valColor(pct)
  return (
    <div className="card" style={{ padding: '14px 16px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
        <div>
          <span style={{ fontSize: 11, color: 'var(--muted)', fontWeight: 700, letterSpacing: 1 }}>{code}</span>
          <div style={{ fontSize: 13, fontWeight: 700, marginTop: 2 }}>{data.icono} {data.nombre}</div>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: 22, fontWeight: 800, color, lineHeight: 1 }}>{data.valor}</div>
          <div style={{ fontSize: 10, color: 'var(--muted)' }}>peso {data.peso}%</div>
        </div>
      </div>
      <div style={{ background: 'var(--surface2)', borderRadius: 4, height: 7, overflow: 'hidden', marginBottom: 8 }}>
        <div style={{ height: '100%', width: `${pct}%`, background: color, borderRadius: 4, transition: 'width 1.2s cubic-bezier(.4,0,.2,1)' }} />
      </div>
      <p style={{ fontSize: 11, color: 'var(--muted)', margin: 0, lineHeight: 1.4 }}>{data.descripcion}</p>
    </div>
  )
}

/* ── Página principal ────────────────────────────────────────────────────── */
export default function IVB() {
  const { activeProject } = useProject()
  const [data, setData]       = useState(null)
  const [loading, setLoading] = useState(false)

  const load = async () => {
    if (!activeProject) return
    setLoading(true)
    try {
      const { data: d } = await api.get(`/ivb/${activeProject.id}`)
      setData(d)
    } catch (e) { console.error(e) }
    finally { setLoading(false) }
  }

  useEffect(() => { load() }, [activeProject])

  if (!activeProject) return <div className="empty-state"><span className="icon">🗂️</span>Selecciona un proyecto.</div>
  if (loading)        return <div className="empty-state"><span className="icon">⏳</span>Calculando IVB...</div>
  if (!data)          return null

  const { ivb, estado, componentes, alertas, recomendacion, tabla_interpretacion } = data
  const gColor = estado.color

  // ── Datos para gráficas ──────────────────────────────────────────────────
  const compArr = Object.entries(componentes).map(([code, d]) => ({
    code,
    nombre: d.nombre,
    icono:  d.icono,
    valor:  d.valor,
    peso:   d.peso,
    contrib: parseFloat(((d.valor * d.peso) / 100).toFixed(1)),
    color:  valColor(d.valor),
  }))

  // Radar necesita formato { subject, valor }
  const radarData = compArr.map(c => ({ subject: c.code, valor: c.valor, fullMark: 100 }))

  return (
    <div>
      {/* ── Header ───────────────────────────────────────────────────────── */}
      <div className="page-header">
        <div className="page-header-left">
          <h2>🎯 Indicador de Voto Blando</h2>
          <p>Índice compuesto 0–100 · Mide fragilidad y oportunidad del electorado no consolidado</p>
        </div>
        <button className="btn btn-outline btn-sm" onClick={load}>↺ Recalcular</button>
      </div>

      {/* ── Alertas ──────────────────────────────────────────────────────── */}
      {alertas.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginBottom: 20 }}>
          {alertas.map((a, i) => {
            const bg   = a.tipo === 'critico' ? 'rgba(247,108,108,.1)' : a.tipo === 'oportunidad' ? 'rgba(86,197,150,.1)' : 'rgba(247,201,72,.1)'
            const bord = a.tipo === 'critico' ? '#f76c6c' : a.tipo === 'oportunidad' ? '#56c596' : '#f7c948'
            return (
              <div key={i} style={{ background: bg, border: `1px solid ${bord}`, borderRadius: 8, padding: '10px 14px', fontSize: 13, display: 'flex', gap: 10, alignItems: 'center' }}>
                <span style={{ fontSize: 16 }}>{a.icono}</span>
                <span>{a.mensaje}</span>
              </div>
            )
          })}
        </div>
      )}

      {/* ── [1] Gauge + tabla interpretación ─────────────────────────────── */}
      <div className="grid-2" style={{ marginBottom: 20, alignItems: 'start' }}>

        <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 10, paddingTop: 18, paddingBottom: 18 }}>
          <GaugeIVB value={ivb} color={gColor} />
          <div style={{
            display: 'inline-block', padding: '6px 20px', borderRadius: 20,
            background: `${gColor}22`, border: `1px solid ${gColor}`,
            color: gColor, fontWeight: 700, fontSize: 13, textAlign: 'center',
          }}>
            {estado.label}
          </div>
          <p style={{ fontSize: 11, color: 'var(--muted)', textAlign: 'center', margin: 0 }}>
            Zona óptima: <strong style={{ color: '#f7964a' }}>55–70</strong>
            &nbsp;·&nbsp;Zona de riesgo: <strong style={{ color: '#f76c6c' }}>&gt;75</strong>
          </p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          <div className="card">
            <div className="card-title">Tabla de interpretación</div>
            <table style={{ fontSize: 12 }}>
              <thead>
                <tr><th>IVB</th><th>Estado</th><th>Lectura política</th></tr>
              </thead>
              <tbody>
                {tabla_interpretacion.map((row, i) => (
                  <tr key={i} style={{ background: estado.zona === row.rango ? `${row.color}1a` : 'transparent' }}>
                    <td>
                      <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                        <span style={{ width: 8, height: 8, borderRadius: '50%', background: row.color, display: 'inline-block', flexShrink: 0 }} />
                        <strong>{row.rango}</strong>
                      </span>
                    </td>
                    <td style={{ color: row.color, fontWeight: 600 }}>{row.estado}</td>
                    <td style={{ color: 'var(--muted)' }}>{row.lectura}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="card" style={{ borderLeft: `3px solid ${gColor}` }}>
            <div className="card-title">🧠 Lectura estratégica</div>
            <p style={{ fontSize: 13, lineHeight: 1.7, color: 'var(--text)', margin: 0, fontStyle: 'italic' }}>
              "{recomendacion}"
            </p>
          </div>
        </div>
      </div>

      {/* ── [2] Radar sub-índices + Contribución ponderada ───────────────── */}
      <div className="grid-2" style={{ marginBottom: 20 }}>

        {/* Radar sub-índices */}
        <div className="card">
          <div className="card-title">🔭 Radar de sub-índices</div>
          <p style={{ fontSize: 11, color: 'var(--muted)', marginBottom: 12, marginTop: -4 }}>
            Perfil comparativo de los 5 componentes (0–100)
          </p>
          <ResponsiveContainer width="100%" height={240}>
            <RadarChart data={radarData} margin={{ top: 10, right: 20, bottom: 10, left: 20 }}>
              <PolarGrid stroke="#2e3350" />
              <PolarAngleAxis
                dataKey="subject"
                tick={({ x, y, payload }) => (
                  <text x={x} y={y} textAnchor="middle" dominantBaseline="central"
                    fontSize={11} fontWeight={700} fill={valColor(
                      compArr.find(c => c.code === payload.value)?.valor ?? 50
                    )}>
                    {payload.value}
                  </text>
                )}
              />
              <PolarRadiusAxis
                angle={90} domain={[0, 100]}
                tick={{ fill: '#4a5580', fontSize: 9 }}
                axisLine={false} tickCount={4}
              />
              <Radar
                name="Valor"
                dataKey="valor"
                stroke={gColor}
                fill={gColor}
                fillOpacity={0.22}
                strokeWidth={2}
              />
              <Tooltip
                {...TT}
                formatter={(v, name, props) => {
                  const comp = compArr.find(c => c.code === props.payload.subject)
                  return [`${v} / 100`, comp ? `${comp.icono} ${comp.nombre}` : name]
                }}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* Contribución ponderada */}
        <div className="card">
          <div className="card-title">⚖️ Contribución ponderada al IVB</div>
          <p style={{ fontSize: 11, color: 'var(--muted)', marginBottom: 12, marginTop: -4 }}>
            Aporte real de cada sub-índice = valor × peso (max {Object.values(componentes).reduce((a, d) => a + d.peso / 100 * 100, 0).toFixed(0)})
          </p>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart
              data={compArr}
              layout="vertical"
              margin={{ top: 4, right: 48, bottom: 4, left: 10 }}
            >
              <CartesianGrid horizontal={false} stroke="#1e2336" />
              <XAxis
                type="number" domain={[0, 25]}
                tick={{ fill: '#4a5580', fontSize: 10 }}
                tickFormatter={v => `${v}`}
              />
              <YAxis
                type="category" dataKey="code" width={40}
                tick={({ x, y, payload }) => (
                  <text x={x} y={y} textAnchor="end" dominantBaseline="central"
                    fontSize={11} fontWeight={700} fill={valColor(
                      compArr.find(c => c.code === payload.value)?.valor ?? 50
                    )}>
                    {payload.value}
                  </text>
                )}
              />
              <Tooltip
                {...TT}
                formatter={(v, name, props) => {
                  const comp = props.payload
                  return [
                    `${v} pts (${comp.valor} × ${comp.peso}% = ${v})`,
                    `${comp.icono} ${comp.nombre}`,
                  ]
                }}
              />
              <Bar dataKey="contrib" radius={[0, 4, 4, 0]}>
                {compArr.map((c, i) => <Cell key={i} fill={c.color} />)}
                <LabelList
                  dataKey="contrib"
                  position="right"
                  style={{ fill: '#e8eaf6', fontSize: 11, fontWeight: 700 }}
                />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* ── [3] Sub-índice cards ─────────────────────────────────────────── */}
      <div style={{ marginBottom: 20 }}>
        <h3 style={{ fontSize: 12, color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: 1.5, marginBottom: 14 }}>
          Desglose por sub-índice
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: 12 }}>
          {Object.entries(componentes).map(([code, d]) => (
            <SubCard key={code} code={code} data={d} />
          ))}
        </div>
      </div>

      {/* ── [4] Fórmula ──────────────────────────────────────────────────── */}
      <div className="card" style={{ marginBottom: 20 }}>
        <div className="card-title">Fórmula de cálculo</div>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, alignItems: 'center', fontFamily: 'monospace', fontSize: 13 }}>
          <span style={{ color: gColor, fontWeight: 800, fontSize: 15 }}>IVB =</span>
          {compArr.map((c, i) => (
            <span key={c.code} style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              <span style={{ color: 'var(--muted)' }}>{(c.peso / 100).toFixed(2)}</span>
              <span>×</span>
              <span style={{ fontWeight: 700 }}>{c.code}</span>
              <span style={{ color: 'var(--muted)', fontWeight: 400, fontSize: 11 }}>({c.valor})</span>
              {i < compArr.length - 1 && <span style={{ color: 'var(--muted)' }}>+</span>}
            </span>
          ))}
          <span style={{ color: 'var(--muted)' }}>=</span>
          <span style={{ color: gColor, fontWeight: 800, fontSize: 15 }}>{ivb}</span>
        </div>
      </div>

      {/* ── [5] Guía táctica ─────────────────────────────────────────────── */}
      <div className="grid-2">
        <div className="card" style={{ borderLeft: '3px solid var(--success)' }}>
          <div className="card-title">✅ Qué activa al voto blando</div>
          {[
            'Certeza y orden: "esto se hará así, paso 1-2-3"',
            'Empatía sin drama: reconoce el problema sin exagerar',
            'Solución concreta y medible con plazos cortos',
            'Humildad: "esto sí depende del municipio / esto no"',
            'Protección de la economía familiar directa',
          ].map((t, i) => (
            <div key={i} style={{ display: 'flex', gap: 8, marginBottom: 8, fontSize: 12, alignItems: 'flex-start' }}>
              <span style={{ color: 'var(--success)', fontWeight: 700, flexShrink: 0, marginTop: 1 }}>✓</span>
              <span>{t}</span>
            </div>
          ))}
        </div>
        <div className="card" style={{ borderLeft: '3px solid var(--accent4)' }}>
          <div className="card-title">❌ Qué espanta al voto blando</div>
          {[
            'Ataque visceral: "ellos son la basura / los enemigos"',
            'Promesa total: "en 100 días arreglo todo"',
            'Polarización ideológica: "patriotas vs traidores"',
            'Soberbia: "yo soy el único capaz"',
            'Ambigüedad: "vamos a ver / haremos lo posible"',
          ].map((t, i) => (
            <div key={i} style={{ display: 'flex', gap: 8, marginBottom: 8, fontSize: 12, alignItems: 'flex-start' }}>
              <span style={{ color: 'var(--accent4)', fontWeight: 700, flexShrink: 0, marginTop: 1 }}>✗</span>
              <span>{t}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
