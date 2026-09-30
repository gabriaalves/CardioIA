import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './contexts/AuthContext.jsx'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import Sidebar from './components/Sidebar.jsx'
import LoginPage from './pages/LoginPage.jsx'
import DashboardPage from './pages/DashboardPage.jsx'
import PacientesPage from './pages/PacientesPage.jsx'
import AgendamentosPage from './pages/AgendamentosPage.jsx'
import './App.css'

/**
 * Componente Layout para páginas autenticadas com Sidebar.
 */
function Layout({ children }) {
  return (
    <div className="app-layout">
      <Sidebar />
      <main className="app-main">
        {children}
      </main>
    </div>
  )
}

/**
 * Componente principal da aplicação CardioIA Portal.
 */
export default function App() {
  const { estaAutenticado } = useAuth()

  return (
    <Routes>
      {/* Rota pública: Login */}
      <Route
        path="/login"
        element={
          estaAutenticado ? <Navigate to="/dashboard" replace /> : <LoginPage />
        }
      />

      {/* Rotas protegidas */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Layout><DashboardPage /></Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/pacientes"
        element={
          <ProtectedRoute>
            <Layout><PacientesPage /></Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/agendamentos"
        element={
          <ProtectedRoute>
            <Layout><AgendamentosPage /></Layout>
          </ProtectedRoute>
        }
      />

      {/* Redirect padrão */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}
