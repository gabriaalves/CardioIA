# 📊 Dicionário de Dados — CardioIA

## Dataset: `cardio_dataset.csv`

Este dicionário descreve detalhadamente cada variável do dataset cardiológico simulado, incluindo tipo, faixa de valores, unidade de medida e relevância clínica para o projeto CardioIA.

---

### Variáveis de Identificação

| # | Variável | Tipo | Faixa de Valores | Unidade | Descrição |
|---|----------|------|-------------------|---------|-----------|
| 1 | `patient_id` | String | CARDIO_0001 a CARDIO_0500 | — | Identificador único anonimizado do paciente |

---

### Variáveis Demográficas

| # | Variável | Tipo | Faixa de Valores | Unidade | Descrição | Relevância Clínica |
|---|----------|------|-------------------|---------|-----------|-------------------|
| 2 | `idade` | Inteiro | 18–95 | anos | Idade do paciente | Principal fator de risco não modificável. Risco CV dobra a cada década após 45 anos (homens) e 55 anos (mulheres). |
| 3 | `sexo` | Categórico | M, F | — | Sexo biológico | Homens têm risco CV 2-5x maior antes da menopausa feminina. Manifestações clínicas diferem entre sexos. |

---

### Variáveis Antropométricas

| # | Variável | Tipo | Faixa de Valores | Unidade | Descrição | Relevância Clínica |
|---|----------|------|-------------------|---------|-----------|-------------------|
| 4 | `peso_kg` | Float | 40.0–160.0 | kg | Peso corporal | Utilizado no cálculo do IMC. Sobrepeso e obesidade são fatores de risco CV independentes. |
| 5 | `altura_cm` | Float | 140.0–200.0 | cm | Estatura | Utilizada no cálculo do IMC. Variações por sexo refletem perfil antropométrico brasileiro (IBGE). |
| 6 | `imc` | Float | 15.0–55.0 | kg/m² | Índice de Massa Corporal | Classificação OMS: <18.5 (baixo peso), 18.5-24.9 (normal), 25-29.9 (sobrepeso), ≥30 (obesidade). IMC ≥30 associado a risco CV 2x maior. |

---

### Variáveis de Sinais Vitais

| # | Variável | Tipo | Faixa de Valores | Unidade | Descrição | Relevância Clínica |
|---|----------|------|-------------------|---------|-----------|-------------------|
| 7 | `pressao_sistolica` | Inteiro | 90–200 | mmHg | Pressão arterial sistólica | Principal fator de risco modificável para DCV. ≥140 mmHg define hipertensão (Diretrizes Brasileiras). |
| 8 | `pressao_diastolica` | Inteiro | 55–130 | mmHg | Pressão arterial diastólica | ≥90 mmHg contribui para diagnóstico de hipertensão. Elevação isolada é menos comum. |
| 9 | `frequencia_cardiaca_repouso` | Inteiro | 45–110 | bpm | Frequência cardíaca em repouso | FC de repouso >80 bpm associada a maior risco CV. Variável central em IoT e monitoramento wearable. |

---

### Variáveis do Perfil Lipídico

| # | Variável | Tipo | Faixa de Valores | Unidade | Descrição | Relevância Clínica |
|---|----------|------|-------------------|---------|-----------|-------------------|
| 10 | `colesterol_total` | Inteiro | 120–380 | mg/dL | Colesterol total sérico | Desejável <200. Cada aumento de 10 mg/dL eleva risco CV em ~2%. Marcador de aterosclerose. |
| 11 | `colesterol_ldl` | Inteiro | 50–250 | mg/dL | Colesterol LDL | "Colesterol ruim". Principal alvo terapêutico. Redução de 1 mmol/L reduz risco CV em ~22%. |
| 12 | `colesterol_hdl` | Inteiro | 20–100 | mg/dL | Colesterol HDL | "Colesterol bom". Efeito cardioprotetor. HDL <40 (homens) ou <50 (mulheres) é fator de risco. |
| 13 | `triglicerides` | Inteiro | 50–500 | mg/dL | Triglicerídeos séricos | ≥150 mg/dL: hipertrigliceridemia. Componente da síndrome metabólica. Associado a pancreatite em níveis muito elevados. |

---

### Variáveis Metabólicas

| # | Variável | Tipo | Faixa de Valores | Unidade | Descrição | Relevância Clínica |
|---|----------|------|-------------------|---------|-----------|-------------------|
| 14 | `glicemia_jejum` | Inteiro | 65–300 | mg/dL | Glicemia de jejum | Normal <100, pré-diabetes 100-125, diabetes ≥126 mg/dL. Diabetes aumenta risco CV em 2-4x. |

---

### Variáveis de Fatores de Risco (Binárias)

| # | Variável | Tipo | Valores | Unidade | Descrição | Relevância Clínica |
|---|----------|------|---------|---------|-----------|-------------------|
| 15 | `fumante` | Inteiro | 0 (não), 1 (sim) | — | Status de tabagismo ativo | Risco CV 2-4x maior em fumantes. Cessação é a intervenção isolada mais eficaz. |
| 16 | `diabetes` | Inteiro | 0 (não), 1 (sim) | — | Diagnóstico de diabetes mellitus | Fator de risco independente. Correlacionado com glicemia, IMC e idade no dataset. |
| 17 | `historico_familiar_cardiaco` | Inteiro | 0 (não), 1 (sim) | — | Histórico de DCV prematura em parentes de 1º grau | Fator não modificável. DCV antes dos 55 (homens) ou 65 (mulheres) anos em parentes. |

---

### Variáveis Clínicas Categóricas

| # | Variável | Tipo | Valores | Descrição | Relevância Clínica |
|---|----------|------|---------|-----------|-------------------|
| 18 | `tipo_dor_toracica` | Inteiro | 0, 1, 2, 3 | Tipo de dor torácica apresentada | 0=Assintomático, 1=Angina típica, 2=Angina atípica, 3=Dor não-anginosa. Angina típica tem alta correlação com doença coronariana. |
| 19 | `resultado_ecg_repouso` | Inteiro | 0, 1, 2 | Resultado do ECG em repouso | 0=Normal, 1=Anormalidade ST-T, 2=Hipertrofia ventricular esquerda. Alterações de ST-T sugerem isquemia. |

---

### Variável-Alvo

| # | Variável | Tipo | Valores | Descrição | Relevância Clínica |
|---|----------|------|---------|-----------|-------------------|
| 20 | `diagnostico_doenca_cardiaca` | Inteiro | 0 (ausência), 1 (presença) | Presença de doença cardíaca diagnosticada | Variável-alvo para modelos de classificação. Calculada com base em score de risco multifatorial. |

---

## Correlações Modeladas no Dataset

O dataset foi gerado com correlações clinicamente plausíveis entre variáveis:

| Relação | Direção | Justificativa Clínica |
|---------|---------|----------------------|
| IMC ↔ Pressão Arterial | Positiva | Obesidade é fator de risco para hipertensão |
| IMC ↔ Colesterol Total | Positiva | Sobrepeso associado a dislipidemia |
| IMC ↔ HDL | Negativa | Obesidade reduz HDL-colesterol |
| IMC ↔ Glicemia | Positiva | Obesidade promove resistência insulínica |
| Idade ↔ Pressão Arterial | Positiva | Enrijecimento arterial progressivo |
| Idade ↔ Colesterol Total | Positiva | Acúmulo lipídico com o envelhecimento |
| Glicemia ↔ Diabetes | Positiva | Glicemia ≥126 mg/dL: critério diagnóstico |
| Sexo ↔ HDL | Mulheres têm HDL mais alto | Efeito estrogênico sobre metabolismo lipídico |
| Múltiplos fatores ↔ Diagnóstico | Score logístico | Modelo multifatorial com interações |

---

## Notas Metodológicas

- **Tipo de dados**: Simulados (gerados computacionalmente)
- **Seed aleatória**: 42 (para reprodutibilidade)
- **Distribuições**: Baseadas em dados epidemiológicos brasileiros (DATASUS, PNS, Vigitel, ABC Cardiol)
- **Correlações**: Modeladas para refletir relações fisiológicas e patológicas reais
- **Anonimização**: IDs são sequenciais e não vinculados a indivíduos reais
