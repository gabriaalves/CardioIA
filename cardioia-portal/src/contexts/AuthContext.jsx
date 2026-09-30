import { createContext, useContext, useState, useEffect } from 'react'

const AuthContext = createContext(null)

/**
 * Gera um JWT fake simulado para localStorage.
 */
function gerarJWTFake(usuario) {
  const header = btoa(JSON.stringify({ alg: 'HS256', typ: 'JWT' }))
  const payload = btoa(JSON.stringify({
    sub: usuario.id,
    nome: usuario.nome,
    email: usuario.email,
    role: usuario.role,
    iat: Date.now(),
    exp: Date.now() + 3600000 // 1 hora
  }))
  const signature = btoa('cardioia-secret-key')
  return `${header}.${payload}.${signature}`
}

/**
 * Usuários simulados para autenticação.
 */
const USUARIOS_MOCK = [
  {
    id: '1',
    nome: 'Dr. Ricardo Mendes',
    email: 'ricardo@cardioia.com',
    senha: '123456',
    role: 'medico',
    especialidade: 'Cardiologia',
    crm: 'CRM-SP 123456'
  },
  {
    id: '2',
    nome: 'Enf. Maria Santos',
    email: 'maria@cardioia.com',
    senha: '123456',
    role: 'enfermeiro',
    especialidade: 'Enfermagem Cardíaca',
    crm: 'COREN-SP 789012'
  }
]

export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(null)
  const [carregando, setCarregando] = useState(true)

  // Verificar token no localStorage ao carregar
  useEffect(() => {
    const token = localStorage.getItem('cardioia_token')
    const dadosUsuario = localStorage.getItem('cardioia_usuario')

    if (token && dadosUsuario) {
      try {
        const parts = token.split('.')
        const payload = JSON.parse(atob(parts[1]))

        // Verificar se o token não expirou
        if (payload.exp > Date.now()) {
          setUsuario(JSON.parse(dadosUsuario))
        } else {
          // Token expirado
          localStorage.removeItem('cardioia_token')
          localStorage.removeItem('cardioia_usuario')
        }
      } catch {
        localStorage.removeItem('cardioia_token')
        localStorage.removeItem('cardioia_usuario')
      }
    }
    setCarregando(false)
  }, [])

  /**
   * Realiza login simulado verificando credenciais contra USUARIOS_MOCK.
   */
  const login = async (email, senha) => {
    // Simular delay de requisição HTTP
    await new Promise(resolve => setTimeout(resolve, 800))

    const usuarioEncontrado = USUARIOS_MOCK.find(
      u => u.email === email && u.senha === senha
    )

    if (!usuarioEncontrado) {
      throw new Error('Credenciais inválidas. Verifique email e senha.')
    }

    const { senha: _, ...dadosSeguros } = usuarioEncontrado
    const token = gerarJWTFake(dadosSeguros)

    localStorage.setItem('cardioia_token', token)
    localStorage.setItem('cardioia_usuario', JSON.stringify(dadosSeguros))
    setUsuario(dadosSeguros)

    return dadosSeguros
  }

  /**
   * Realiza logout removendo dados do localStorage.
   */
  const logout = () => {
    localStorage.removeItem('cardioia_token')
    localStorage.removeItem('cardioia_usuario')
    setUsuario(null)
  }

  const estaAutenticado = !!usuario

  return (
    <AuthContext.Provider value={{
      usuario,
      carregando,
      estaAutenticado,
      login,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider')
  }
  return context
}

export default AuthContext
