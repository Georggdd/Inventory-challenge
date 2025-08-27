// Funciones para interactuar con la API: GET, POST, PATCH y autenticación de usuarios.

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

function authHeaders() {
  const token = localStorage.getItem("token")
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export async function apiGet(path) {
  const res = await fetch(`${API_URL}${path}`, { headers: { ...authHeaders() } })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function apiPost(path, body) {
  const res = await fetch(`${API_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function apiPatch(path, body) {
  const res = await fetch(`${API_URL}${path}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json", ...authHeaders() },
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function login(email, password) {
  const form = new URLSearchParams()
  form.set("username", email)
  form.set("password", password)
  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: form.toString(),
  })
  if (!res.ok) throw new Error(await res.text())
  const data = await res.json()
  localStorage.setItem("token", data.access_token)
  return data
}

export async function register(email, password) {
  return apiPost("/auth/register", { email, password })
}
