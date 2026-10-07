import { useState, useEffect, useReducer } from 'react'
import { apiService } from '../services/api.js'
import styles from './AgendamentosPage.module.css'

/**
 * Estado inicial do formulário de agendamento.
 */
const formularioInicial = {
  pacienteId: '',
  pacienteNome: '',
  data: '',
  horario: '',
  tipo: 'Consulta Inicial'
}

const DATA_MINIMA_HOJE = new Date().toISOString().split('T')[0]

/**
 * Reducer para gerenciar o estado do formulário com useReducer.
 */
function formularioReducer(state, action) {
  switch (action.type) {
    case 'ATUALIZAR_CAMPO':
      return { ...state, [action.campo]: action.valor }
    case 'RESETAR':
      return formularioInicial
    case 'SELECIONAR_PACIENTE':
      return { ...state, pacienteId: action.id, pacienteNome: action.nome }
    default:
      return state
  }
}

/**
 * Página de agendamento de consultas.
 * Usa useReducer para o formulário e useState para estado da página.
 */
export default function AgendamentosPage() {
  const [consultas, setConsultas] = useState([])
  const [pacientes, setPacientes] = useState([])
  const [carregando, setCarregando] = useState(true)
  const [salvando, setSalvando] = useState(false)
  const [mensagem, setMensagem] = useState(null)
  const [mostrarForm, setMostrarForm] = useState(false)

  const [formulario, dispatch] = useReducer(formularioReducer, formularioInicial)

  useEffect(() => {
    async function carregarDados() {
      try {
        const [consultasDados, pacientesDados] = await Promise.all([
          apiService.getConsultas(),
          apiService.getPacientes()
        ])
        setConsultas(consultasDados)
        setPacientes(pacientesDados)
      } catch (err) {
        console.error('Erro ao carregar dados:', err)
      } finally {
        setCarregando(false)
      }
    }
    carregarDados()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSalvando(true)
    setMensagem(null)

    try {
      const novaConsulta = await apiService.agendarConsulta(formulario)
      setConsultas(prev => [...prev, novaConsulta])
      dispatch({ type: 'RESETAR' })
      setMostrarForm(false)
      setMensagem({ tipo: 'sucesso', texto: `✅ Consulta agendada com sucesso! (${novaConsulta.id})` })

      // Limpar mensagem após 4 segundos
      setTimeout(() => setMensagem(null), 4000)
    } catch (err) {
      console.error('Erro ao agendar consulta:', err)
      setMensagem({ tipo: 'erro', texto: '❌ Erro ao agendar consulta. Tente novamente.' })
    } finally {
      setSalvando(false)
    }
  }

  const handleCancelar = async (id) => {
    try {
      const atualizadas = await apiService.cancelarConsulta(id)
      setConsultas(atualizadas)
      setMensagem({ tipo: 'sucesso', texto: `Consulta ${id} cancelada.` })
      setTimeout(() => setMensagem(null), 3000)
    } catch (err) {
      console.error('Erro ao cancelar:', err)
    }
  }

  const tiposConsulta = [
    'Consulta Inicial', 'Retorno', 'Eletrocardiograma',
    'Ecocardiograma', 'Teste Ergométrico', 'Holter 24h'
  ]

  const consultasAtivas = consultas.filter(c => c.status === 'agendada')
  const consultasCanceladas = consultas.filter(c => c.status === 'cancelada')

  if (carregando) {
    return <div className={styles.loading}>Carregando agendamentos...</div>
  }

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <div>
          <h1 className={styles.title}>📅 Agendamentos</h1>
          <p className={styles.subtitle}>
            {consultasAtivas.length} consulta(s) agendada(s)
          </p>
        </div>
        <button
          onClick={() => setMostrarForm(!mostrarForm)}
          className={styles.addBtn}
          id="btn-novo-agendamento"
        >
          {mostrarForm ? '✕ Fechar' : '+ Nova Consulta'}
        </button>
      </header>

      {/* Mensagem de feedback */}
      {mensagem && (
        <div className={`${styles.mensagem} ${mensagem.tipo === 'sucesso' ? styles.mensagemSucesso : styles.mensagemErro}`}>
          {mensagem.texto}
        </div>
      )}

      {/* Formulário de agendamento */}
      {mostrarForm && (
        <div className={styles.formCard}>
          <h2 className={styles.formTitle}>📝 Novo Agendamento</h2>
          <form onSubmit={handleSubmit} className={styles.form}>
            <div className={styles.formGrid}>
              <div className={styles.inputGroup}>
                <label htmlFor="paciente" className={styles.label}>Paciente</label>
                <select
                  id="paciente"
                  value={formulario.pacienteId}
                  onChange={(e) => {
                    const pac = pacientes.find(p => p.id === e.target.value)
                    dispatch({
                      type: 'SELECIONAR_PACIENTE',
                      id: e.target.value,
                      nome: pac ? pac.nome : ''
                    })
                  }}
                  className={styles.select}
                  required
                >
                  <option value="">Selecione um paciente...</option>
                  {pacientes.map(p => (
                    <option key={p.id} value={p.id}>{p.nome} ({p.id})</option>
                  ))}
                </select>
              </div>

              <div className={styles.inputGroup}>
                <label htmlFor="tipo" className={styles.label}>Tipo de Consulta</label>
                <select
                  id="tipo"
                  value={formulario.tipo}
                  onChange={(e) => dispatch({ type: 'ATUALIZAR_CAMPO', campo: 'tipo', valor: e.target.value })}
                  className={styles.select}
                  required
                >
                  {tiposConsulta.map(tipo => (
                    <option key={tipo} value={tipo}>{tipo}</option>
                  ))}
                </select>
              </div>

              <div className={styles.inputGroup}>
                <label htmlFor="data" className={styles.label}>Data</label>
                <input
                  id="data"
                  type="date"
                  value={formulario.data}
                  onChange={(e) => dispatch({ type: 'ATUALIZAR_CAMPO', campo: 'data', valor: e.target.value })}
                  className={styles.input}
                  required
                  min={DATA_MINIMA_HOJE}
                />
              </div>

              <div className={styles.inputGroup}>
                <label htmlFor="horario" className={styles.label}>Horário</label>
                <input
                  id="horario"
                  type="time"
                  value={formulario.horario}
                  onChange={(e) => dispatch({ type: 'ATUALIZAR_CAMPO', campo: 'horario', valor: e.target.value })}
                  className={styles.input}
                  required
                />
              </div>
            </div>

            <div className={styles.formActions}>
              <button
                type="button"
                onClick={() => { dispatch({ type: 'RESETAR' }); setMostrarForm(false) }}
                className={styles.cancelBtn}
              >
                Cancelar
              </button>
              <button
                type="submit"
                className={styles.submitBtn}
                disabled={salvando}
                id="btn-salvar-agendamento"
              >
                {salvando ? 'Agendando...' : '✓ Agendar Consulta'}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Lista de consultas agendadas */}
      <div className={styles.section}>
        <h2 className={styles.sectionTitle}>📋 Consultas Agendadas</h2>
        {consultasAtivas.length === 0 ? (
          <p className={styles.emptyMsg}>Nenhuma consulta agendada no momento.</p>
        ) : (
          <div className={styles.consultasGrid}>
            {consultasAtivas.map((c, i) => (
              <div key={c.id} className={styles.consultaCard} style={{ animationDelay: `${i * 0.08}s` }}>
                <div className={styles.consultaHeader}>
                  <span className={styles.consultaId}>{c.id}</span>
                  <span className={styles.statusBadge}>Agendada</span>
                </div>
                <p className={styles.consultaPaciente}>{c.pacienteNome}</p>
                <p className={styles.consultaTipo}>{c.tipo}</p>
                <div className={styles.consultaDateTime}>
                  <span>📅 {new Date(c.data + 'T12:00:00').toLocaleDateString('pt-BR')}</span>
                  <span>🕐 {c.horario}</span>
                </div>
                <button
                  onClick={() => handleCancelar(c.id)}
                  className={styles.cancelConsultaBtn}
                >
                  Cancelar
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Consultas canceladas */}
      {consultasCanceladas.length > 0 && (
        <div className={styles.section}>
          <h2 className={styles.sectionTitle}>🚫 Canceladas ({consultasCanceladas.length})</h2>
          <div className={styles.consultasGrid}>
            {consultasCanceladas.map(c => (
              <div key={c.id} className={`${styles.consultaCard} ${styles.cardCancelada}`}>
                <div className={styles.consultaHeader}>
                  <span className={styles.consultaId}>{c.id}</span>
                  <span className={styles.statusCancelada}>Cancelada</span>
                </div>
                <p className={styles.consultaPaciente}>{c.pacienteNome}</p>
                <p className={styles.consultaTipo}>{c.tipo}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
