# 🫀 CardioIA Portal — Interface Web (Ir Além 1)
### Portal Responsivo de Diagnóstico em Cardiologia | React 19 + Vite

Projeto desenvolvido para a disciplina de **Inteligência Artificial — FIAP 2025** (Metodologia PBL).

---

## 👥 Equipe de Desenvolvimento

| Nome Completo | RM | Função / Contribuição |
|---------------|:--:|-----------------------|
| **Gabriela de Andrade Alves** | RM567740 | Front-End, Context API, Roteamento e Estilização |
| **Leonardo de Mattos Oliveira** | RM568219 | Serviços de API Fake, Gestão de Estado e Componentização |

---

## 🎬 Vídeo de Demonstração

> 📹 **Vídeo de Demonstração no YouTube (Não Listado):**  
> `[INSERIR O LINK DO VÍDEO DO PORTAL NO YOUTUBE AQUI]`  
> *(Vídeo de até 4 minutos apresentando login, dashboard, pacientes, agendamentos com useReducer e rotas protegidas)*

---

## ✨ Funcionalidades e Requisitos Atendidos

| Requisito do Enunciado | Implementação | Arquivos Principais |
|------------------------|---------------|----------------------|
| **Autenticação Simulada** | Context API com token JWT fake armazenado no `localStorage` e expiração de sessão | [`src/contexts/AuthContext.jsx`](src/contexts/AuthContext.jsx) |
| **Proteção de Rotas** | Redirecionamento automático de usuários não autenticados para `/login` | [`src/components/ProtectedRoute.jsx`](src/components/ProtectedRoute.jsx) |
| **Listagem de Pacientes** | Consumo assíncrono de API simulada, busca em tempo real e filtros dinâmicos por risco | [`src/pages/PacientesPage.jsx`](src/pages/PacientesPage.jsx), [`src/services/api.js`](src/services/api.js) |
| **Agendamento de Consultas** | Formulário com fluxo gerenciado via `useReducer` e `useState` | [`src/pages/AgendamentosPage.jsx`](src/pages/AgendamentosPage.jsx) |
| **Dashboard Clínico** | Painel com métricas de pacientes, consultas marcadas e distribuição de risco | [`src/pages/DashboardPage.jsx`](src/pages/DashboardPage.jsx) |
| **Estilização e Responsividade** | CSS Modules com tema escuro moderno (*glassmorphism*, gradientes e micro-animações) | `*.module.css`, [`src/index.css`](src/index.css) |

---

## 🔑 Credenciais para Acesso

| Perfil Clínico | E-mail | Senha | Função |
|----------------|--------|:-----:|--------|
| **Médico Cardiologista** | `ricardo@cardioia.com` | `123456` | Dr. Ricardo Mendes (CRM-SP 123456) |
| **Enfermagem Cardíaca** | `maria@cardioia.com` | `123456` | Enf. Maria Santos (COREN-SP 789012) |

---

## 🚀 Instalação e Execução

### Pré-requisitos
- **Node.js** v18+ instalado
- **npm** v9+ instalado

### Comandos

```bash
# 1. Navegue até o diretório do portal (se estiver na raiz do CardioIA)
cd cardioia-portal

# 2. Instale as dependências
npm install

# 3. Inicie o servidor de desenvolvimento
npm run dev
```

Acesse a aplicação no navegador em: **`http://localhost:5173`**

### Build de Produção e Validação

```bash
# Gerar build de produção
npm run build

# Pré-visualizar build localmente
npm run preview
```

---

## 📁 Estrutura de Pastas Padronizada

```
cardioia-portal/
├── src/
│   ├── contexts/
│   │   └── AuthContext.jsx       # Context API de Autenticação + JWT Fake
│   ├── components/
│   │   ├── ProtectedRoute.jsx    # Componente guardião de rotas privadas
│   │   ├── Sidebar.jsx           # Navegação lateral responsiva
│   │   └── Sidebar.module.css
│   ├── services/
│   │   └── api.js                # Serviço de API simulada (pacientes, métricas, agenda)
│   ├── pages/
│   │   ├── LoginPage.jsx         # Tela de autenticação clínica
│   │   ├── DashboardPage.jsx     # Painel gerencial e métricas
│   │   ├── PacientesPage.jsx     # Gestão e busca de prontuários
│   │   └── AgendamentosPage.jsx  # Agendamento gerenciado via useReducer
│   ├── App.jsx                   # Roteamento SPA (React Router v7)
│   ├── main.jsx                  # Ponto de entrada
│   └── index.css                 # Design system global e tokens visuais
├── package.json
└── vite.config.js
```

---

## 🛠️ Tecnologias Utilizadas

- **React 19**
- **Vite 8**
- **React Router v7**
- **CSS Modules**
- **Hooks:** `useState`, `useEffect`, `useContext`, `useReducer`, `useMemo`
