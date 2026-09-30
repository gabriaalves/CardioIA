import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext.jsx'
import styles from './Sidebar.module.css'

/**
 * Barra lateral de navegação com links e informações do usuário.
 */
export default function Sidebar() {
  const { usuario, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const links = [
    { to: '/dashboard', icon: '📊', label: 'Dashboard' },
    { to: '/pacientes', icon: '👥', label: 'Pacientes' },
    { to: '/agendamentos', icon: '📅', label: 'Agendamentos' },
  ]

  return (
    <aside className={styles.sidebar}>
      {/* Logo */}
      <div className={styles.logo}>
        <span className={styles.logoIcon}>🫀</span>
        <div>
          <h1 className={styles.logoTitle}>CardioIA</h1>
          <p className={styles.logoSubtitle}>Portal Clínico</p>
        </div>
      </div>

      {/* Navegação */}
      <nav className={styles.nav}>
        {links.map(link => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              `${styles.navLink} ${isActive ? styles.navLinkActive : ''}`
            }
          >
            <span className={styles.navIcon}>{link.icon}</span>
            <span>{link.label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Perfil do usuário */}
      <div className={styles.profile}>
        <div className={styles.profileAvatar}>
          {usuario?.nome?.charAt(0) || 'U'}
        </div>
        <div className={styles.profileInfo}>
          <p className={styles.profileName}>{usuario?.nome}</p>
          <p className={styles.profileRole}>{usuario?.especialidade}</p>
        </div>
        <button
          onClick={handleLogout}
          className={styles.logoutBtn}
          title="Sair"
          id="btn-logout"
        >
          🚪
        </button>
      </div>
    </aside>
  )
}
