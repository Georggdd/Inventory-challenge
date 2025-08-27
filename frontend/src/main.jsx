// Punto de entrada de la aplicación React que renderiza el componente principal App.

import React from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'

// Crear el root y renderizar el componente principal
createRoot(document.getElementById('root')).render(<App />)
