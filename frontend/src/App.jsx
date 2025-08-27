// Componente principal de la aplicación React que muestra el inventario, movimientos y autenticación.

import React, { useState, useEffect } from "react"
import InventoryTable from "./components/InventoryTable.jsx"
import Movements from "./components/Movements.jsx"
import Login from "./components/Login.jsx"

export default function App() {
  const [refreshKey, setRefreshKey] = useState(0)
  const onChanged = () => setRefreshKey(k => k + 1)

  useEffect(() => {}, [refreshKey])

  return (
    <div style={{maxWidth: 1000, margin: "24px auto", padding: "0 16px", fontFamily:"Inter, system-ui, Arial"}}>
      <h1 style={{fontSize: 28, marginBottom: 4}}>Inventario</h1>
      <p style={{color:"#555", marginTop:0}}>FastAPI + React + PostgreSQL</p>
      <Login onLoggedIn={() => setRefreshKey(k => k + 1)} />
      <InventoryTable onChanged={onChanged} />
      <Movements key={refreshKey} />
    </div>
  )
}
