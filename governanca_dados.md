# 🛡️ Governança de Dados e Análise de Viés — CardioIA

## 1. Introdução

Este documento estabelece as diretrizes de governança de dados para o projeto CardioIA, abordando princípios de qualidade, segurança, ética e conformidade regulatória no tratamento de dados cardiológicos. A governança de dados é um pilar essencial em projetos de Inteligência Artificial aplicada à saúde, pois decisões algorítmicas baseadas em dados de baixa qualidade ou enviesados podem impactar diretamente a vida e a saúde dos pacientes.

---

## 2. Princípios de Governança de Dados em IA na Saúde

### 2.1. Qualidade dos Dados

A qualidade dos dados é o alicerce de qualquer sistema de IA confiável. Os princípios fundamentais incluem:

- **Completude**: Garantir que todas as variáveis relevantes estejam preenchidas, minimizando valores ausentes (missing values). No dataset CardioIA, todas as 500 linhas possuem dados completos para as 20 variáveis.
- **Consistência**: Assegurar que os dados sejam internamente coerentes e que as correlações entre variáveis reflitam relações clínicas plausíveis.
- **Acurácia**: Os dados devem representar fielmente a realidade que pretendem modelar. No caso de dados simulados, as distribuições devem ser baseadas em evidências epidemiológicas.
- **Atualidade (Timeliness)**: Os dados devem refletir o estado atual do conhecimento clínico e epidemiológico.
- **Rastreabilidade (Provenance)**: A origem, o processo de geração e as transformações aplicadas aos dados devem ser documentados.

### 2.2. Segurança e Privacidade

- **Criptografia**: Dados de saúde devem ser armazenados e transmitidos com criptografia adequada (AES-256 para armazenamento, TLS 1.3 para transmissão).
- **Controle de Acesso**: Implementar o princípio do menor privilégio, garantindo que apenas usuários autorizados acessem dados sensíveis.
- **Anonimização e Pseudonimização**: Dados que identifiquem pacientes devem ser anonimizados antes de serem utilizados para treinamento de modelos de IA.
- **Auditoria**: Manter logs de acesso e modificações nos dados para fins de rastreabilidade e compliance.

### 2.3. Transparência e Explicabilidade

- **Documentação**: Todos os datasets devem ser acompanhados de dicionários de dados, documentação de fontes e descrição de limitações.
- **Explicabilidade de Modelos**: Modelos de IA devem utilizar técnicas como SHAP, LIME e Attention Maps para tornar suas decisões interpretáveis por profissionais de saúde.
- **Reprodutibilidade**: O processo de geração e preparação de dados deve ser reprodutível, com scripts versionados e seeds aleatórias documentadas.

---

## 3. Conformidade com a LGPD

A Lei Geral de Proteção de Dados (Lei nº 13.709/2018) impõe requisitos específicos para o tratamento de dados sensíveis de saúde:

### 3.1. Bases Legais para Tratamento de Dados de Saúde

O tratamento de dados pessoais sensíveis (incluindo dados de saúde) deve ser fundamentado em uma das seguintes bases legais (Art. 11 da LGPD):

| Base Legal | Descrição | Aplicabilidade ao CardioIA |
|-----------|-----------|---------------------------|
| Consentimento | Manifestação livre, informada e inequívoca do titular | Essencial para dados reais de pacientes |
| Tutela da saúde | Procedimentos realizados por profissionais de saúde | Aplicável em contexto clínico |
| Pesquisa | Estudos por órgão de pesquisa, preferencialmente com anonimização | **Aplicável ao contexto acadêmico** |
| Exercício regular de direitos | Em processo judicial, administrativo ou arbitral | Não aplicável |
| Proteção da vida | Proteção da vida ou incolumidade física do titular | Situações de emergência |

### 3.2. Medidas Implementadas no CardioIA

- **Dados Simulados**: O dataset numérico do CardioIA utiliza dados simulados computacionalmente, não vinculados a indivíduos reais, eliminando riscos diretos à privacidade.
- **IDs Anonimizados**: Os identificadores de pacientes são sequenciais (CARDIO_0001 a CARDIO_0500) e não possuem correspondência com pessoas reais.
- **Textos de Fontes Públicas**: Os textos médicos são baseados em publicações científicas de acesso aberto (SciELO, BVS), não contendo dados de pacientes individuais.
- **Imagens de Datasets Públicos**: As imagens ECG são provenientes de datasets públicos aprovados por comitês de ética, com anonimização prévia dos identificadores dos pacientes.

### 3.3. Direitos dos Titulares (Art. 18 da LGPD)

Mesmo em contexto acadêmico, é importante compreender os direitos que a LGPD garante aos titulares de dados:

1. **Confirmação** da existência de tratamento
2. **Acesso** aos dados pessoais
3. **Correção** de dados incompletos, inexatos ou desatualizados
4. **Anonimização**, bloqueio ou eliminação de dados desnecessários
5. **Portabilidade** dos dados
6. **Eliminação** dos dados tratados com consentimento
7. **Informação** sobre compartilhamento
8. **Revogação** do consentimento

---

## 4. Análise de Viés nos Dados

### 4.1. O que é Viés em IA?

Viés algorítmico ocorre quando um modelo de IA produz resultados sistematicamente injustos ou imprecisos para determinados subgrupos populacionais. Em saúde cardiovascular, o viés pode ter consequências graves, como subdiagnóstico em mulheres ou tratamento inadequado de minorias étnicas.

### 4.2. Tipos de Viés Identificados

#### Viés de Seleção (Selection Bias)

| Viés | Descrição | Impacto no CardioIA | Mitigação |
|------|-----------|---------------------|-----------|
| Sub-representação de gênero | Mulheres historicamente sub-representadas em estudos CV | Dataset com 55% homens / 45% mulheres — reflete epidemiologia real, mas pode subrepresentar manifestações atípicas femininas | Incluir variáveis específicas de apresentação por sexo nas fases futuras |
| Viés etário | Dados concentrados em faixa etária 45-75 anos | Jovens (<30) e muito idosos (>85) sub-representados | Ampliar faixas etárias em iterações futuras |
| Viés étnico-racial | Ausência da variável raça/etnia no dataset | Impossibilidade de analisar disparidades raciais em risco CV | Considerar inclusão de variável étnica com base em dados do IBGE |

#### Viés de Medição (Measurement Bias)

| Viés | Descrição | Impacto | Mitigação |
|------|-----------|---------|-----------|
| Efeito do avental branco | PA em consultório pode ser maior que habitual | Dados de pressão podem superestimar prevalência de hipertensão | Incluir variáveis de MAPA/MRPA nas fases futuras |
| Critérios diagnósticos variáveis | Diferentes diretrizes usam pontos de corte distintos | Classificação binária (0/1) simplifica a realidade clínica | Considerar variável-alvo contínua (score de risco) |

#### Viés de Confusão (Confounding Bias)

| Viés | Descrição | Impacto | Mitigação |
|------|-----------|---------|-----------|
| Variáveis socioeconômicas ausentes | Renda, escolaridade e acesso à saúde não estão no dataset | Esses fatores influenciam significativamente os desfechos CV | Incluir variáveis socioeconômicas em fases futuras |
| Comportamentais não capturadas | Dieta, atividade física, consumo de álcool | Fatores de risco modificáveis importantes não representados | Expandir dataset com variáveis comportamentais |

### 4.3. Estratégias de Mitigação de Viés

1. **Balanceamento do dataset**: Utilizar técnicas como SMOTE, undersampling ou oversampling para equilibrar classes desbalanceadas na variável-alvo.

2. **Auditoria de equidade**: Avaliar o desempenho do modelo separadamente para cada subgrupo (sexo, faixa etária) para identificar disparidades.

3. **Métricas de equidade**: Além de acurácia global, monitorar métricas como:
   - **Equalized Odds**: Taxas de verdadeiro positivo e falso positivo iguais entre subgrupos
   - **Demographic Parity**: Probabilidade de predição positiva igual entre subgrupos
   - **Calibration**: Probabilidades preditas correspondentes às frequências observadas em cada subgrupo

4. **Diversificação de fontes**: Combinar múltiplas fontes de dados para reduzir o viés de uma fonte única.

5. **Validação externa**: Testar modelos em datasets independentes de populações diversas.

---

## 5. Considerações Éticas no Uso de Dados Médicos

### 5.1. Princípios Bioéticos Aplicados à IA

| Princípio | Descrição | Aplicação no CardioIA |
|-----------|-----------|----------------------|
| **Beneficência** | Maximizar o benefício para o paciente | Desenvolver modelos que melhorem o diagnóstico e a predição de risco CV |
| **Não-maleficência** | Não causar dano | Garantir que vieses algorítmicos não levem a subdiagnóstico ou tratamento inadequado |
| **Autonomia** | Respeitar as decisões do paciente | Assegurar consentimento informado para uso de dados reais; manter o médico como decisor final |
| **Justiça** | Distribuir benefícios e riscos de forma equitativa | Garantir que os modelos funcionem igualmente bem para todos os subgrupos populacionais |

### 5.2. IA como Ferramenta de Suporte, Não de Substituição

É fundamental enfatizar que os modelos de IA desenvolvidos no CardioIA são ferramentas de **suporte à decisão clínica**, e não substitutos do julgamento médico. A responsabilidade final pelo diagnóstico e tratamento permanece com o profissional de saúde habilitado.

### 5.3. Transparência com o Paciente

Pacientes devem ser informados quando algoritmos de IA são utilizados em seu processo de cuidado, compreendendo:
- Que tipo de dados são coletados e processados
- Como os algoritmos influenciam as decisões médicas
- Quais são as limitações conhecidas dos modelos
- Como exercer seus direitos em relação aos dados

---

## 6. Matriz de Riscos e Controles

| Risco | Probabilidade | Impacto | Controle |
|-------|:---:|:---:|----------|
| Dados simulados não representam população real | Média | Alto | Basear distribuições em dados epidemiológicos oficiais (DATASUS, PNS) |
| Viés de gênero no modelo preditivo | Média | Alto | Auditar métricas de desempenho por sexo |
| Vazamento de dados de pacientes (fases futuras) | Baixa | Muito Alto | Implementar anonimização, criptografia e controle de acesso |
| Overfitting em dados simulados | Alta | Médio | Utilizar validação cruzada e reservar dados de teste |
| Uso inadequado de predições por não-especialistas | Média | Alto | Incluir disclaimers e limitar acesso a profissionais qualificados |

---

## 7. Plano de Ação para Fases Futuras

| Fase | Ação de Governança | Responsável |
|------|---------------------|-------------|
| Fase 2 | Implementar pipeline de validação de dados com testes automatizados | Equipe de dados |
| Fase 3 | Realizar auditoria de viés nos modelos treinados | Equipe de ML |
| Fase 4 | Implementar criptografia end-to-end no módulo de IoT | Equipe de segurança |
| Fase 5 | Conduzir avaliação de impacto à proteção de dados (DPIA) | Equipe jurídica + dados |
| Fase 6 | Testar explicabilidade dos modelos com profissionais de saúde | Equipe clínica + ML |
| Fase 7 | Documentar todo o pipeline de governança para auditoria | Todas as equipes |

---

## 8. Referências

- Brasil. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD).
- Conselho Federal de Medicina. Resolução CFM nº 2.314/2022 - Telemedicina.
- European Commission. Ethics Guidelines for Trustworthy AI, 2019.
- Obermeyer Z, et al. Dissecting racial bias in an algorithm used to manage the health of populations. Science, 2019.
- Rajkomar A, et al. Ensuring Fairness in Machine Learning to Advance Health Equity. Annals of Internal Medicine, 2018.
- World Health Organization. Ethics and Governance of Artificial Intelligence for Health, 2021.
