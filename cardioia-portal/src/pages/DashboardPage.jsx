import { useState, useEffect } from 'react'
import { apiService } from '../services/api.js'
import { useAuth } from '../contexts/AuthContext.jsx'
import styles from './DashboardPage.module.css'

const DATA_HOJE_FORMATADA = new Date().toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })

/**
 * Página principal do Dashboard com métricas e resumos.
 */
export default function DashboardPage() {
  const [metricas, setMetricas] = useState(null)
  const [carregando, setCarregando] = useState(true)
  const { usuario } = useAuth()

  useEffect(() => {
    async function carregarMetricas() {
      try {
        const dados = await apiService.getMetricas()
        setMetricas(dados)
      } catch (err) {
        console.error('Erro ao carregar métricas:', err)
      } finally {
        setCarregando(false)
      }
    }
    carregarMetricas()
  }, [])

  if (carregando) {
    return <div className={styles.loading}>Carregando dados...</div>
  }

  return (
    <div className={styles.page}>
      {/* Header */}
      <header className={styles.header}>
        <div>
          <h1 className={styles.greeting}>
            Olá, <span className="gradient-text">{usuario?.nome?.split(' ')[0]}</span> 👋
          </h1>
          <p className={styles.subGreeting}>
            Aqui está o resumo do seu portal cardiológico
          </p>
        </div>
        <div className={styles.dateBox}>
          <span className={styles.dateIcon}>📅</span>
          <span>{DATA_HOJE_FORMATADA}</span>
        </div>
      </header>

      {/* Metric Cards */}
      <div className={styles.metricsGrid}>
        <div className={`${styles.metricCard} ${styles.metricPrimary}`} style={{ animationDelay: '0.1s' }}>
          <div className={styles.metricIcon}>👥</div>
          <div className={styles.metricContent}>
            <p className={styles.metricValue}>{metricas.totalPacientes}</p>
            <p className={styles.metricLabel}>Total de Pacientes</p>
          </div>
        </div>

        <div className={`${styles.metricCard} ${styles.metricAccent}`} style={{ animationDelay: '0.2s' }}>
          <div className={styles.metricIcon}>📋</div>
          <div className={styles.metricContent}>
            <p className={styles.metricValue}>{metricas.consultasAgendadas}</p>
            <p className={styles.metricLabel}>Consultas Agendadas</p>
          </div>
        </div>

        <div className={`${styles.metricCard} ${styles.metricDanger}`} style={{ animationDelay: '0.3s' }}>
          <div className={styles.metricIcon}>🔴</div>
          <div className={styles.metricContent}>
            <p className={styles.metricValue}>{metricas.pacientesAltoRisco}</p>
            <p className={styles.metricLabel}>Alto Risco</p>
          </div>
        </div>

        <div className={`${styles.metricCard} ${styles.metricSuccess}`} style={{ animationDelay: '0.4s' }}>
          <div className={styles.metricIcon}>💚</div>
          <div className={styles.metricContent}>
            <p className={styles.metricValue}>{metricas.pacientesBaixoRisco}</p>
            <p className={styles.metricLabel}>Baixo Risco</p>
          </div>
        </div>
      </div>

      {/* Bottom Section */}
      <div className={styles.bottomGrid}>
        {/* Próximas Consultas */}
        <div className={styles.sectionCard}>
          <h2 className={styles.sectionTitle}>📅 Próximas Consultas</h2>
          <div className={styles.consultasList}>
            {metricas.proximasConsultas.map(c => (
              <div key={c.id} className={styles.consultaItem}>
                <div className={styles.consultaInfo}>
                  <p className={styles.consultaNome}>{c.pacienteNome}</p>
                  <p className={styles.consultaTipo}>{c.tipo}</p>
                </div>
                <div className={styles.consultaTime}>
                  <span className={styles.consultaData}>{new Date(c.data + 'T12:00:00').toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' })}</span>
                  <span className={styles.consultaHora}>{c.horario}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Estatísticas */}
        <div className={styles.sectionCard}>
          <h2 className={styles.sectionTitle}>📊 Estatísticas Clínicas</h2>
          <div className={styles.statsList}>
            <div className={styles.statItem}>
              <span className={styles.statLabel}>Média de Idade</span>
              <span className={styles.statValue}>{metricas.mediaIdade} anos</span>
            </div>
            <div className={styles.statItem}>
              <span className={styles.statLabel}>IMC Médio</span>
              <span className={styles.statValue}>{metricas.mediaIMC}</span>
            </div>
            <div className={styles.statItem}>
              <span className={styles.statLabel}>Pacientes Masculinos</span>
              <span className={styles.statValue}>{metricas.distribuicaoSexo.masculino}</span>
            </div>
            <div className={styles.statItem}>
              <span className={styles.statLabel}>Pacientes Femininos</span>
              <span className={styles.statValue}>{metricas.distribuicaoSexo.feminino}</span>
            </div>
            <div className={styles.statItem}>
              <span className={styles.statLabel}>Risco Moderado</span>
              <span className={styles.statValue}>{metricas.pacientesRiscoModerado}</span>
            </div>
          </div>

          {/* Mini barra de risco */}
          <div className={styles.riskBar}>
            <div className={styles.riskSegment} style={{
              width: `${(metricas.pacientesBaixoRisco / metricas.totalPacientes) * 100}%`,
              background: 'var(--color-success)'
            }} />
            <div className={styles.riskSegment} style={{
              width: `${(metricas.pacientesRiscoModerado / metricas.totalPacientes) * 100}%`,
              background: 'var(--color-warning)'
            }} />
            <div className={styles.riskSegment} style={{
              width: `${(metricas.pacientesAltoRisco / metricas.totalPacientes) * 100}%`,
              background: 'var(--color-danger)'
            }} />
          </div>
          <div className={styles.riskLegend}>
            <span><span style={{ color: 'var(--color-success)' }}>●</span> Baixo</span>
            <span><span style={{ color: 'var(--color-warning)' }}>●</span> Moderado</span>
            <span><span style={{ color: 'var(--color-danger)' }}>●</span> Alto</span>
          </div>
        </div>
      </div>
    </div>
  )
}
