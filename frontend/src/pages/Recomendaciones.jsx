import { useState } from 'react'
import api from '../api/client'
import { useProject } from '../context/ProjectContext'

const URGENCIA_COLOR = { inmediata:'var(--accent4)', esta_semana:'var(--accent3)', este_mes:'var(--success)' }
const PRIO_BADGE = { alta:'badge-red', media:'badge-yellow', baja:'badge-green' }

export default function Recomendaciones() {
  const { activeProject } = useProject()
  const [loading, setLoading] = useState(false)
  const [result, setResult]   = useState(null)
  const [error, setError]     = useState(null)

  const generate = async () => {
    if (!activeProject) return alert('Selecciona un proyecto')
    setLoading(true); setResult(null); setError(null)
    try {
      const { data } = await api.post('/ai/recommend', { project_id: activeProject.id })
      setResult(data)
    } catch(e) { setError(e.message) }
    finally { setLoading(false) }
  }

  if (!activeProject) return <div className="empty-state"><span className="icon">🗂️</span>Selecciona un proyecto.</div>

  return (
    <div>
      <div className="page-header">
        <div className="page-header-left">
          <h2>💡 Recomendaciones Estratégicas</h2>
          <p>SocialRank IA analiza todos tus datos y genera recomendaciones de comunicación</p>
        </div>
        <button className="btn btn-primary" onClick={generate} disabled={loading}>
          {loading ? <><span className="loader" style={{width:14,height:14}} /> Analizando...</> : '💡 Generar recomendaciones'}
        </button>
      </div>

      {!result && !loading && !error && (
        <div className="card">
          <div style={{padding:'20px 0',textAlign:'center'}}>
            <div style={{fontSize:48,marginBottom:16}}>🤖</div>
            <h3 style={{marginBottom:8}}>Análisis estratégico con IA</h3>
            <p style={{fontSize:13,color:'var(--muted)',maxWidth:480,margin:'0 auto',lineHeight:1.6}}>
              SocialRank IA leerá todos los datos del proyecto — narrativas, emociones, arquetipos, lenguaje y riesgos —
              y generará recomendaciones estratégicas sobre <strong>qué decir, qué no decir, en qué canal, con qué tono y cuándo</strong>.
            </p>
            <button className="btn btn-primary" style={{marginTop:20}} onClick={generate}>
              💡 Generar ahora
            </button>
          </div>
        </div>
      )}

      {loading && (
        <div className="card" style={{textAlign:'center',padding:40}}>
          <div className="loader" style={{width:32,height:32,margin:'0 auto 16px',borderWidth:3}} />
          <p style={{color:'var(--muted)'}}>SocialRank IA está leyendo tus datos y generando recomendaciones...</p>
        </div>
      )}

      {error && <div className="card"><p style={{color:'var(--accent4)'}}>✗ {error}</p></div>}

      {result && !result.error && (
        <div>
          {/* Diagnóstico */}
          <div className="card" style={{marginBottom:16,borderLeft:'3px solid var(--accent)'}}>
            <div className="card-title">🔍 Diagnóstico general</div>
            <p style={{fontSize:13,lineHeight:1.7}}>{result.diagnostico_general}</p>
            {result.momento_optimo && (
              <div style={{marginTop:12,display:'flex',alignItems:'center',gap:10}}>
                <span style={{fontSize:11,color:'var(--muted)'}}>URGENCIA:</span>
                <span className="badge" style={{background:`${URGENCIA_COLOR[result.momento_optimo.urgencia]}22`,color:URGENCIA_COLOR[result.momento_optimo.urgencia]}}>
                  {result.momento_optimo.urgencia?.replace(/_/g,' ')}
                </span>
                <span style={{fontSize:12,color:'var(--muted)'}}>{result.momento_optimo.descripcion}</span>
              </div>
            )}
          </div>

          <div className="grid-2" style={{marginBottom:16}}>
            {/* Qué decir */}
            {result.que_decir?.length > 0 && (
              <div className="card" style={{borderLeft:'3px solid var(--success)'}}>
                <div className="card-title">✅ Qué decir</div>
                {result.que_decir.map((q,i)=>(
                  <div key={i} style={{marginBottom:12,paddingBottom:12,borderBottom:'1px solid var(--border)'}}>
                    <p style={{fontSize:13,fontWeight:600,marginBottom:3}}>"{q.mensaje}"</p>
                    <p style={{fontSize:12,color:'var(--muted)'}}>{q.razon}</p>
                    {q.arquetipo_objetivo && <span className="badge badge-teal" style={{marginTop:4}}>{q.arquetipo_objetivo}</span>}
                  </div>
                ))}
              </div>
            )}

            {/* Qué NO decir */}
            {result.que_no_decir?.length > 0 && (
              <div className="card" style={{borderLeft:'3px solid var(--accent4)'}}>
                <div className="card-title">🚫 Qué NO decir</div>
                {result.que_no_decir.map((q,i)=>(
                  <div key={i} style={{marginBottom:12,paddingBottom:12,borderBottom:'1px solid var(--border)'}}>
                    <p style={{fontSize:13,fontWeight:600,marginBottom:3,textDecoration:'line-through',color:'var(--accent4)'}}>"{q.mensaje}"</p>
                    <p style={{fontSize:12,color:'var(--muted)'}}>{q.razon}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Canales */}
          {result.canales_prioritarios?.length > 0 && (
            <div className="card" style={{marginBottom:16}}>
              <div className="card-title">📡 Canales prioritarios</div>
              <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(220px,1fr))',gap:12}}>
                {result.canales_prioritarios.map((c,i)=>(
                  <div key={i} style={{background:'var(--surface2)',border:'1px solid var(--border)',borderRadius:8,padding:12}}>
                    <div style={{fontWeight:700,fontSize:14,marginBottom:4}}>{c.canal}</div>
                    <p style={{fontSize:12,color:'var(--muted)',marginBottom:6}}>{c.razon}</p>
                    {c.formato_recomendado && <span className="badge badge-purple">{c.formato_recomendado}</span>}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Tono */}
          {result.tono_recomendado && (
            <div className="card" style={{marginBottom:16}}>
              <div className="card-title">🎯 Tono recomendado</div>
              <p style={{fontSize:13,marginBottom:10}}>{result.tono_recomendado.descripcion}</p>
              <div style={{display:'flex',gap:16,flexWrap:'wrap'}}>
                {result.tono_recomendado.palabras_clave?.length > 0 && (
                  <div>
                    <div style={{fontSize:11,color:'var(--success)',fontWeight:600,marginBottom:5}}>✓ USAR</div>
                    <div className="tag-list">{result.tono_recomendado.palabras_clave.map((p,i)=><span key={i} className="tag" style={{borderColor:'var(--success)',color:'var(--success)'}}>{p}</span>)}</div>
                  </div>
                )}
                {result.tono_recomendado.palabras_a_evitar?.length > 0 && (
                  <div>
                    <div style={{fontSize:11,color:'var(--accent4)',fontWeight:600,marginBottom:5}}>✗ EVITAR</div>
                    <div className="tag-list">{result.tono_recomendado.palabras_a_evitar.map((p,i)=><span key={i} className="tag" style={{borderColor:'var(--accent4)',color:'var(--accent4)'}}>{p}</span>)}</div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Acciones */}
          {result.acciones_prioritarias?.length > 0 && (
            <div className="card">
              <div className="card-title">🚀 Acciones prioritarias</div>
              <table>
                <thead><tr><th>Acción</th><th>Prioridad</th><th>Plazo</th></tr></thead>
                <tbody>
                  {result.acciones_prioritarias.map((a,i)=>(
                    <tr key={i}>
                      <td>{a.accion}</td>
                      <td><span className={`badge ${PRIO_BADGE[a.prioridad]||'badge-gray'}`}>{a.prioridad}</span></td>
                      <td style={{fontSize:12,color:'var(--muted)'}}>{a.plazo}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
