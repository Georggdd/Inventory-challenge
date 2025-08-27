// Componente React para autenticación de usuario: login, registro y logout.

import React, { useState } from "react"
import { login, register } from "../api"

export default function Login({ onLoggedIn }) {
  const [email, setEmail] = useState("admin@example.com") // Email del usuario
  const [password, setPassword] = useState("admin123") // Password del usuario
  const [msg, setMsg] = useState("") // Mensajes de estado

  // Manejar login de usuario
  const doLogin = async (e) => {
    e.preventDefault()
    try {
      await login(email, password) // Llamada API para login
      setMsg("¡Login correcto!")
      onLoggedIn?.() // Avisar al padre de que se ha logueado
    } catch (e) {
      setMsg("Error de login: " + e.message)
    }
  }

  // Manejar registro de nuevo usuario
  const doRegister = async (e) => {
    e.preventDefault()
    try {
      await register(email, password) // Llamada API para registro
      setMsg("Registrado. Ahora puedes iniciar sesión.")
    } catch (e) {
      setMsg("Error de registro: " + e.message)
    }
  }

  return (
    <div style={{border: "1px solid #eee", padding: 16, borderRadius: 12, marginBottom: 16}}>
      <h3>Autenticación (opcional)</h3>
      <form onSubmit={doLogin} style={{display: "flex", gap: 8, flexWrap: "wrap"}}>
        <input 
          placeholder="email" 
          value={email} 
          onChange={e => setEmail(e.target.value)} 
        />
        <input 
          placeholder="password" 
          type="password" 
          value={password} 
          onChange={e => setPassword(e.target.value)} 
        />
        <button type="submit">Login</button>
        <button onClick={doRegister}>Registrar</button>
        <button 
          type="button" 
          onClick={() => { 
            localStorage.removeItem("token") // Eliminar token del localStorage
            setMsg("Sesión cerrada") 
          }}
        >
          Logout
        </button>
      </form>
      {msg && <div style={{marginTop:8, fontSize: 12}}>{msg}</div>}
    </div>
  )
}
