import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext.jsx'
import styles from './LoginPage.module.css'

/**
 * Página de login com autenticação simulada.
 */
export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [erro, setErro] = useState('')
  const [carregando, setCarregando] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setErro('')
    setCarregando(true)

    try {
      await login(email, senha)
      navigate('/dashboard')
    } catch (err) {
      setErro(err.message)
    } finally {
      setCarregando(false)
    }
  }

  return (
    <div className={styles.container}>
      {/* Partículas de fundo */}
      <div className={styles.bgParticles}>
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className={styles.particle} style={{
            '--delay': `${i * 0.8}s`,
            '--x': `${15 + i * 15}%`,
            '--size': `${60 + i * 40}px`
          }} />
        ))}
      </div>

      <div className={styles.card}>
        {/* Header */}
        <div className={styles.header}>
          <div className={styles.logoCircle}>
            <span className={styles.heartIcon}>🫀</span>
          </div>
          <h1 className={styles.title}>CardioIA</h1>
          <p className={styles.subtitle}>Portal de Diagnóstico Cardiológico</p>
        </div>

        {/* Formulário */}
        <form onSubmit={handleSubmit} className={styles.form}>
          {erro && (
            <div className={styles.errorBox}>
              <span>⚠️</span> {erro}
            </div>
          )}

          <div className={styles.inputGroup}>
            <label htmlFor="email" className={styles.label}>E-mail</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="seu@email.com"
              className={styles.input}
              required
              autoFocus
            />
          </div>

          <div className={styles.inputGroup}>
            <label htmlFor="senha" className={styles.label}>Senha</label>
            <input
              id="senha"
              type="password"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              placeholder="••••••••"
              className={styles.input}
              required
            />
          </div>

          <button
            type="submit"
            className={styles.submitBtn}
            disabled={carregando}
            id="btn-login"
          >
            {carregando ? (
              <span className={styles.spinner} />
            ) : (
              'Entrar'
            )}
          </button>
        </form>

        {/* Credenciais de demo */}
        <div className={styles.demo}>
          <p className={styles.demoTitle}>🔑 Acesso de demonstração:</p>
          <p className={styles.demoCredential}>
            <strong>Email:</strong> ricardo@cardioia.com
          </p>
          <p className={styles.demoCredential}>
            <strong>Senha:</strong> 123456
          </p>
        </div>
      </div>
    </div>
  )
}
