import { useState, useEffect } from 'react'
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer,
         PieChart, Pie, Cell, Tooltip, Legend, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts'
import api from '../api/client'
import { useProject } from '../context/ProjectContext'

const EMOTION_COLORS = { ira:'#f76c6c', miedo:'#f7c948', frustracion:'#f7964a', esperanza:'#56c596', desconfianza:'#a78bfa', orgullo:'#4ecdc4' }
const PIE_COLORS = ['#7c6af7','#4ecdc4','#f7c948','#f76c6c','#56c596','#a78bfa']

// Tooltip dark style — hardcoded so it works inside Recharts portals
const TT = {
  contentStyle: { background: '#1a1d27', border: '1px solid #3a3f5c', borderRadius: 8, color: '#e8eaf6', fontSize: 12 },
  labelStyle:   { color: '#e8eaf6', fontWeight: 600 },
  itemStyle:    { color: '#c8cde8' },
}

export default function Dashboard() {
  const { activeProject } = useProject()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!activeProject) return
    setLoading(true)
    api.get(`/dashboard/${activeProject.id}`)
      .then(r => setData(r.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [activeProject])

  if (!activeProject) return (
    <div className="empty-state"><span className="icon">🗂️</span>Selecciona un proyecto en la sección <strong>Proyectos</strong> para ver el dashboard.</div>
  )
  if (loading) return <div style={{padding:40,textAlign:'center'}}><div className="loader" /></div>
  if (!data) return null

  const { totales, riesgos, emociones_radar, narrativas_por_tipo, arquetipos_top, riesgos_criticos } = data

  // Radar: normalize avg (0-10) → full (0-10), add color per emotion
  const radarData = emociones_radar.map(e => ({
    tipo: e.tipo,
    valor: e.avg,
    color: EMOTION_COLORS[e.tipo] || '#7c6af7',
  }))

  return (
    <div>
      <div className="page-header">
        <div className="page-header-left">
          <h2>📊 {activeProject.nombre}</h2>
          <p>{activeProject.cliente}{activeProject.contexto_pais ? ` · ${activeProject.contexto_pais}` : ''}</p>
        </div>
        <div style={{fontSize:12,color:'var(--muted)'}}>{new Date().toLocaleDateString('es',{weekday:'long',year:'numeric',month:'long',day:'numeric'})}</div>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        <div className="stat-card"><div className="label">Narrativas</div><div className="value c-purple">{totales.narrativas}</div><div className="sub">relatos registrados</div></div>
        <div className="stat-card"><div className="label">Emociones</div><div className="value c-teal">{totales.emociones}</div><div className="sub">registros emocionales</div></div>
        <div className="stat-card"><div className="label">Arquetipos</div><div className="value c-yellow">{totales.arquetipos}</div><div className="sub">perfiles de actor</div></div>
        <div className="stat-card"><div className="label">Lenguaje</div><div className="value c-green">{totales.lenguaje}</div><div className="sub">términos culturales</div></div>
        <div className="stat-card"><div className="label">Comunidades</div><div className="value" style={{color:'var(--accent2)'}}>{totales.comunidades}</div><div className="sub">grupos digitales</div></div>
        <div className="stat-card">
          <div className="label">Semáforo de riesgos</div>
          <div style={{display:'flex',gap:12,marginTop:8,alignItems:'center'}}>
            <span><span className="dot-rojo" /> <span style={{fontSize:20,fontWeight:800,color:'var(--accent4)'}}>{riesgos.rojo}</span></span>
            <span><span className="dot-amarillo" /> <span style={{fontSize:20,fontWeight:800,color:'var(--accent3)'}}>{riesgos.amarillo}</span></span>
            <span><span className="dot-verde" /> <span style={{fontSize:20,fontWeight:800,color:'var(--success)'}}>{riesgos.verde}</span></span>
          </div>
        </div>
      </div>

      {/* Charts row */}
      <div className="grid-2" style={{marginBottom:20}}>

        {/* ── Mapa emocional radar ─────────────────────────────────────── */}
        <div className="card">
          <div className="card-title">Mapa emocional (radar)</div>
          {radarData.length ? (
            <ResponsiveContainer width="100%" height={240}>
              <RadarChart data={radarData} margin={{top:10,right:20,bottom:10,left:20}}>
                <PolarGrid stroke="#2e3350" />
                <PolarAngleAxis
                  dataKey="tipo"
                  tick={({ x, y, payload }) => {
                    const color = EMOTION_COLORS[payload.value] || '#7b82a8'
                    return (
                      <text x={x} y={y} textAnchor="middle" dominantBaseline="central"
                        fontSize={11} fontWeight={600} fill={color}>
                        {payload.value}
                      </text>
                    )
                  }}
                />
                <PolarRadiusAxis
                  angle={90} domain={[0, 10]}
                  tick={{fill:'#4a5580', fontSize:9}}
                  axisLine={false} tickCount={4}
                />
                <Radar
                  name="Intensidad"
                  dataKey="valor"
                  stroke="var(--accent)"
                  fill="var(--accent)"
                  fillOpacity={0.25}
                  strokeWidth={2}
                />
                <Tooltip
                  {...TT}
                  formatter={(value) => [`${value} / 10`, 'Intensidad promedio']}
                />
              </RadarChart>
            </ResponsiveContainer>
          ) : <div className="empty-state" style={{padding:20}}><span className="icon" style={{fontSize:24}}>🎭</span>Sin datos emocionales</div>}
        </div>

        {/* ── Narrativas por tipo pie ──────────────────────────────────── */}
        <div className="card">
          <div className="card-title">Narrativas por tipo</div>
          {narrativas_por_tipo.length ? (
            <ResponsiveContainer width="100%" height={240}>
              <PieChart>
                <Pie
                  data={narrativas_por_tipo}
                  dataKey="count"
                  nameKey="tipo"
                  cx="50%" cy="50%"
                  outerRadius={85}
                  innerRadius={38}
                  label={({tipo, percent, x, y}) => (
                    <text x={x} y={y} textAnchor="middle" dominantBaseline="central"
                      fontSize={11} fill="#c8cde8">
                      {tipo} {(percent*100).toFixed(0)}%
                    </text>
                  )}
                  labelLine={{stroke:'#3a3f5c'}}
                >
                  {narrativas_por_tipo.map((_, i) => <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />)}
                </Pie>
                <Tooltip {...TT} />
                <Legend
                  wrapperStyle={{fontSize:12, color:'#c8cde8'}}
                  formatter={(value) => <span style={{color:'#c8cde8'}}>{value}</span>}
                />
              </PieChart>
            </ResponsiveContainer>
          ) : <div className="empty-state" style={{padding:20}}><span className="icon" style={{fontSize:24}}>📖</span>Sin narrativas</div>}
        </div>
      </div>

      {/* Bottom row */}
      <div className="grid-2">
        <div className="card">
          <div className="card-title">Arquetipos principales</div>
          {arquetipos_top.length ? arquetipos_top.map((a,i) => (
            <div key={i} style={{marginBottom:12}}>
              <div style={{display:'flex',justifyContent:'space-between',fontSize:13,marginBottom:4}}>
                <span style={{fontWeight:600}}>{a.nombre}</span>
                <span style={{color:'var(--muted)'}}>{a.peso}%</span>
              </div>
              <div className="progress-bar"><div className="progress-fill" style={{width:`${a.peso}%`}} /></div>
              {a.emocion && <div style={{fontSize:11,color: EMOTION_COLORS[a.emocion] || 'var(--muted)',marginTop:2}}>● {a.emocion}</div>}
            </div>
          )) : <div className="empty-state" style={{padding:20}}><span className="icon" style={{fontSize:24}}>👤</span>Sin arquetipos</div>}
        </div>

        <div className="card">
          <div className="card-title">Riesgos críticos activos</div>
          {riesgos_criticos.length ? riesgos_criticos.map((r,i) => (
            <div key={i} style={{display:'flex',alignItems:'center',gap:10,padding:'8px 0',borderBottom:'1px solid var(--border)'}}>
              <span className={`dot-${r.nivel}`} />
              <div style={{flex:1}}>
                <div style={{fontSize:13,fontWeight:600}}>{r.tema}</div>
                <div style={{fontSize:11,color:'var(--muted)'}}>Velocidad: {'🔥'.repeat(r.velocidad)}</div>
              </div>
              <span className={`badge badge-${r.nivel==='rojo'?'red':r.nivel==='amarillo'?'yellow':'green'}`}>{r.nivel}</span>
            </div>
          )) : <div className="empty-state" style={{padding:20}}><span className="icon" style={{fontSize:24}}>✅</span>Sin riesgos críticos</div>}
        </div>
      </div>
    </div>
  )
}
