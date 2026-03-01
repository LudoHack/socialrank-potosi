import { useState, useEffect } from 'react'
import api from '../api/client'
import { useProject } from '../context/ProjectContext'

const NIVEL_COLOR = { bajo:'var(--success)', medio:'var(--accent3)', alto:'var(--accent4)', critico:'#ff0044' }
const RECEP_COLOR = { alto:'var(--success)', medio:'var(--accent3)', bajo:'var(--accent4)', rechazo:'#ff0044' }

export default function Simulacion() {
  const { activeProject } = useProject()
  const [mensaje, setMensaje]     = useState('')
  const [loading, setLoading]     = useState(false)
  const [result, setResult]       = useState(null)
  const [error, setError]         = useState(null)
  const [history, setHistory]     = useState([])
  const [showHistory, setShowHistory] = useState(false)

  const loadHistory = () => {
    if (!activeProject) return
    api.get(`/ai/simulations/${activeProject.id}`).then(r=>setHistory(r.data)).catch(()=>{})
  }
  useEffect(()=>{ loadHistory() },[activeProject])

  const simulate = async () => {
    if (!mensaje.trim()) return alert('Escribe un mensaje para simular')
    if (!activeProject) return alert('Selecciona un proyecto')
    setLoading(true); setResult(null); setError(null)
    try {
      const { data } = await api.post('/ai/simulate', { project_id: activeProject.id, mensaje })
      setResult(data)
      loadHistory()
    } catch(e) { setError(e.message) }
    finally { setLoading(false) }
  }

  if (!activeProject) return <div className="empty-state"><span className="icon">🗂️</span>Selecciona un proyecto.</div>

  return (
    <div>
      <div className="page-header">
        <div className="page-header-left">
          <h2>🤖 Simulación de Mensajes</h2>
          <p>Analiza cómo reaccionarán tus arquetipos ante un mensaje usando SocialRank IA</p>
        </div>
        <button className="btn btn-outline btn-sm" onClick={()=>setShowHistory(!showHistory)}>
          🕐 Historial ({history.length})
        </button>
      </div>

      {showHistory && history.length > 0 && (
        <div className="card" style={{marginBottom:20}}>
          <div className="card-title">Simulaciones anteriores</div>
          {history.map(h=>(
            <div key={h.id} style={{padding:'10px 0',borderBottom:'1px solid var(--border)',cursor:'pointer'}} onClick={()=>{ setResult(h.resultado); setMensaje(h.mensaje); setShowHistory(false) }}>
              <div style={{fontSize:13,fontWeight:600,marginBottom:3}}>"{h.mensaje.slice(0,80)}{h.mensaje.length>80?'…':''}"</div>
              <div style={{display:'flex',gap:10}}>
                {h.resultado?.riesgo_general && <span className="badge" style={{background:`${NIVEL_COLOR[h.resultado.riesgo_general]}22`,color:NIVEL_COLOR[h.resultado.riesgo_general]}}>Riesgo: {h.resultado.riesgo_general}</span>}
                <span style={{fontSize:11,color:'var(--muted)'}}>{new Date(h.fecha).toLocaleDateString('es')}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="card" style={{marginBottom:20}}>
        <div className="card-title">Mensaje a simular</div>
        <textarea
          value={mensaje}
          onChange={e=>setMensaje(e.target.value)}
          placeholder="Escribe aquí el mensaje, discurso o comunicación que quieres simular. Ej: 'Vamos a recuperar los empleos perdidos y devolverle la dignidad a cada familia trabajadora...'"
          style={{width:'100%',minHeight:100,marginBottom:12}}
        />
        <button className="btn btn-primary" onClick={simulate} disabled={loading}>
          {loading ? <><span className="loader" style={{width:14,height:14}} /> Analizando con SocialRank IA...</> : '🤖 Simular con IA'}
        </button>
        {error && <p style={{color:'var(--accent4)',fontSize:13,marginTop:10}}>✗ {error}</p>}
      </div>

      {result && !result.error && (
        <div>
          {/* Resumen ejecutivo */}
          <div className="card" style={{marginBottom:16,borderLeft:`3px solid ${NIVEL_COLOR[result.riesgo_general]||'var(--accent)'}`}}>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-start',marginBottom:10}}>
              <div className="card-title" style={{margin:0}}>Diagnóstico general</div>
              <span className="badge" style={{background:`${NIVEL_COLOR[result.riesgo_general]}22`,color:NIVEL_COLOR[result.riesgo_general]}}>
                Riesgo {result.riesgo_general?.toUpperCase()}
              </span>
            </div>
            <p style={{fontSize:13,lineHeight:1.6}}>{result.resumen_ejecutivo}</p>
          </div>

          {/* Reacciones por arquetipo */}
          {result.reacciones_por_arquetipo?.length > 0 && (
            <div className="card" style={{marginBottom:16}}>
              <div className="card-title">Reacciones por arquetipo</div>
              <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(240px,1fr))',gap:12}}>
                {result.reacciones_por_arquetipo.map((r,i)=>(
                  <div key={i} style={{background:'var(--surface2)',border:`1px solid ${RECEP_COLOR[r.nivel_receptividad]||'var(--border)'}`,borderRadius:8,padding:12}}>
                    <div style={{fontWeight:700,fontSize:13,marginBottom:4}}>{r.arquetipo}</div>
                    <div style={{display:'flex',gap:6,marginBottom:6}}>
                      <span className="badge badge-gray">{r.emocion_activada}</span>
                      <span className="badge" style={{background:`${RECEP_COLOR[r.nivel_receptividad]}22`,color:RECEP_COLOR[r.nivel_receptividad]}}>{r.nivel_receptividad}</span>
                    </div>
                    <p style={{fontSize:12,color:'var(--muted)',lineHeight:1.5}}>{r.reaccion_esperada}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="grid-2" style={{marginBottom:16}}>
            {result.fortalezas_del_mensaje?.length > 0 && (
              <div className="card">
                <div className="card-title">✅ Fortalezas</div>
                {result.fortalezas_del_mensaje.map((f,i)=>(
                  <div key={i} className="ai-item">{f}</div>
                ))}
              </div>
            )}
            {result.riesgos_del_mensaje?.length > 0 && (
              <div className="card" style={{borderLeft:'3px solid var(--accent4)'}}>
                <div className="card-title">⚠️ Riesgos del mensaje</div>
                {result.riesgos_del_mensaje.map((r,i)=>(
                  <div key={i} className="ai-item" style={{'--ai-color':'var(--accent4)'}}>{r}</div>
                ))}
              </div>
            )}
          </div>

          {result.version_optimizada && (
            <div className="card" style={{borderLeft:'3px solid var(--accent2)'}}>
              <div className="card-title">💡 Versión optimizada sugerida</div>
              <p style={{fontSize:14,lineHeight:1.7,fontStyle:'italic',color:'var(--accent2)'}}>{result.version_optimizada}</p>
              {result.ajuste_de_tono_sugerido && (
                <p style={{fontSize:12,color:'var(--muted)',marginTop:8}}>💬 {result.ajuste_de_tono_sugerido}</p>
              )}
            </div>
          )}
        </div>
      )}
      {result?.error && (
        <div className="card"><p style={{color:'var(--accent4)'}}>{result.error}</p><pre style={{fontSize:11,color:'var(--muted)',marginTop:10,overflow:'auto'}}>{result.raw}</pre></div>
      )}
    </div>
  )
}
