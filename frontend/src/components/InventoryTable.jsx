// Componente React que muestra y gestiona el inventario, permitiendo ajustar stock y registrar movimientos.

import React, { useEffect, useState } from "react"
import { apiGet, apiPatch, apiPost } from "../api"

export default function InventoryTable({ onChanged }) {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  const load = async () => {
    try {
      setLoading(true)
      const data = await apiGet("/api/products")
      setItems(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const adjust = async (id, current) => {
    const qtyStr = prompt(`Nueva cantidad para ID ${id} (actual ${current}):`, String(current))
    if (qtyStr == null) return
    const quantity = parseInt(qtyStr, 10)
    if (Number.isNaN(quantity) || quantity < 0) return alert("Cantidad inválida")
    try {
      await apiPatch(`/api/products/${id}/stock`, { quantity, reason: "Ajuste manual" })
      await load()
      onChanged?.()
    } catch (e) {
      alert("Error: " + e.message)
    }
  }

  const move = async (id) => {
    const deltaStr = prompt(`Delta (ej. +10 entrada, -5 salida) para ID ${id}:`, "+1")
    if (deltaStr == null) return
    const delta = parseInt(deltaStr, 10)
    if (Number.isNaN(delta)) return alert("Delta inválido")
    try {
      await apiPost(`/api/movements`, { product_id: id, delta, reason: "Movimiento manual" })
      await load()
      onChanged?.()
    } catch (e) {
      alert("Error: " + e.message)
    }
  }

  if (loading) return <div>Cargando inventario...</div>
  if (error) return <div style={{color:"crimson"}}>Error: {error}</div>

  return (
    <div>
      <h3>Inventario</h3>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th style={{textAlign:"left", borderBottom:"1px solid #ccc"}}>ID</th>
            <th style={{textAlign:"left", borderBottom:"1px solid #ccc"}}>SKU</th>
            <th style={{textAlign:"left", borderBottom:"1px solid #ccc"}}>EAN13</th>
            <th style={{textAlign:"left", borderBottom:"1px solid #ccc"}}>Nombre</th>
            <th style={{textAlign:"right", borderBottom:"1px solid #ccc"}}>Stock</th>
            <th style={{textAlign:"right", borderBottom:"1px solid #ccc"}}>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {items.map(it => (
            <tr key={it.id}>
              <td>{it.id}</td>
              <td>{it.sku}</td>
              <td>{it.ean13}</td>
              <td>{it.name}</td>
              <td style={{textAlign:"right"}}>{it.stock_qty}</td>
              <td style={{textAlign:"right"}}>
                <button onClick={() => adjust(it.id, it.stock_qty)} style={{marginRight:8}}>Ajustar</button>
                <button onClick={() => move(it.id)}>Movimiento</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
