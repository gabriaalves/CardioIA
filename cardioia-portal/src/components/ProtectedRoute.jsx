import { Navigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext.jsx'

/**
 * Componente que protege rotas autenticadas.
 * Redireciona para /login se o usuário não estiver logado.
 */
export default function ProtectedRoute({ children }) {
  const { estaAutenticado, carregando } = useAuth()

  if (carregando) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        color: 'var(--text-secondary)'
      }}>
        <div className="loading-spinner" />
      </div>
    )
  }

  if (!estaAutenticado) {
    return <Navigate to="/login" replace />
  }

  return children
}
