import { useState } from 'react'
import Header from './components/Header'
import Dashboard from './components/Dashboard'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-100 flex flex-col items-center p-4">
      <Header />
      <Dashboard />
    </div>
  )
}

export default App
