import React, { useEffect, useState } from "react"
import { apiGet } from "../api"

export default function Movements() {
  const [items, setItems] = useState([])
  const [productId, setProductId] = useState("")
  const [limit, setLimit] = useState(50)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  const load = async () => {
    try {
      setLoading(true)
      const query = new URLSearchParams()
      if (productId) query.set("product_id", productId)
      if (limit) query.set("limit", String(limit))
      const data = await apiGet(`/api/movements?${query.toString()}`)
      setItems(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  return (
    <div style={{marginTop:24}}>
      <h3>Historial de movimientos</h3>
      <div style={{display:"flex", gap:8, marginBottom:8}}>
        <input placeholder="Filtrar por product_id" value={productId} onChange={e => setProductId(e.target.value)} />
        <input placeholder="Límite" type="number" value={limit} onChange={e => setLimit(parseInt(e.target.value||"0",10))} />
        <button onClick={load}>Refrescar</button>
      </div>
      {loading && <div>Cargando movimientos...</div>}
      {error && <div style={{color:"crimson"}}>Error: {error}</div>}
      {!loading && !error && (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{textAlign:"left", borderBottom:"1px solid #ccc"}}>ID</th>
              <th style={{textAlign:"left", borderBottom:"1px solid #ccc"}}>Producto</th>
              <th style={{textAlign:"right", borderBottom:"1px solid #ccc"}}>Delta</th>
              <th style={{textAlign:"right", borderBottom:"1px solid #ccc"}}>Antes</th>
              <th style={{textAlign:"right", borderBottom:"1px solid #ccc"}}>Después</th>
              <th style={{textAlign:"left", borderBottom:"1px solid #ccc"}}>Tipo</th>
              <th style={{textAlign:"left", borderBottom:"1px solid #ccc"}}>Motivo</th>
              <th style={{textAlign:"left", borderBottom:"1px solid #ccc"}}>Fecha</th>
            </tr>
          </thead>
          <tbody>
            {items.map(it => (
              <tr key={it.id}>
                <td>{it.id}</td>
                <td>{it.product_id}</td>
                <td style={{textAlign:"right"}}>{it.delta}</td>
                <td style={{textAlign:"right"}}>{it.qty_before}</td>
                <td style={{textAlign:"right"}}>{it.qty_after}</td>
                <td>{it.type}</td>
                <td>{it.reason || "-"}</td>
                <td>{new Date(it.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
