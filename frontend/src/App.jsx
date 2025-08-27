/**
 * Componente principal de la aplicación React.
 * Muestra el inventario, el historial de movimientos y la autenticación.
 * Se encarga de refrescar los datos al iniciar sesión o al realizar cambios en el inventario.
 */

import React, { useState, useEffect } from "react"
import InventoryTable from "./components/InventoryTable.jsx"
import Movements from "./components/Movements.jsx"
import Login from "./components/Login.jsx"

export default function App() {
  const [refreshKey, setRefreshKey] = useState(0)  // Clave usada para forzar recarga de Movements

  // Función que incrementa refreshKey para notificar cambios
  const onChanged = () => setRefreshKey(k => k + 1)

  // Hook de efecto dependiente de refreshKey (reservado para lógica futura si se requiere)
  useEffect(() => {}, [refreshKey])

  return (
    <div style={{maxWidth: 1000, margin: "24px auto", padding: "0 16px", fontFamily:"Inter, system-ui, Arial"}}>
      <h1 style={{fontSize: 28, marginBottom: 4}}>Inventario</h1>
      <p style={{color:"#555", marginTop:0}}>FastAPI + React + PostgreSQL</p>

      {/* Componente de login: refresca los datos al iniciar sesión */}
      <Login onLoggedIn={() => setRefreshKey(k => k + 1)} />

      {/* Tabla del inventario: llama a onChanged al modificar stock */}
      <InventoryTable onChanged={onChanged} />

      {/* Historial de movimientos: se vuelve a renderizar con refreshKey */}
      <Movements key={refreshKey} />
    </div>
  )
}
