import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, Cell } from 'recharts'
import api from '../api/client'
import { useProject } from '../context/ProjectContext'

const EMOC_COLORS = { ira:'#f76c6c', miedo:'#f7c948', frustracion:'#f7964a', esperanza:'#56c596', desconfianza:'#a78bfa', orgullo:'#4ecdc4' }

export default function Evolucion() {
  const { activeProject } = useProject()
  const [data, setData] = useState(null)

  useEffect(()=>{
    if (!activeProject) return
    api.get(`/evolution/${activeProject.id}`).then(r=>setData(r.data)).catch(console.error)
  },[activeProject])

  if (!activeProject) return <div className="empty-state"><span className="icon">🗂️</span>Selecciona un proyecto.</div>
  if (!data) return <div style={{padding:40,textAlign:'center'}}><div className="loader"/></div>

  // Pivot emociones por mes
  const emoMeses = {}
  data.emociones_por_mes.forEach(e=>{ if(!emoMeses[e.mes]) emoMeses[e.mes]={}; emoMeses[e.mes][e.tipo]=e.avg })
  const emoData = Object.entries(emoMeses).map(([mes,vals])=>({mes,...vals}))
  const tiposEmo = [...new Set(data.emociones_por_mes.map(e=>e.tipo))]

  // Pivot riesgos por mes
  const riesMeses = {}
  data.riesgos_por_mes.forEach(r=>{ if(!riesMeses[r.mes]) riesMeses[r.mes]={rojo:0,amarillo:0,verde:0}; riesMeses[r.mes][r.nivel]=r.count })
  const riesData = Object.entries(riesMeses).map(([mes,vals])=>({mes,...vals}))

  return (
    <div>
      <div className="page-header">
        <div className="page-header-left"><h2>📈 Evolución Temporal</h2><p>Seguimiento histórico de narrativas, emociones y riesgos</p></div>
      </div>

      <div className="card" style={{marginBottom:20}}>
        <div className="card-title">Narrativas detectadas por mes</div>
        {data.narrativas_por_mes.length ? (
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={data.narrativas_por_mes}>
              <CartesianGrid stroke="var(--border)" vertical={false} />
              <XAxis dataKey="mes" tick={{fill:'var(--muted)',fontSize:11}} />
              <YAxis tick={{fill:'var(--muted)',fontSize:11}} />
              <Tooltip contentStyle={{background:'var(--surface)',border:'1px solid var(--border)',color:'var(--text)'}} />
              <Bar dataKey="count" name="Narrativas" fill="var(--accent)" radius={[4,4,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        ) : <div className="empty-state" style={{padding:20}}><span className="icon" style={{fontSize:28}}>📖</span>Sin datos de narrativas con fecha</div>}
      </div>

      <div className="grid-2" style={{marginBottom:20}}>
        <div className="card">
          <div className="card-title">Intensidad emocional por mes</div>
          {emoData.length ? (
            <ResponsiveContainer width="100%" height={240}>
              <LineChart data={emoData}>
                <CartesianGrid stroke="var(--border)" />
                <XAxis dataKey="mes" tick={{fill:'var(--muted)',fontSize:10}} />
                <YAxis domain={[0,10]} tick={{fill:'var(--muted)',fontSize:10}} />
                <Tooltip contentStyle={{background:'var(--surface)',border:'1px solid var(--border)',color:'var(--text)'}} />
                <Legend wrapperStyle={{fontSize:11,color:'var(--muted)'}} />
                {tiposEmo.map(t=>(
                  <Line key={t} type="monotone" dataKey={t} stroke={EMOC_COLORS[t]||'var(--accent)'} strokeWidth={2} dot={false} />
                ))}
              </LineChart>
            </ResponsiveContainer>
          ) : <div className="empty-state" style={{padding:20}}><span className="icon" style={{fontSize:28}}>🎭</span>Sin datos con fecha</div>}
        </div>

        <div className="card">
          <div className="card-title">Riesgos detectados por mes</div>
          {riesData.length ? (
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={riesData}>
                <CartesianGrid stroke="var(--border)" vertical={false} />
                <XAxis dataKey="mes" tick={{fill:'var(--muted)',fontSize:11}} />
                <YAxis tick={{fill:'var(--muted)',fontSize:11}} />
                <Tooltip contentStyle={{background:'var(--surface)',border:'1px solid var(--border)',color:'var(--text)'}} />
                <Legend wrapperStyle={{fontSize:11}} />
                <Bar dataKey="rojo"     name="Crítico"   fill="var(--accent4)" stackId="a" />
                <Bar dataKey="amarillo" name="Atención"  fill="var(--accent3)" stackId="a" />
                <Bar dataKey="verde"    name="Bajo"      fill="var(--success)" stackId="a" radius={[4,4,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : <div className="empty-state" style={{padding:20}}><span className="icon" style={{fontSize:28}}>⚠️</span>Sin riesgos con fecha</div>}
        </div>
      </div>
    </div>
  )
}
