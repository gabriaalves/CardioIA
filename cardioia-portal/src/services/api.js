/**
 * CardioIA Portal — Serviço de API (Dados Simulados)
 *
 * Simula chamadas a APIs para pacientes, consultas e métricas.
 * Usa dados locais em vez de requisições HTTP reais.
 */

// ─── Dados simulados de pacientes ───────────────────────────────────────────
const PACIENTES = [
  { id: 'P001', nome: 'Ana Clara Oliveira', idade: 67, sexo: 'F', telefone: '(11) 98765-4321', risco: 'alto', diagnostico: 'Insuficiência Cardíaca', pressao: '148/95', imc: 31.2, ultimaConsulta: '2026-09-15' },
  { id: 'P002', nome: 'Carlos Eduardo Silva', idade: 54, sexo: 'M', telefone: '(11) 91234-5678', risco: 'moderado', diagnostico: 'Hipertensão Arterial', pressao: '135/88', imc: 28.5, ultimaConsulta: '2026-09-20' },
  { id: 'P003', nome: 'Maria José Santos', idade: 72, sexo: 'F', telefone: '(21) 97654-3210', risco: 'alto', diagnostico: 'Arritmia Cardíaca', pressao: '155/100', imc: 26.8, ultimaConsulta: '2026-09-10' },
  { id: 'P004', nome: 'Roberto Ferreira Lima', idade: 45, sexo: 'M', telefone: '(11) 99876-5432', risco: 'baixo', diagnostico: 'Check-up Preventivo', pressao: '120/80', imc: 24.1, ultimaConsulta: '2026-09-25' },
  { id: 'P005', nome: 'Francisca Souza Almeida', idade: 61, sexo: 'F', telefone: '(31) 98765-1234', risco: 'alto', diagnostico: 'Angina de Peito', pressao: '142/92', imc: 33.7, ultimaConsulta: '2026-09-05' },
  { id: 'P006', nome: 'José Antônio Pereira', idade: 58, sexo: 'M', telefone: '(21) 93456-7890', risco: 'moderado', diagnostico: 'Dislipidemia', pressao: '130/85', imc: 29.4, ultimaConsulta: '2026-09-22' },
  { id: 'P007', nome: 'Lúcia Helena Costa', idade: 79, sexo: 'F', telefone: '(11) 92345-6789', risco: 'alto', diagnostico: 'Fibrilação Atrial', pressao: '160/98', imc: 27.3, ultimaConsulta: '2026-09-01' },
  { id: 'P008', nome: 'Fernando Augusto Ramos', idade: 42, sexo: 'M', telefone: '(41) 98123-4567', risco: 'baixo', diagnostico: 'Check-up Preventivo', pressao: '118/76', imc: 23.5, ultimaConsulta: '2026-09-28' },
  { id: 'P009', nome: 'Tereza Cristina Barbosa', idade: 65, sexo: 'F', telefone: '(11) 94567-8901', risco: 'moderado', diagnostico: 'Doença Arterial Coronariana', pressao: '138/90', imc: 30.1, ultimaConsulta: '2026-09-18' },
  { id: 'P010', nome: 'Paulo Ricardo Mendes', idade: 51, sexo: 'M', telefone: '(21) 96789-0123', risco: 'baixo', diagnostico: 'Sopro Cardíaco Inocente', pressao: '122/78', imc: 25.9, ultimaConsulta: '2026-09-26' },
  { id: 'P011', nome: 'Sandra Maria Vieira', idade: 70, sexo: 'F', telefone: '(11) 95678-9012', risco: 'alto', diagnostico: 'Estenose Aórtica', pressao: '150/96', imc: 28.0, ultimaConsulta: '2026-09-08' },
  { id: 'P012', nome: 'Marcos Antônio Dias', idade: 48, sexo: 'M', telefone: '(31) 97890-1234', risco: 'moderado', diagnostico: 'Hipertensão Arterial', pressao: '140/88', imc: 32.0, ultimaConsulta: '2026-09-17' },
]

// ─── Consultas agendadas ────────────────────────────────────────────────────
let CONSULTAS_STORAGE_KEY = 'cardioia_consultas'

function getConsultas() {
  const dados = localStorage.getItem(CONSULTAS_STORAGE_KEY)
  if (dados) return JSON.parse(dados)
  
  const consultasIniciais = [
    { id: 'C001', pacienteId: 'P001', pacienteNome: 'Ana Clara Oliveira', data: '2026-10-02', horario: '09:00', tipo: 'Retorno', status: 'agendada' },
    { id: 'C002', pacienteId: 'P003', pacienteNome: 'Maria José Santos', data: '2026-10-02', horario: '10:30', tipo: 'Eletrocardiograma', status: 'agendada' },
    { id: 'C003', pacienteId: 'P005', pacienteNome: 'Francisca Souza Almeida', data: '2026-10-03', horario: '14:00', tipo: 'Ecocardiograma', status: 'agendada' },
    { id: 'C004', pacienteId: 'P007', pacienteNome: 'Lúcia Helena Costa', data: '2026-10-04', horario: '08:30', tipo: 'Retorno', status: 'agendada' },
    { id: 'C005', pacienteId: 'P002', pacienteNome: 'Carlos Eduardo Silva', data: '2026-10-05', horario: '11:00', tipo: 'Consulta Inicial', status: 'agendada' },
  ]
  localStorage.setItem(CONSULTAS_STORAGE_KEY, JSON.stringify(consultasIniciais))
  return consultasIniciais
}

function salvarConsultas(consultas) {
  localStorage.setItem(CONSULTAS_STORAGE_KEY, JSON.stringify(consultas))
}

// ─── API Service ────────────────────────────────────────────────────────────

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))

export const apiService = {
  /**
   * Busca todos os pacientes.
   */
  async getPacientes() {
    await delay(300)
    return [...PACIENTES]
  },

  /**
   * Busca um paciente pelo ID.
   */
  async getPaciente(id) {
    await delay(200)
    return PACIENTES.find(p => p.id === id) || null
  },

  /**
   * Busca todas as consultas agendadas.
   */
  async getConsultas() {
    await delay(300)
    return getConsultas()
  },

  /**
   * Agenda uma nova consulta.
   */
  async agendarConsulta(dados) {
    await delay(500)
    const consultas = getConsultas()
    const novaConsulta = {
      id: `C${String(consultas.length + 1).padStart(3, '0')}`,
      ...dados,
      status: 'agendada'
    }
    consultas.push(novaConsulta)
    salvarConsultas(consultas)
    return novaConsulta
  },

  /**
   * Cancela uma consulta pelo ID.
   */
  async cancelarConsulta(id) {
    await delay(300)
    const consultas = getConsultas()
    const idx = consultas.findIndex(c => c.id === id)
    if (idx !== -1) {
      consultas[idx].status = 'cancelada'
      salvarConsultas(consultas)
    }
    return consultas
  },

  /**
   * Retorna métricas do dashboard.
   */
  async getMetricas() {
    await delay(400)
    const consultas = getConsultas()
    const ativas = consultas.filter(c => c.status === 'agendada')

    return {
      totalPacientes: PACIENTES.length,
      consultasAgendadas: ativas.length,
      pacientesAltoRisco: PACIENTES.filter(p => p.risco === 'alto').length,
      pacientesRiscoModerado: PACIENTES.filter(p => p.risco === 'moderado').length,
      pacientesBaixoRisco: PACIENTES.filter(p => p.risco === 'baixo').length,
      mediaIdade: Math.round(PACIENTES.reduce((s, p) => s + p.idade, 0) / PACIENTES.length),
      mediaIMC: (PACIENTES.reduce((s, p) => s + p.imc, 0) / PACIENTES.length).toFixed(1),
      distribuicaoSexo: {
        masculino: PACIENTES.filter(p => p.sexo === 'M').length,
        feminino: PACIENTES.filter(p => p.sexo === 'F').length,
      },
      proximasConsultas: ativas.slice(0, 3)
    }
  }
}
