# 🫀 CardioIA Portal — Interface Web

Portal responsivo em **React 19 + Vite** que simula a rotina de um sistema de diagnóstico cardiológico.

## ✨ Funcionalidades

- **Autenticação simulada** via Context API com JWT fake no localStorage
- **Dashboard** com métricas de pacientes, consultas e distribuição de risco
- **Listagem de pacientes** com busca e filtros por nível de risco
- **Agendamento de consultas** com formulário usando `useReducer`
- **Proteção de rotas** — dados visíveis apenas para usuários logados
- **Design responsivo** com CSS Modules e tema dark premium

## 🚀 Instalação e Execução

```bash
# Instalar dependências
npm install

# Iniciar em modo desenvolvimento
npm run dev

# Build para produção
npm run build
```

Acesse: **http://localhost:5173**

## 🔑 Credenciais de Acesso

| Email | Senha |
|-------|-------|
| `ricardo@cardioia.com` | `123456` |
| `maria@cardioia.com` | `123456` |

## 📁 Estrutura

```
src/
├── contexts/AuthContext.jsx      # Autenticação com JWT fake
├── components/
│   ├── ProtectedRoute.jsx        # Proteção de rotas
│   └── Sidebar.jsx               # Navegação lateral
├── services/api.js               # API simulada (dados locais)
├── pages/
│   ├── LoginPage.jsx             # Tela de login
│   ├── DashboardPage.jsx         # Dashboard com métricas
│   ├── PacientesPage.jsx         # Lista de pacientes
│   └── AgendamentosPage.jsx      # Agendamento de consultas
├── App.jsx                       # Roteamento
├── main.jsx                      # Entry point
└── index.css                     # Design system global
```

## 🛠️ Tecnologias

- React 19 + Vite 8
- React Router v7
- CSS Modules
- Context API + useReducer
