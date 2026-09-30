import { useState, useEffect } from 'react'
import { apiService } from '../services/api.js'
import styles from './PacientesPage.module.css'

/**
 * Página de listagem de pacientes com busca e filtro por risco.
 */
export default function PacientesPage() {
  const [pacientes, setPacientes] = useState([])
  const [carregando, setCarregando] = useState(true)
  const [busca, setBusca] = useState('')
  const [filtroRisco, setFiltroRisco] = useState('todos')

  useEffect(() => {
    async function carregarPacientes() {
      try {
        const dados = await apiService.getPacientes()
        setPacientes(dados)
      } catch (err) {
        console.error('Erro ao carregar pacientes:', err)
      } finally {
        setCarregando(false)
      }
    }
    carregarPacientes()
  }, [])

  // Filtragem
  const pacientesFiltrados = pacientes.filter(p => {
    const matchBusca = p.nome.toLowerCase().includes(busca.toLowerCase()) ||
                       p.id.toLowerCase().includes(busca.toLowerCase()) ||
                       p.diagnostico.toLowerCase().includes(busca.toLowerCase())
    const matchRisco = filtroRisco === 'todos' || p.risco === filtroRisco
    return matchBusca && matchRisco
  })

  const riscoCor = {
    alto: styles.riscoAlto,
    moderado: styles.riscoModerado,
    baixo: styles.riscoBaixo
  }

  const riscoLabel = {
    alto: '🔴 Alto',
    moderado: '🟡 Moderado',
    baixo: '🟢 Baixo'
  }

  if (carregando) {
    return <div className={styles.loading}>Carregando pacientes...</div>
  }

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>👥 Pacientes</h1>
        <p className={styles.subtitle}>{pacientes.length} pacientes cadastrados</p>
      </header>

      {/* Filtros */}
      <div className={styles.filters}>
        <input
          type="text"
          placeholder="🔍 Buscar por nome, ID ou diagnóstico..."
          value={busca}
          onChange={(e) => setBusca(e.target.value)}
          className={styles.searchInput}
          id="input-busca-paciente"
        />
        <div className={styles.filterBtns}>
          {['todos', 'alto', 'moderado', 'baixo'].map(filtro => (
            <button
              key={filtro}
              onClick={() => setFiltroRisco(filtro)}
              className={`${styles.filterBtn} ${filtroRisco === filtro ? styles.filterBtnActive : ''}`}
            >
              {filtro === 'todos' ? '📋 Todos' : riscoLabel[filtro]}
            </button>
          ))}
        </div>
      </div>

      {/* Tabela de Pacientes */}
      <div className={styles.tableWrapper}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome</th>
              <th>Idade</th>
              <th>Sexo</th>
              <th>Diagnóstico</th>
              <th>PA</th>
              <th>IMC</th>
              <th>Risco</th>
            </tr>
          </thead>
          <tbody>
            {pacientesFiltrados.map((p, i) => (
              <tr key={p.id} className={styles.tableRow} style={{ animationDelay: `${i * 0.05}s` }}>
                <td className={styles.cellId}>{p.id}</td>
                <td>
                  <div className={styles.cellNome}>
                    <div className={styles.avatar}>{p.nome.charAt(0)}</div>
                    <div>
                      <p className={styles.nome}>{p.nome}</p>
                      <p className={styles.telefone}>{p.telefone}</p>
                    </div>
                  </div>
                </td>
                <td>{p.idade} anos</td>
                <td>{p.sexo === 'M' ? '♂️' : '♀️'} {p.sexo}</td>
                <td className={styles.diagnostico}>{p.diagnostico}</td>
                <td className={styles.mono}>{p.pressao}</td>
                <td className={styles.mono}>{p.imc}</td>
                <td>
                  <span className={`${styles.riscoBadge} ${riscoCor[p.risco]}`}>
                    {riscoLabel[p.risco]}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {pacientesFiltrados.length === 0 && (
          <div className={styles.emptyState}>
            <p>Nenhum paciente encontrado com os filtros aplicados.</p>
          </div>
        )}
      </div>
    </div>
  )
}
