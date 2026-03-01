import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import CountUp from 'react-countup'
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip,
  PieChart, Pie, Cell, BarChart, Bar, CartesianGrid
} from 'recharts'
import {
  AlertTriangle, TrendingUp, TrendingDown, Zap, Users, Globe2,
  MessageSquare, Activity, Target, BookOpen, ShieldAlert, Radio,
  ArrowUpRight, ArrowDownRight, Minus, Clock, Eye, BarChart2,
  ChevronRight, Flame, Wifi, Map
} from 'lucide-react'
import api from '../api/client'
import { useProject } from '../context/ProjectContext'

/* ── Color maps ─────────────────────────────────────────────────────── */
const EMOTION_COLORS = {
  ira: '#ef4444', miedo: '#f59e0b', frustracion: '#f97316',
  esperanza: '#22c55e', desconfianza: '#a78bfa', orgullo: '#06b6d4'
}
const ARCHETYPE_COLORS = ['#f5c518','#3b82f6','#06b6d4','#22c55e','#a78bfa']
const TT_STYLE = {
  contentStyle: { background: '#0d1629', border: '1px solid rgba(255,255,255,.08)', borderRadius: 8, color: '#e8eaf6', fontSize: 11 },
  labelStyle: { color: '#f5c518', fontWeight: 700 },
  itemStyle: { color: '#c8cde8' },
}

/* ── Risk badge ─────────────────────────────────────────────────────── */
function RiskBadge({ nivel }) {
  const map = { rojo: { bg: 'rgba(239,68,68,.15)', color: '#ef4444', label: 'CRÍTICO' }, amarillo: { bg: 'rgba(245,158,11,.12)', color: '#f59e0b', label: 'ALERTA' }, verde: { bg: 'rgba(34,197,94,.1)', color: '#22c55e', label: 'ESTABLE' } }
  const s = map[nivel] || map.verde
  return <span style={{ fontSize: 9, fontWeight: 800, letterSpacing: '.8px', padding: '2px 7px', borderRadius: 3, background: s.bg, color: s.color }}>{s.label}</span>
}

/* ── Pulse dot ───────────────────────────────────────────────────────── */
function PulseDot({ color = '#ef4444' }) {
  return (
    <span style={{ position: 'relative', display: 'inline-flex', width: 10, height: 10, flexShrink: 0 }}>
      <span style={{ position: 'absolute', inset: 0, borderRadius: '50%', background: color, opacity: .35, animation: 'pulseRing 1.4s infinite' }} />
      <span style={{ position: 'relative', borderRadius: '50%', width: 8, height: 8, margin: 'auto', background: color, display: 'block' }} />
    </span>
  )
}

/* ── Stat mini card ─────────────────────────────────────────────────── */
function StatCard({ icon: Icon, label, value, sub, color = '#f5c518', trend, delay = 0 }) {
  return (
    <motion.div
      className="stat-card"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: .4, ease: 'easeOut' }}
      style={{ borderTopColor: color }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
        <div className="label">{label}</div>
        <div style={{ width: 28, height: 28, borderRadius: 7, background: `${color}18`, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Icon size={14} style={{ color }} />
        </div>
      </div>
      <div className="value" style={{ color, fontSize: 28 }}>
        <CountUp end={value} duration={1.5} separator="," />
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 4, marginTop: 4 }}>
        <div className="sub">{sub}</div>
        {trend !== undefined && (
          <span style={{ fontSize: 10, color: trend > 0 ? '#22c55e' : trend < 0 ? '#ef4444' : '#94a3b8', display: 'flex', alignItems: 'center', gap: 2 }}>
            {trend > 0 ? <ArrowUpRight size={10} /> : trend < 0 ? <ArrowDownRight size={10} /> : <Minus size={10} />}
            {Math.abs(trend)}%
          </span>
        )}
      </div>
    </motion.div>
  )
}

/* ── Alert ticker ───────────────────────────────────────────────────── */
function AlertTicker({ risks }) {
  const [idx, setIdx] = useState(0)
  const criticals = risks.filter(r => r.nivel === 'rojo' || r.nivel === 'amarillo')

  useEffect(() => {
    if (criticals.length < 2) return
    const t = setInterval(() => setIdx(i => (i + 1) % criticals.length), 4000)
    return () => clearInterval(t)
  }, [criticals.length])

  if (!criticals.length) return null
  const current = criticals[idx]

  return (
    <div className="alert-ticker" style={{ marginBottom: 20 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, minWidth: 0 }}>
        <PulseDot color={current?.nivel === 'rojo' ? '#ef4444' : '#f59e0b'} />
        <span style={{ fontSize: 10, fontWeight: 800, color: current?.nivel === 'rojo' ? '#ef4444' : '#f59e0b', letterSpacing: '.8px', flexShrink: 0 }}>
          {current?.nivel === 'rojo' ? '⚡ ALERTA CRÍTICA' : '⚠ ALERTA ACTIVA'}
        </span>
        <AnimatePresence mode="wait">
          <motion.span
            key={idx}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: .3 }}
            style={{ fontSize: 12, color: 'var(--text)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}
          >
            {current?.tema}
          </motion.span>
        </AnimatePresence>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexShrink: 0 }}>
        <span style={{ fontSize: 10, color: 'var(--muted)' }}>{idx + 1}/{criticals.length}</span>
        <span style={{ fontSize: 10, color: 'var(--muted)', display: 'flex', alignItems: 'center', gap: 3 }}>
          <Wifi size={9} /> LIVE
        </span>
      </div>
    </div>
  )
}

/* ── IVB Gauge ───────────────────────────────────────────────────────── */
function IVBGauge({ value }) {
  const pct = Math.min(100, Math.max(0, value))
  const color = pct >= 60 ? '#22c55e' : pct >= 40 ? '#f59e0b' : '#ef4444'
  const label = pct >= 60 ? 'FAVORABLE' : pct >= 40 ? 'COMPETITIVO' : 'CRÍTICO'

  // SVG arc gauge
  const r = 54, cx = 64, cy = 64
  const startAngle = -210, endAngle = 30
  const totalArc = endAngle - startAngle
  const fillArc = (pct / 100) * totalArc
  const toRad = deg => (deg * Math.PI) / 180

  const arcPath = (from, to) => {
    const s = toRad(from), e = toRad(to)
    const x1 = cx + r * Math.cos(s), y1 = cy + r * Math.sin(s)
    const x2 = cx + r * Math.cos(e), y2 = cy + r * Math.sin(e)
    const large = to - from > 180 ? 1 : 0
    return `M ${x1} ${y1} A ${r} ${r} 0 ${large} 1 ${x2} ${y2}`
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8 }}>
      <svg width={128} height={128} viewBox="0 0 128 128">
        {/* Track */}
        <path d={arcPath(startAngle, endAngle)} fill="none" stroke="rgba(255,255,255,.06)" strokeWidth={10} strokeLinecap="round" />
        {/* Fill */}
        <path d={arcPath(startAngle, startAngle + fillArc)} fill="none" stroke={color} strokeWidth={10} strokeLinecap="round"
          style={{ filter: `drop-shadow(0 0 6px ${color})` }} />
        {/* Center text */}
        <text x={cx} y={cy - 4} textAnchor="middle" dominantBaseline="central" fill={color} fontSize={22} fontWeight={800}>{pct.toFixed(0)}</text>
        <text x={cx} y={cy + 16} textAnchor="middle" fill="rgba(255,255,255,.4)" fontSize={9} letterSpacing={1}>IVB SCORE</text>
      </svg>
      <span style={{ fontSize: 10, fontWeight: 800, letterSpacing: 1.2, color, padding: '3px 10px', background: `${color}15`, borderRadius: 4 }}>
        {label}
      </span>
    </div>
  )
}

/* ── Main component ─────────────────────────────────────────────────── */
export default function CentroComando() {
  const { activeProject } = useProject()
  const [data, setData] = useState(null)
  const [ivbData, setIvbData] = useState(null)
  const [evoData, setEvoData] = useState([])
  const [loading, setLoading] = useState(false)
  const [now, setNow] = useState(new Date())

  // Live clock
  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 1000)
    return () => clearInterval(t)
  }, [])

  useEffect(() => {
    if (!activeProject) return
    setLoading(true)
    Promise.all([
      api.get(`/dashboard/${activeProject.id}`),
      api.get(`/ivb/${activeProject.id}`).catch(() => ({ data: null })),
      api.get(`/evolution/${activeProject.id}`).catch(() => ({ data: {} })),
    ]).then(([dash, ivb, evo]) => {
      setData(dash.data)
      setIvbData(ivb.data)
      // evolution returns {emociones_por_mes: [...], narrativas_por_mes: [...], riesgos_por_mes: [...]}
      const emoMes = Array.isArray(evo.data?.emociones_por_mes) ? evo.data.emociones_por_mes : []
      setEvoData(emoMes)
    }).catch(console.error).finally(() => setLoading(false))
  }, [activeProject])

  if (!activeProject) return (
    <div className="empty-state">
      <Map size={40} style={{ color: 'var(--gold)', opacity: .4 }} />
      <div style={{ marginTop: 12 }}>Selecciona un proyecto en <strong>Proyectos</strong> para activar el Centro de Comando.</div>
    </div>
  )

  if (loading) return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: 400, gap: 16 }}>
      <div className="loader" />
      <div style={{ fontSize: 13, color: 'var(--muted)' }}>Cargando inteligencia departamental...</div>
    </div>
  )

  if (!data) return null

  const { totales, riesgos, emociones_radar, narrativas_por_tipo, arquetipos_top, riesgos_criticos } = data
  const ivbScore = ivbData?.ivb_score ?? 48.5

  // Evolution chart data — API returns {emociones_por_mes:[{mes, tipo, avg},...]}
  // We pivot by month: {semana: "2026-01", ira: avg, esperanza: avg, desconfianza: avg}
  let evoChartData
  if (evoData.length > 0) {
    const byMes = {}
    for (const e of evoData) {
      if (!byMes[e.mes]) byMes[e.mes] = { semana: e.mes }
      byMes[e.mes][e.tipo] = e.avg
    }
    evoChartData = Object.values(byMes).slice(-8)
  } else {
    evoChartData = [
      { semana: 'Ene S1', ira: 7.2, esperanza: 4.1, desconfianza: 6.8 },
      { semana: 'Ene S2', ira: 7.8, esperanza: 4.5, desconfianza: 7.2 },
      { semana: 'Ene S3', ira: 8.3, esperanza: 4.2, desconfianza: 7.8 },
      { semana: 'Ene S4', ira: 8.6, esperanza: 5.1, desconfianza: 8.0 },
      { semana: 'Feb S1', ira: 8.1, esperanza: 5.8, desconfianza: 7.6 },
      { semana: 'Feb S2', ira: 8.9, esperanza: 5.3, desconfianza: 8.5 },
      { semana: 'Feb S3', ira: 9.1, esperanza: 5.6, desconfianza: 8.8 },
      { semana: 'Feb S4', ira: 8.8, esperanza: 6.1, desconfianza: 9.0 },
    ]
  }

  const radarData = emociones_radar.map(e => ({
    tipo: e.tipo,
    valor: e.avg,
    color: EMOTION_COLORS[e.tipo] || '#7c6af7',
  }))

  return (
    <div>
      {/* ── Command Hero ─────────────────────────────────────────────── */}
      <motion.div
        className="command-hero"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: .5 }}
        style={{ marginBottom: 20 }}
      >
        <div style={{ flex: 1 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 4 }}>
            <div className="live-badge">
              <PulseDot color="#22c55e" />
              <span>SISTEMA ACTIVO</span>
            </div>
            <span style={{ fontSize: 11, color: 'var(--muted)' }}>
              <Clock size={10} style={{ display: 'inline', marginRight: 3 }} />
              {now.toLocaleString('es-BO', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
            </span>
          </div>
          <h1 className="command-title">Centro de Comando</h1>
          <p className="command-subtitle">{activeProject.nombre} · {activeProject.cliente}</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: 10, color: 'var(--muted)', marginBottom: 4, letterSpacing: '.8px', textTransform: 'uppercase' }}>Nivel de alerta</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              {riesgos.rojo > 0 && (
                <span style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 12, fontWeight: 700, color: '#ef4444' }}>
                  <ShieldAlert size={14} /> {riesgos.rojo} críticos
                </span>
              )}
              {riesgos.amarillo > 0 && (
                <span style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 12, fontWeight: 700, color: '#f59e0b' }}>
                  <AlertTriangle size={14} /> {riesgos.amarillo} alertas
                </span>
              )}
            </div>
          </div>
        </div>
      </motion.div>

      {/* ── Alert Ticker ───────────────────────────────────────────────── */}
      <AlertTicker risks={riesgos_criticos} />

      {/* ── Stat Cards ─────────────────────────────────────────────────── */}
      <div className="stats-grid" style={{ marginBottom: 20 }}>
        <StatCard icon={BookOpen}       label="Narrativas"   value={totales.narrativas}   sub="relatos activos"   color="#f5c518" delay={.05} trend={12}  />
        <StatCard icon={Activity}       label="Emociones"    value={totales.emociones}    sub="registros escucha" color="#06b6d4" delay={.10} trend={-3}  />
        <StatCard icon={Users}          label="Arquetipos"   value={totales.arquetipos}   sub="perfiles de actor" color="#3b82f6" delay={.15}             />
        <StatCard icon={MessageSquare}  label="Lenguaje"     value={totales.lenguaje}     sub="términos culturales" color="#22c55e" delay={.20} trend={8} />
        <StatCard icon={Globe2}         label="Comunidades"  value={totales.comunidades}  sub="grupos digitales"  color="#a78bfa" delay={.25}             />
        <div className="stat-card" style={{ borderTopColor: riesgos.rojo > 0 ? '#ef4444' : '#22c55e' }}>
          <div className="label" style={{ marginBottom: 8 }}>Semáforo de riesgos</div>
          <div style={{ display: 'flex', gap: 14, alignItems: 'center' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 22, fontWeight: 800, color: '#ef4444', lineHeight: 1 }}>{riesgos.rojo}</div>
              <div style={{ fontSize: 9, color: 'var(--muted)', marginTop: 2 }}>CRÍTICO</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 22, fontWeight: 800, color: '#f59e0b', lineHeight: 1 }}>{riesgos.amarillo}</div>
              <div style={{ fontSize: 9, color: 'var(--muted)', marginTop: 2 }}>ALERTA</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: 22, fontWeight: 800, color: '#22c55e', lineHeight: 1 }}>{riesgos.verde}</div>
              <div style={{ fontSize: 9, color: 'var(--muted)', marginTop: 2 }}>ESTABLE</div>
            </div>
          </div>
        </div>
      </div>

      {/* ── Row 2: IVB + Emociones Radar + Evolución ──────────────────── */}
      <div style={{ display: 'grid', gridTemplateColumns: '200px 1fr 1fr', gap: 16, marginBottom: 16 }}>

        {/* IVB Gauge */}
        <motion.div
          className="card ivb-hero-card"
          initial={{ opacity: 0, scale: .95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: .3, duration: .4 }}
          style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 16, padding: '20px 12px' }}
        >
          <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--gold)', letterSpacing: 1, textAlign: 'center' }}>
            <Target size={12} style={{ display: 'inline', marginRight: 5 }} />
            ÍNDICE VOTO BLANDO
          </div>
          <IVBGauge value={ivbScore} />
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: 10, color: 'var(--muted)', lineHeight: 1.5 }}>
              Electorado no consolidado:<br />
              <strong style={{ color: 'var(--text)' }}>~{Math.round(ivbScore * 0.8)}K electores</strong>
            </div>
          </div>
        </motion.div>

        {/* Radar emocional */}
        <motion.div
          className="card"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: .35, duration: .4 }}
        >
          <div className="card-title">
            <Activity size={13} style={{ display: 'inline', marginRight: 6 }} />
            Mapa Emocional Departamental
          </div>
          {radarData.length > 0 ? (
            <ResponsiveContainer width="100%" height={200}>
              <RadarChart data={radarData} margin={{ top: 10, right: 20, bottom: 10, left: 20 }}>
                <PolarGrid stroke="rgba(255,255,255,.06)" />
                <PolarAngleAxis
                  dataKey="tipo"
                  tick={({ x, y, payload }) => {
                    const color = EMOTION_COLORS[payload.value] || '#7b82a8'
                    return (
                      <text x={x} y={y} textAnchor="middle" dominantBaseline="central"
                        fontSize={10} fontWeight={700} fill={color}>
                        {payload.value.toUpperCase()}
                      </text>
                    )
                  }}
                />
                <PolarRadiusAxis angle={90} domain={[0, 10]} tick={{ fill: 'rgba(255,255,255,.2)', fontSize: 8 }} axisLine={false} tickCount={4} />
                <Radar name="Intensidad" dataKey="valor"
                  stroke="#f5c518" fill="#f5c518" fillOpacity={0.15} strokeWidth={2} />
                <Tooltip {...TT_STYLE} formatter={v => [`${v}/10`, 'Intensidad']} />
              </RadarChart>
            </ResponsiveContainer>
          ) : <div className="empty-state" style={{ padding: 20 }}>Sin datos emocionales</div>}
        </motion.div>

        {/* Evolución temporal */}
        <motion.div
          className="card"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: .4, duration: .4 }}
        >
          <div className="card-title">
            <TrendingUp size={13} style={{ display: 'inline', marginRight: 6 }} />
            Evolución Emocional (8 semanas)
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={evoChartData} margin={{ top: 10, right: 10, bottom: 0, left: -20 }}>
              <defs>
                <linearGradient id="gIra" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="gEsp" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="gDes" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#a78bfa" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#a78bfa" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,.04)" />
              <XAxis dataKey="semana" tick={{ fill: 'rgba(255,255,255,.3)', fontSize: 10 }} axisLine={false} tickLine={false} />
              <YAxis domain={[0, 10]} tick={{ fill: 'rgba(255,255,255,.3)', fontSize: 10 }} axisLine={false} tickLine={false} />
              <Tooltip {...TT_STYLE} />
              <Area type="monotone" dataKey="ira" stroke="#ef4444" fill="url(#gIra)" strokeWidth={2} name="Ira" dot={false} />
              <Area type="monotone" dataKey="desconfianza" stroke="#a78bfa" fill="url(#gDes)" strokeWidth={2} name="Desconfianza" dot={false} />
              <Area type="monotone" dataKey="esperanza" stroke="#22c55e" fill="url(#gEsp)" strokeWidth={2} name="Esperanza" dot={false} />
            </AreaChart>
          </ResponsiveContainer>
          <div style={{ display: 'flex', gap: 12, marginTop: 6, justifyContent: 'center' }}>
            {[{ color: '#ef4444', label: 'Ira' }, { color: '#a78bfa', label: 'Desconfianza' }, { color: '#22c55e', label: 'Esperanza' }].map(l => (
              <div key={l.label} style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: 10, color: 'var(--muted)' }}>
                <div style={{ width: 20, height: 2, background: l.color, borderRadius: 1 }} />
                {l.label}
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* ── Row 3: Arquetipos + Narrativas + Riesgos críticos ───────────── */}
      <div className="grid-2" style={{ marginBottom: 16 }}>

        {/* Arquetipos bar */}
        <motion.div
          className="card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: .45, duration: .4 }}
        >
          <div className="card-title">
            <Users size={13} style={{ display: 'inline', marginRight: 6 }} />
            Arquetipos Electorales
          </div>
          {arquetipos_top.length > 0 ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
              {arquetipos_top.map((a, i) => (
                <div key={i}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, marginBottom: 5 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                      <div style={{ width: 8, height: 8, borderRadius: '50%', background: ARCHETYPE_COLORS[i % ARCHETYPE_COLORS.length], flexShrink: 0 }} />
                      <span style={{ fontWeight: 600, color: 'var(--text)' }}>{a.nombre}</span>
                    </div>
                    <span style={{ color: ARCHETYPE_COLORS[i % ARCHETYPE_COLORS.length], fontWeight: 700 }}>{a.peso}%</span>
                  </div>
                  <div className="progress-bar">
                    <motion.div
                      className="progress-fill"
                      style={{ background: ARCHETYPE_COLORS[i % ARCHETYPE_COLORS.length], boxShadow: `0 0 8px ${ARCHETYPE_COLORS[i % ARCHETYPE_COLORS.length]}60` }}
                      initial={{ width: 0 }}
                      animate={{ width: `${a.peso}%` }}
                      transition={{ delay: .5 + i * .08, duration: .7, ease: 'easeOut' }}
                    />
                  </div>
                  {a.emocion && (
                    <div style={{ fontSize: 10, color: EMOTION_COLORS[a.emocion] || 'var(--muted)', marginTop: 2, display: 'flex', alignItems: 'center', gap: 3 }}>
                      <Activity size={8} /> {a.emocion}
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : <div className="empty-state" style={{ padding: 20 }}>Sin arquetipos</div>}
        </motion.div>

        {/* Riesgos críticos */}
        <motion.div
          className="card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: .5, duration: .4 }}
        >
          <div className="card-title">
            <ShieldAlert size={13} style={{ display: 'inline', marginRight: 6 }} />
            Riesgos Críticos Activos
          </div>
          {riesgos_criticos.length > 0 ? riesgos_criticos.map((r, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: .55 + i * .07 }}
              style={{
                display: 'flex', alignItems: 'flex-start', gap: 10, padding: '10px 0',
                borderBottom: i < riesgos_criticos.length - 1 ? '1px solid var(--border)' : 'none'
              }}
            >
              <div style={{ paddingTop: 2 }}>
                <PulseDot color={r.nivel === 'rojo' ? '#ef4444' : r.nivel === 'amarillo' ? '#f59e0b' : '#22c55e'} />
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--text)', marginBottom: 3 }}>{r.tema}</div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span style={{ fontSize: 10, color: 'var(--muted)', display: 'flex', alignItems: 'center', gap: 3 }}>
                    <Flame size={9} /> {'█'.repeat(r.velocidad)}{'░'.repeat(5 - r.velocidad)} vel.
                  </span>
                </div>
              </div>
              <RiskBadge nivel={r.nivel} />
            </motion.div>
          )) : (
            <div className="empty-state" style={{ padding: 20 }}>
              <ShieldAlert size={24} style={{ opacity: .3 }} />
              <div style={{ marginTop: 8 }}>Sin riesgos críticos activos</div>
            </div>
          )}
        </motion.div>
      </div>

      {/* ── Row 4: Narrativas + Lenguaje top ──────────────────────────── */}
      <div className="grid-2">
        {/* Narrativas por tipo */}
        <motion.div
          className="card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: .55, duration: .4 }}
        >
          <div className="card-title">
            <BookOpen size={13} style={{ display: 'inline', marginRight: 6 }} />
            Narrativas Activas por Tipo
          </div>
          {narrativas_por_tipo.length > 0 ? (
            <div style={{ display: 'flex', gap: 16, alignItems: 'center' }}>
              <ResponsiveContainer width="50%" height={180}>
                <PieChart>
                  <Pie data={narrativas_por_tipo} dataKey="count" nameKey="tipo"
                    cx="50%" cy="50%" outerRadius={70} innerRadius={35} strokeWidth={0}>
                    {narrativas_por_tipo.map((_, i) => (
                      <Cell key={i} fill={['#f5c518', '#3b82f6', '#06b6d4', '#22c55e', '#a78bfa'][i % 5]} />
                    ))}
                  </Pie>
                  <Tooltip {...TT_STYLE} />
                </PieChart>
              </ResponsiveContainer>
              <div style={{ flex: 1 }}>
                {narrativas_por_tipo.map((n, i) => (
                  <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                    <div style={{ width: 8, height: 8, borderRadius: 2, background: ['#f5c518', '#3b82f6', '#06b6d4', '#22c55e', '#a78bfa'][i % 5], flexShrink: 0 }} />
                    <span style={{ fontSize: 11, color: 'var(--text)', flex: 1 }}>{n.tipo}</span>
                    <span style={{ fontSize: 12, fontWeight: 700, color: ['#f5c518', '#3b82f6', '#06b6d4', '#22c55e', '#a78bfa'][i % 5] }}>{n.count}</span>
                  </div>
                ))}
              </div>
            </div>
          ) : <div className="empty-state" style={{ padding: 20 }}>Sin narrativas</div>}
        </motion.div>

        {/* Comunidades top */}
        <motion.div
          className="card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: .6, duration: .4 }}
        >
          <div className="card-title">
            <Globe2 size={13} style={{ display: 'inline', marginRight: 6 }} />
            Ecosistema de Comunidades Digitales
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {[
              { nombre: 'Noticias Potosí — Actualidad', plat: 'Facebook', tam: '185K', influencia: 9, color: '#3b82f6' },
              { nombre: 'Mineros del Cerro Rico', plat: 'TikTok', tam: '78K', influencia: 8, color: '#06b6d4' },
              { nombre: 'Cooperativistas FEDECOMIN', plat: 'WhatsApp', tam: '45K', influencia: 9, color: '#f5c518' },
              { nombre: 'Periodistas e Intelectuales Potosí', plat: 'Twitter/X', tam: '9.5K', influencia: 9, color: '#a78bfa' },
              { nombre: 'Canal Potosí Noticias', plat: 'YouTube', tam: '28K', influencia: 8, color: '#22c55e' },
            ].map((c, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <div style={{ width: 6, height: 28, borderRadius: 3, background: c.color, flexShrink: 0 }} />
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontSize: 11, fontWeight: 600, color: 'var(--text)' }}>{c.nombre}</div>
                  <div style={{ fontSize: 9, color: 'var(--muted)' }}>{c.plat} · {c.tam} miembros</div>
                </div>
                <div style={{ textAlign: 'right', flexShrink: 0 }}>
                  <div style={{ fontSize: 10, color: c.color, fontWeight: 700 }}>Inf. {c.influencia}/10</div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}
