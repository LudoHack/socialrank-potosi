import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import api from '../../api/client'

export default function ExcelUpload({ projectId, onSuccess }) {
  const [uploading, setUploading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const onDrop = useCallback(async (files) => {
    if (!files.length || !projectId) return
    const file = files[0]
    setUploading(true); setResult(null); setError(null)
    const form = new FormData()
    form.append('file', file)
    try {
      const { data } = await api.post(`/upload/${projectId}`, form, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setResult(data.importados)
      onSuccess?.()
    } catch (e) {
      setError(e.message)
    } finally {
      setUploading(false)
    }
  }, [projectId, onSuccess])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop, accept: { 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'], 'application/vnd.ms-excel': ['.xls'] },
    multiple: false
  })

  const downloadTemplate = async () => {
    const resp = await fetch('/api/upload/template')
    const blob = await resp.blob()
    const a = document.createElement('a')
    a.href = URL.createObjectURL(blob)
    a.download = 'template_etnografica.xlsx'
    a.click()
  }

  return (
    <div style={{ marginBottom: 20 }}>
      <div style={{ display: 'flex', gap: 10, marginBottom: 12, alignItems: 'center' }}>
        <span style={{ fontSize: 13, color: 'var(--muted)' }}>¿Primera vez?</span>
        <button className="btn btn-outline btn-sm" onClick={downloadTemplate}>
          📥 Descargar template Excel
        </button>
      </div>

      <div
        {...getRootProps()}
        style={{
          border: `2px dashed ${isDragActive ? 'var(--accent)' : 'var(--border)'}`,
          borderRadius: 10,
          padding: '32px 20px',
          textAlign: 'center',
          background: isDragActive ? 'rgba(124,106,247,.08)' : 'var(--surface2)',
          cursor: 'pointer',
          transition: 'all .2s'
        }}
      >
        <input {...getInputProps()} />
        {uploading
          ? <><div className="loader" style={{ margin: '0 auto 8px' }} /><p style={{ fontSize: 13, color: 'var(--muted)' }}>Importando datos...</p></>
          : <>
              <div style={{ fontSize: 32, marginBottom: 8 }}>📂</div>
              <p style={{ fontSize: 13, color: 'var(--text)' }}>
                {isDragActive ? 'Suelta el archivo aquí' : 'Arrastra tu Excel aquí o haz clic para seleccionar'}
              </p>
              <p style={{ fontSize: 11, color: 'var(--muted)', marginTop: 4 }}>Acepta .xlsx / .xls con las hojas del template</p>
            </>
        }
      </div>

      {result && (
        <div style={{ marginTop: 12, padding: '12px 16px', background: 'rgba(86,197,150,.1)', border: '1px solid var(--success)', borderRadius: 8 }}>
          <p style={{ fontSize: 13, color: 'var(--success)', fontWeight: 600, marginBottom: 6 }}>✓ Importación exitosa</p>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {Object.entries(result).map(([k, v]) => (
              <span key={k} className="badge badge-green">{k}: {v}</span>
            ))}
          </div>
        </div>
      )}
      {error && (
        <div style={{ marginTop: 12, padding: '12px 16px', background: 'rgba(247,108,108,.1)', border: '1px solid var(--accent4)', borderRadius: 8 }}>
          <p style={{ fontSize: 13, color: 'var(--accent4)' }}>✗ {error}</p>
        </div>
      )}
    </div>
  )
}
