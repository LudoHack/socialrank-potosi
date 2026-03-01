import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
         ResponsiveContainer, BarChart, Bar, Cell, Area, AreaChart } from 'recharts'
import api from '../api/client'
import { useProject } from '../context/ProjectContext'

const EMOC_COLORS = {
  ira:          '#f76c6c',
  miedo:        '#f7c948',
  frustracion:  '#f7964a',
  esperanza:    '#56c596',
  desconfianza: '#a78bfa',
  orgullo:      '#4ecdc4',
}

const TOOLTIP_STYLE  = { background: '#1a1d27', border: '1px solid #3a3f5c', borderRadius: 8, fontSize: 12 }
const LABEL_STYLE    = { color: '#e8eaf6', fontWeight: 600 }
const ITEM_STYLE     = { color: '#c8cde8' }
const TICK_MUTED     = { fill: '#8b92b8', fontSize: 11 }
const TICK_BRIGHT    = { fill: '#c8cde8', fontSize: 11 }
const GRID_COLOR     = '#2a2f4c'

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
  data.emociones_por_mes.forEach(e=>{
    if(!emoMeses[e.mes]) emoMeses[e.mes]={}
    emoMeses[e.mes][e.tipo]=e.avg
  })
  const emoData   = Object.entries(emoMeses).map(([mes,vals])=>({mes,...vals}))
  const tiposEmo  = [...new Set(data.emociones_por_mes.map(e=>e.tipo))]

  // Pivot riesgos por mes
  const riesMeses = {}
  data.riesgos_por_mes.forEach(r=>{
    if(!riesMeses[r.mes]) riesMeses[r.mes]={rojo:0,amarillo:0,verde:0}
    riesMeses[r.mes][r.nivel]=r.count
  })
  const riesData = Object.entries(riesMeses).map(([mes,vals])=>({mes,...vals}))

  return (
    <div>
      <div className="page-header">
        <div className="page-header-left">
          <h2>📈 Evolución Temporal</h2>
          <p>Seguimiento histórico de narrativas, emociones y riesgos</p>
        </div>
      </div>

      {/* Narrativas por mes */}
      <div className="card" style={{marginBottom:20}}>
        <div className="card-title">Narrativas detectadas por mes</div>
        {data.narrativas_por_mes.length ? (
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={data.narrativas_por_mes} margin={{top:5,right:20,bottom:5,left:0}}>
              <CartesianGrid stroke={GRID_COLOR} vertical={false} />
              <XAxis dataKey="mes" tick={TICK_MUTED} />
              <YAxis tick={TICK_MUTED} allowDecimals={false} />
              <Tooltip
                contentStyle={TOOLTIP_STYLE}
                labelStyle={LABEL_STYLE}
                itemStyle={ITEM_STYLE}
                formatter={(v) => [v, 'Narrativas']}
              />
              <Bar dataKey="count" name="Narrativas" radius={[6,6,0,0]}>
                {data.narrativas_por_mes.map((_, i) => (
                  <Cell key={i} fill={i % 2 === 0 ? '#a78bfa' : '#7c6fdb'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <div className="empty-state" style={{padding:20}}>
            <span className="icon" style={{fontSize:28}}>📖</span>
            Sin datos de narrativas con fecha
          </div>
        )}
      </div>

      <div className="grid-2" style={{marginBottom:20}}>

        {/* Emociones por mes */}
        <div className="card">
          <div className="card-title">Intensidad emocional por mes</div>
          {emoData.length ? (
            <ResponsiveContainer width="100%" height={260}>
              <LineChart data={emoData} margin={{top:5,right:20,bottom:5,left:0}}>
                <CartesianGrid stroke={GRID_COLOR} />
                <XAxis dataKey="mes" tick={TICK_MUTED} />
                <YAxis domain={[0,10]} tick={TICK_MUTED} />
                <Tooltip
                  contentStyle={TOOLTIP_STYLE}
                  labelStyle={LABEL_STYLE}
                  itemStyle={ITEM_STYLE}
                />
                <Legend
                  wrapperStyle={{fontSize:11, paddingTop:8}}
                  formatter={(value) => (
                    <span style={{color: EMOC_COLORS[value] || '#c8cde8'}}>{value}</span>
                  )}
                />
                {tiposEmo.map(t=>(
                  <Line
                    key={t}
                    type="monotone"
                    dataKey={t}
                    stroke={EMOC_COLORS[t] || '#a78bfa'}
                    strokeWidth={2.5}
                    dot={{ fill: EMOC_COLORS[t] || '#a78bfa', r: 5, strokeWidth: 0 }}
                    activeDot={{ r: 7 }}
                  />
                ))}
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state" style={{padding:20}}>
              <span className="icon" style={{fontSize:28}}>🎭</span>
              Sin datos con fecha
            </div>
          )}
        </div>

        {/* Riesgos por mes */}
        <div className="card">
          <div className="card-title">Riesgos detectados por mes</div>
          {riesData.length ? (
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={riesData} margin={{top:5,right:20,bottom:5,left:0}}>
                <CartesianGrid stroke={GRID_COLOR} vertical={false} />
                <XAxis dataKey="mes" tick={TICK_MUTED} />
                <YAxis tick={TICK_MUTED} allowDecimals={false} />
                <Tooltip
                  contentStyle={TOOLTIP_STYLE}
                  labelStyle={LABEL_STYLE}
                  itemStyle={ITEM_STYLE}
                />
                <Legend
                  wrapperStyle={{fontSize:11, paddingTop:8}}
                  formatter={(value) => (
                    <span style={{color: value==='Crítico'?'#f76c6c': value==='Atención'?'#f7c948':'#56c596'}}>
                      {value}
                    </span>
                  )}
                />
                <Bar dataKey="rojo"     name="Crítico"  fill="#f76c6c" stackId="a" />
                <Bar dataKey="amarillo" name="Atención" fill="#f7c948" stackId="a" />
                <Bar dataKey="verde"    name="Bajo"     fill="#56c596" stackId="a" radius={[6,6,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state" style={{padding:20}}>
              <span className="icon" style={{fontSize:28}}>⚠️</span>
              Sin riesgos con fecha
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
