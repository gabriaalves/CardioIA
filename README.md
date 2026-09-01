<div align="center">

# 🫀 CardioIA — A Nova Era da Cardiologia Inteligente

### Fase 1: Batimentos de Dados

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Fase%201%20Completa-success?style=for-the-badge)
![FIAP](https://img.shields.io/badge/FIAP-IA%202025-red?style=for-the-badge)

*Plataforma digital inteligente que simula o ecossistema de uma cardiologia moderna, integrando dados clínicos, Machine Learning, Visão Computacional, IoT e agentes inteligentes.*

---

[Dados Numéricos](#parte-1--dados-numéricos-iot) •
[Dados Textuais](#parte-2--dados-textuais-nlp) •
[Dados Visuais](#parte-3--dados-visuais-visão-computacional) •
[Governança](#governança-de-dados-e-viés) •
[Referências](#referências-bibliográficas)

</div>

---

## 📋 Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Parte 1 – Dados Numéricos (IoT)](#parte-1--dados-numéricos-iot)
- [Parte 2 – Dados Textuais (NLP)](#parte-2--dados-textuais-nlp)
- [Parte 3 – Dados Visuais (Visão Computacional)](#parte-3--dados-visuais-visão-computacional)
- [Governança de Dados e Viés](#governança-de-dados-e-viés)
- [Como Executar](#como-executar)
- [Links para os Dados](#links-para-os-dados)
- [Referências Bibliográficas](#referências-bibliográficas)
- [Equipe](#equipe)

---

## Sobre o Projeto

O **CardioIA** é um projeto acadêmico inovador do curso de Inteligência Artificial da FIAP, desenvolvido sob a metodologia PBL (Project Based Learning). O projeto simula o ecossistema completo de uma cardiologia inteligente, sendo desenvolvido ao longo de 7 fases que abrangem desde a coleta de dados até a implantação de agentes inteligentes.

### Fase 1 — Batimentos de Dados

Nesta primeira fase, assumimos o papel de **cientistas de dados hospitalares** com a missão de levantar, organizar e compreender dados cardiológicos que alimentarão os módulos inteligentes do CardioIA nas fases seguintes. Esta fase constrói a **base de dados** que sustentará todo o ecossistema.

### Objetivos da Fase 1

1. **Dados Numéricos (IoT)**: Preparar um dataset estruturado com variáveis clínicas de pacientes cardíacos
2. **Dados Textuais (NLP)**: Coletar textos médicos para futura análise por algoritmos de Processamento de Linguagem Natural
3. **Dados Visuais (VC)**: Reunir imagens de exames cardiológicos para treinamento de modelos de Visão Computacional
4. **Governança de Dados**: Documentar princípios de governança, conformidade com LGPD e análise de viés

---

## Estrutura do Repositório

```
CardioIA/
│
├── README.md                          # 📄 Este arquivo — documentação principal
├── LICENSE                            # ⚖️ Licença MIT
├── .gitignore                         # 🚫 Arquivos ignorados pelo Git
├── requirements.txt                   # 📦 Dependências Python do projeto
│
├── data/
│   └── cardio_dataset.csv             # 📊 Dataset numérico (500 linhas, 20 variáveis)
│
├── docs/
│   ├── texto_01_estatistica_cardiovascular_brasil.txt    # 📝 Texto 1: Epidemiologia CV no Brasil
│   ├── texto_02_fatores_risco_doencas_cardiacas.txt      # 📝 Texto 2: Fatores de risco cardiovascular
│   ├── texto_03_diretrizes_hipertensao_arterial.txt      # 📝 Texto 3: Diretrizes de hipertensão
│   └── texto_04_inteligencia_artificial_cardiologia.txt  # 📝 Texto 4: IA aplicada à cardiologia
│
├── assets/
│   └── ecg_images/                    # 🖼️ Imagens ECG (120 imagens)
│       ├── normal/                    # 🟢 40 ECGs com ritmo sinusal normal
│       ├── infarto_miocardio/         # 🔴 40 ECGs com padrão de infarto
│       ├── arritmia/                  # 🟣 40 ECGs com arritmias diversas
│       └── README_IMAGES.md           # 📄 Instruções e organização
│
├── scripts/
│   ├── gerar_dataset.py               # ⚙️ Script gerador do dataset
│   └── eda_cardio.py                  # 📈 Script de Análise Exploratória (EDA + gráficos)
│
├── figures/                           # 📊 Gráficos gerados pelo EDA (9 visualizações)
│
├── dicionario_dados.md                # 📖 Dicionário detalhado de variáveis
├── governanca_dados.md                # 🛡️ Governança de dados e análise de viés
└── index.html                         # 🌐 Dashboard interativo (abrir com servidor local)
```

---

## Parte 1 – Dados Numéricos (IoT)

### Descrição do Dataset

O arquivo [`data/cardio_dataset.csv`](data/cardio_dataset.csv) contém **500 registros simulados** de pacientes cardíacos com **20 variáveis clínicas**, gerados computacionalmente com distribuições baseadas em dados epidemiológicos brasileiros.

> **Origem dos dados**: Dados **simulados** por meio do script [`scripts/gerar_dataset.py`](scripts/gerar_dataset.py), utilizando distribuições estatísticas baseadas em dados reais do DATASUS, Pesquisa Nacional de Saúde (PNS), Vigitel e publicações dos Arquivos Brasileiros de Cardiologia (ABC Cardiol). Seed aleatória: 42 (para reprodutibilidade).

### Variáveis do Dataset

| # | Variável | Tipo | Descrição | Relevância Clínica |
|:-:|----------|:----:|-----------|-------------------|
| 1 | `patient_id` | String | ID anonimizado do paciente | Identificação única |
| 2 | `idade` | int | Idade (18-95 anos) | Principal fator de risco não modificável. Risco CV dobra a cada década após 45/55 anos |
| 3 | `sexo` | cat | Sexo biológico (M/F) | Homens: risco CV 2-5x maior pré-menopausa |
| 4 | `peso_kg` | float | Peso corporal em kg | Base para cálculo do IMC |
| 5 | `altura_cm` | float | Estatura em cm | Base para cálculo do IMC |
| 6 | `imc` | float | Índice de Massa Corporal (kg/m²) | ≥30: obesidade. Fator de risco metabólico e hemodinâmico |
| 7 | `pressao_sistolica` | int | PA sistólica (mmHg) | ≥140: hipertensão. Principal fator modificável para DCV |
| 8 | `pressao_diastolica` | int | PA diastólica (mmHg) | ≥90: contribui para diagnóstico de hipertensão |
| 9 | `frequencia_cardiaca_repouso` | int | FC em repouso (bpm) | >80 bpm: risco CV aumentado. Central em IoT/wearables |
| 10 | `colesterol_total` | int | Colesterol total (mg/dL) | >200: dislipidemia. Marcador de aterosclerose |
| 11 | `colesterol_ldl` | int | LDL-colesterol (mg/dL) | "Colesterol ruim". Principal alvo terapêutico |
| 12 | `colesterol_hdl` | int | HDL-colesterol (mg/dL) | "Colesterol bom". <40 (H) ou <50 (M): fator de risco |
| 13 | `triglicerides` | int | Triglicerídeos (mg/dL) | ≥150: componente da síndrome metabólica |
| 14 | `glicemia_jejum` | int | Glicemia de jejum (mg/dL) | ≥126: critério de diabetes. Diabetes aumenta risco CV 2-4x |
| 15 | `fumante` | bin | Tabagismo ativo (0/1) | Risco CV 2-4x maior. Cessação é a intervenção mais eficaz |
| 16 | `diabetes` | bin | Diabetes mellitus (0/1) | Fator independente. Promove disfunção endotelial e aterosclerose |
| 17 | `historico_familiar_cardiaco` | bin | Histórico familiar de DCV (0/1) | DCV prematura em parentes: preditor independente de risco |
| 18 | `tipo_dor_toracica` | cat | Tipo de dor (0-3) | 0=Assintomático, 1=Angina típica, 2=Atípica, 3=Não-anginosa |
| 19 | `resultado_ecg_repouso` | cat | ECG em repouso (0-2) | 0=Normal, 1=Anormalidade ST-T, 2=Hipertrofia VE |
| 20 | `diagnostico_doenca_cardiaca` | bin | **Variável-alvo** (0/1) | Presença de doença cardíaca. Calculada por score multifatorial |

### Justificativa das Variáveis Mais Relevantes

As variáveis foram selecionadas com base em sua relevância clínica comprovada pela literatura cardiológica:

1. **Idade e Sexo** — São os principais fatores de risco não modificáveis. O envelhecimento promove enrijecimento arterial e disfunção endotelial. Homens apresentam maior prevalência de doença coronariana até a menopausa feminina.

2. **Pressão Arterial (sistólica/diastólica)** — A hipertensão arterial é o **principal fator de risco modificável** para DCV, afetando ~32% da população brasileira adulta (Vigitel, 2023). É a variável mais importante em contexto de IoT, pois pode ser monitorada continuamente por dispositivos vestíveis.

3. **Perfil Lipídico (colesterol total, LDL, HDL, triglicerídeos)** — Fundamental para avaliação do risco aterosclerótico. A redução de 1 mmol/L no LDL diminui o risco de eventos CV em ~22% (CTT Collaboration, Lancet, 2010).

4. **Glicemia e Diabetes** — Diabetes aumenta o risco CV em 2-4x e frequentemente coexiste com outros fatores de risco (síndrome metabólica).

5. **IMC** — Obesidade (IMC ≥30) é um fator de risco metabólico que contribui para hipertensão, dislipidemia e resistência insulínica. Segundo o EDA realizado, **35.6% dos pacientes do dataset são obesos**, e a prevalência de doença cardíaca aumenta progressivamente com o IMC (de 23.8% em baixo peso a 61.5% em obesidade grau III).

6. **Frequência Cardíaca de Repouso** — Variável central para projetos de IoT e monitoramento com wearables. FC >80 bpm em repouso está associada a maior risco cardiovascular.

### Resultados da Análise Exploratória (EDA)

O script [`scripts/eda_cardio.py`](scripts/eda_cardio.py) produziu os seguintes insights principais:

| Insight | Valor |
|---------|-------|
| Prevalência de doença cardíaca | 42.0% |
| Maior correlação positiva com DC | Idade (r = 0.265) |
| Maior correlação negativa com DC | HDL-colesterol (r = -0.086) |
| Pacientes hipertensos (PA ≥ 140) | 8.6% |
| Pacientes obesos (IMC ≥ 30) | 35.6% |
| Fumantes | 18.6% |
| Diabéticos | 21.4% |

**Correlações clinicamente relevantes modeladas**:
- Colesterol total ↔ LDL: r = 0.887 (esperado: ~60-70% do total é LDL)
- Peso ↔ IMC: r = 0.845 (relação matemática direta)
- Idade ↔ Pressão sistólica: r = 0.423 (enrijecimento arterial com idade)
- Glicemia ↔ Diabetes: r = 0.361 (critério diagnóstico)

### Link para os Dados Numéricos

🔗 **Link público para o dataset**: [Acessar no Google Drive](https://drive.google.com/drive/folders/12m6HMAOG698t0vBn6kGeKNU_aVWNo5Ry?usp=sharing)

> ℹ️ Também disponível diretamente no repositório em [`data/cardio_dataset.csv`](data/cardio_dataset.csv)

---

## Parte 2 – Dados Textuais (NLP)

### Descrição dos Textos

A pasta [`docs/`](docs/) contém **4 textos em português** sobre saúde cardiovascular, totalizando aproximadamente 8.000 palavras de conteúdo técnico-científico. Os textos foram redigidos com base em publicações científicas reais das principais fontes da área:

| # | Arquivo | Tema | Palavras | Fontes |
|:-:|---------|------|:--------:|--------|
| 1 | [`texto_01_estatistica_cardiovascular_brasil.txt`](docs/texto_01_estatistica_cardiovascular_brasil.txt) | Panorama epidemiológico das DCV no Brasil | ~1.200 | ABC Cardiol, DATASUS, PNS |
| 2 | [`texto_02_fatores_risco_doencas_cardiacas.txt`](docs/texto_02_fatores_risco_doencas_cardiacas.txt) | Fatores de risco modificáveis e não-modificáveis | ~2.000 | SBC, OMS, BVS, INTERHEART |
| 3 | [`texto_03_diretrizes_hipertensao_arterial.txt`](docs/texto_03_diretrizes_hipertensao_arterial.txt) | Diretrizes brasileiras de hipertensão arterial | ~2.000 | SBC, SBH, ESC/ESH |
| 4 | [`texto_04_inteligencia_artificial_cardiologia.txt`](docs/texto_04_inteligencia_artificial_cardiologia.txt) | Estado da arte da IA na cardiologia | ~2.500 | Nature Medicine, Lancet, JAMA |

### Origem dos Textos

Os textos foram elaborados com base em publicações científicas de acesso aberto das seguintes fontes:
- **SciELO** (Scientific Electronic Library Online) — Artigos dos Arquivos Brasileiros de Cardiologia
- **BVS** (Biblioteca Virtual em Saúde) — Publicações sobre doenças cardiovasculares
- **Sociedade Brasileira de Cardiologia (SBC)** — Diretrizes clínicas e estatísticas
- **Organização Mundial da Saúde (OMS)** — Relatórios sobre doenças cardiovasculares
- **Periódicos internacionais** — Nature Medicine, The Lancet, JAMA Cardiology

### Potencial de Uso em NLP

Esses textos são recursos valiosos para múltiplas tarefas de Processamento de Linguagem Natural (NLP) nas fases seguintes do CardioIA:

#### 1. Extração de Entidades Nomeadas (NER)
- **O que é**: Identificação automática de entidades como doenças, sintomas, medicamentos, procedimentos e órgãos mencionados nos textos.
- **Exemplo**: No texto sobre fatores de risco, algoritmos de NER podem extrair entidades como `hipertensão arterial` (doença), `betabloqueadores` (medicamento), `disfunção endotelial` (mecanismo), `140 mmHg` (valor limiar).
- **Relevância**: Permite construir ontologias cardiológicas e bases de conhecimento estruturadas a partir de textos não estruturados, fundamentais para sistemas de suporte à decisão clínica.

#### 2. Análise de Sentimento e Classificação de Severidade
- **O que é**: Classificação do tom e da gravidade das informações contidas nos textos.
- **Exemplo**: Trechos que mencionam "fator de risco mais potente" ou "condição de alto risco" podem ser classificados com polaridade negativa/alta severidade, enquanto "efeito cardioprotetor" recebe classificação positiva.
- **Relevância**: Em aplicações futuras, a análise de sentimento pode ser aplicada a relatos de pacientes em fóruns de saúde e redes sociais para monitorar a percepção sobre sintomas e adesão ao tratamento.

#### 3. Classificação de Tópicos (Topic Modeling)
- **O que é**: Identificação automática dos temas abordados nos textos usando algoritmos como LDA (Latent Dirichlet Allocation).
- **Exemplo**: Os 4 textos abordam tópicos distintos (epidemiologia, fatores de risco, hipertensão, IA) que podem ser automaticamente identificados e categorizados.
- **Relevância**: Permite organizar automaticamente grandes volumes de literatura médica, identificando tendências de pesquisa e lacunas no conhecimento cardiológico.

#### 4. Sumarização Automática
- **O que é**: Geração de resumos concisos a partir de textos extensos.
- **Exemplo**: Algoritmos de sumarização podem condensar o texto de 2.000 palavras sobre fatores de risco em um resumo de 200 palavras mantendo as informações mais relevantes.
- **Relevância**: Em contexto hospitalar, a sumarização automática de prontuários e relatórios pode economizar tempo significativo dos profissionais de saúde.

#### 5. Similaridade Semântica e Busca Inteligente
- **O que é**: Cálculo de similaridade entre textos e consultas usando embeddings.
- **Exemplo**: Uma busca por "tratamento para pressão alta" deve retornar trechos do texto 3 (diretrizes de hipertensão) com alta relevância.
- **Relevância**: Fundamental para chatbots de triagem e sistemas de busca em bases de conhecimento médico.

### Justificativa da Relevância para IA em Saúde

A análise de textos médicos por NLP é essencial porque:

1. **~80% dos dados de saúde são não-estruturados** (notas de evolução, laudos, relatórios), e NLP é a única forma de extrair informações deles de maneira escalável.
2. **A literatura médica cresce exponencialmente** — mais de 1 milhão de artigos biomédicos são publicados por ano, impossibilitando a leitura manual por profissionais.
3. **Erros de comunicação** são uma das principais causas de eventos adversos em hospitais; NLP pode padronizar e verificar a consistência de registros clínicos.
4. **A telemedicina** depende cada vez mais de interações textuais (chat, mensagens) que podem ser analisadas por algoritmos de NLP para triagem e priorização.

---

## Parte 3 – Dados Visuais (Visão Computacional)

### Descrição das Imagens

A pasta [`assets/ecg_images/`](assets/ecg_images/) contém **120+ imagens de eletrocardiogramas (ECGs)** de 12 derivações, obtidas de datasets públicos de acesso aberto aprovados por comitês de ética.

### Fonte das Imagens

As imagens foram obtidas do dataset público:
- **ECG Images Dataset of Cardiac and COVID-19 Patients** — Disponível no Mendeley Data e Kaggle
- **Publicação**: Khan AH, et al. *Data in Brief*, 2021
- **Licença**: CC BY 4.0 (Creative Commons Attribution)
- **Aprovação ética**: Dataset aprovado por comitê de ética, com anonimização prévia

### Organização das Imagens

As imagens estão organizadas em 3 categorias clínicas:

```
ecg_images/
├── normal/              (≥40 imagens) — ECGs com ritmo sinusal normal
├── infarto_miocardio/   (≥40 imagens) — ECGs com padrão de infarto (supradesnivelamento ST)
└── arritmia/            (≥40 imagens) — ECGs com diferentes tipos de arritmias
```

> Instruções detalhadas de download estão disponíveis em [`assets/ecg_images/README_IMAGES.md`](assets/ecg_images/README_IMAGES.md).

### Link para as Imagens

🔗 **Link público para as imagens ECG**: [Acessar no Google Drive](https://drive.google.com/drive/folders/1D6pXrsmjo5gJzfLwCx31hHX0H86eZY2W?usp=sharing)

> ℹ️ Também disponíveis diretamente no repositório em [`assets/ecg_images/`](assets/ecg_images/)

### Potencial para Visão Computacional

As imagens ECG são particularmente adequadas para algoritmos de Visão Computacional por diversas razões:

#### 1. Classificação de Arritmias
- **Técnica**: Redes Neurais Convolucionais (CNNs) como ResNet, EfficientNet e VGG
- **Objetivo**: Classificar automaticamente o tipo de ritmo cardíaco (normal, fibrilação atrial, taquicardia ventricular, etc.)
- **Impacto**: O estudo de Hannun et al. (Nature Medicine, 2019) demonstrou que CNNs superam cardiologistas na classificação de 12 tipos de arritmias

#### 2. Detecção de Infarto Agudo do Miocárdio
- **Técnica**: Transfer Learning com modelos pré-treinados (ImageNet → ECG)
- **Objetivo**: Identificar padrões de supradesnivelamento de ST indicativos de infarto
- **Impacto**: Diagnóstico precoce de infarto pode reduzir a mortalidade em até 50% quando tratado nas primeiras horas

#### 3. Segmentação de Ondas
- **Técnica**: Redes de segmentação semântica (U-Net)
- **Objetivo**: Delinear automaticamente as ondas P, complexo QRS e onda T do traçado eletrocardiográfico
- **Impacto**: Permite medições automáticas de intervalos (PR, QT, QRS) fundamentais para o diagnóstico

#### 4. Detecção de Bordas e Extração de Características
- **Técnica**: Filtros de Canny, Sobel, Laplaciano e técnicas de processamento de imagem
- **Objetivo**: Identificar contornos e formas das ondas cardíacas para extração de features
- **Impacto**: Base para pipelines de feature engineering em modelos de Machine Learning

#### 5. Reconhecimento de Anomalias (Anomaly Detection)
- **Técnica**: Autoencoders Variacionais (VAE) e Redes Adversárias Generativas (GAN)
- **Objetivo**: Detectar ECGs anormais sem necessidade de rótulos específicos
- **Impacto**: Útil para triagem em larga escala onde a maioria dos ECGs é normal

### Justificativa da Importância para IA em Saúde

1. **Escala**: O ECG é o exame cardiológico mais realizado mundialmente — a IA pode analisar milhões de registros que seriam impossíveis de revisar manualmente.
2. **Acessibilidade**: Equipamentos de ECG portáteis são relativamente baratos e disponíveis até em áreas remotas, tornando a IA um multiplicador de acesso.
3. **Velocidade**: Diagnóstico automatizado reduz o tempo de análise de minutos para segundos, crucial em emergências cardíacas.
4. **Consistência**: A IA não sofre de fadiga ou viés de confirmação, garantindo análise padronizada.
5. **Telemedicina**: ECGs portáteis + IA permitem diagnóstico remoto em comunidades sem cardiologistas.

---

## Governança de Dados e Viés

A governança de dados é um pilar essencial no CardioIA. O documento completo está disponível em [`governanca_dados.md`](governanca_dados.md), e abrange:

### Conformidade com LGPD (Lei nº 13.709/2018)

| Aspecto | Implementação no CardioIA |
|---------|--------------------------|
| **Dados sensíveis** | Dataset utiliza dados simulados, sem vínculo com indivíduos reais |
| **Anonimização** | IDs sequenciais (CARDIO_0001-0500) sem correspondência com pessoas |
| **Base legal** | Pesquisa acadêmica (Art. 11, LGPD) |
| **Textos** | Baseados em publicações científicas de acesso aberto |
| **Imagens** | Provenientes de datasets públicos aprovados por comitês de ética |

### Análise de Viés

Identificamos e documentamos os seguintes vieses potenciais:

- **Viés de seleção**: Dataset com 55% homens / 45% mulheres — reflete epidemiologia, mas pode subrepresentar manifestações atípicas femininas
- **Viés étnico-racial**: Ausência de variável raça/etnia impede análise de disparidades raciais
- **Viés socioeconômico**: Variáveis como renda e escolaridade, que influenciam desfechos CV, não estão representadas
- **Viés de confusão**: Fatores comportamentais (dieta, exercício, álcool) não capturados

### Estratégias de Mitigação

1. Técnicas de balanceamento (SMOTE, undersampling)
2. Auditoria de equidade por subgrupo
3. Métricas de fairness (Equalized Odds, Demographic Parity)
4. Validação externa com datasets independentes
5. Explicabilidade de modelos (SHAP, LIME)

### Princípios Bioéticos

O projeto segue os 4 princípios fundamentais da bioética:
- **Beneficência**: Desenvolver soluções que melhorem o cuidado cardiovascular
- **Não-maleficência**: Garantir que vieses não causem dano a subgrupos
- **Autonomia**: O médico permanece como decisor final
- **Justiça**: Modelos devem funcionar equitativamente para todos

---

## Como Executar

### Pré-requisitos

```bash
# Python 3.10+
pip install -r requirements.txt
```

### Gerar o Dataset

```bash
python scripts/gerar_dataset.py
```

Saída esperada:
```
============================================================
  CARDIOIA - DATASET GERADO COM SUCESSO
============================================================
  [DADOS] Total de registros: 500
  [DADOS] Total de variaveis: 20
  [ALVO]  Distribuicao da variavel-alvo:
          Sem doenca cardiaca: 290 (58.0%)
          Com doenca cardiaca: 210 (42.0%)
============================================================
```

### Executar a Análise Exploratória (EDA)

```bash
python scripts/eda_cardio.py
```

O script produz 10 seções de análise:
1. Visão geral do dataset
2. Estatísticas descritivas
3. Distribuição de variáveis categóricas
4. Correlações com a variável-alvo
5. Comparação: pacientes com vs sem doença cardíaca
6. Detecção de outliers (método IQR)
7. Classificação de IMC (OMS)
8. Classificação de pressão arterial (Diretrizes Brasileiras)
9. Matriz de correlação (top 10 pares)
10. **Geração de 9 gráficos** (salvos em `figures/`)

### Visualizar o Dashboard Interativo

```bash
# Iniciar servidor local (necessário para carregar o CSV)
python -m http.server 8000

# Abrir no navegador:
# http://localhost:8000
```

---

## Links Públicos para os Dados

> ⚠️ **Nota para correção FIAP**: Todos os links abaixo são públicos e acessíveis para qualquer pessoa.

| Tipo de Dado | Formato | Quantidade | Link Público (Google Drive) | Link no Repositório |
|:---:|:---:|:---:|:---:|:---:|
| Dados Numéricos | CSV | 500 registros × 20 variáveis | [🔗 Google Drive](https://drive.google.com/drive/folders/12m6HMAOG698t0vBn6kGeKNU_aVWNo5Ry?usp=sharing) | [`data/cardio_dataset.csv`](data/cardio_dataset.csv) |
| Dados Textuais | TXT | 4 textos (~8.000 palavras) | [🔗 Google Drive](https://drive.google.com/drive/folders/1YORdOnraxeqBKunYGYGP64O-0ThYkxpt?usp=sharing) | [`docs/`](docs/) |
| Dados Visuais | JPG | 120 imagens ECG (3×40) | [🔗 Google Drive](https://drive.google.com/drive/folders/1D6pXrsmjo5gJzfLwCx31hHX0H86eZY2W?usp=sharing) | [`assets/ecg_images/`](assets/ecg_images/) |

---

## Referências Bibliográficas

### Dados Epidemiológicos e Clínicos

1. SOCIEDADE BRASILEIRA DE CARDIOLOGIA. Estatística Cardiovascular – Brasil. **Arquivos Brasileiros de Cardiologia**, 2023.
2. BARROSO, W. K. S. et al. Diretrizes Brasileiras de Hipertensão Arterial – 2020. **Arquivos Brasileiros de Cardiologia**, v. 116, n. 3, p. 516-658, 2021.
3. PRÉCOMA, D. B. et al. Atualização da Diretriz de Prevenção Cardiovascular da SBC. **Arquivos Brasileiros de Cardiologia**, v. 113, n. 4, p. 787-891, 2019.
4. DATASUS. Sistema de Informações sobre Mortalidade (SIM). **Ministério da Saúde**, Brasil.
5. PESQUISA NACIONAL DE SAÚDE (PNS). **IBGE/Ministério da Saúde**, 2019.
6. VIGITEL BRASIL. Vigilância de Fatores de Risco e Proteção para Doenças Crônicas. **Ministério da Saúde**, 2023.
7. YUSUF, S. et al. Effect of potentially modifiable risk factors associated with myocardial infarction in 52 countries (INTERHEART study). **The Lancet**, v. 364, n. 9438, p. 937-952, 2004.

### Inteligência Artificial em Cardiologia

8. TOPOL, E. J. High-performance medicine: the convergence of human and artificial intelligence. **Nature Medicine**, v. 25, n. 1, p. 44-56, 2019.
9. HANNUN, A. Y. et al. Cardiologist-level arrhythmia detection and classification in ambulatory electrocardiograms using a deep neural network. **Nature Medicine**, v. 25, n. 1, p. 65-69, 2019.
10. ATTIA, Z. I. et al. An artificial intelligence-enabled ECG algorithm for the identification of patients with atrial fibrillation during sinus rhythm. **The Lancet**, v. 394, n. 10201, p. 861-867, 2019.
11. JOHNSON, K. W. et al. Artificial Intelligence in Cardiology. **Journal of the American College of Cardiology**, v. 71, n. 23, p. 2668-2679, 2018.
12. OLIVEIRA, G. M. M. et al. Inteligência Artificial em Cardiologia: conceitos, ferramentas e desafios. **Arquivos Brasileiros de Cardiologia**, 2022.

### Datasets Utilizados

13. KHAN, A. H. et al. ECG Images dataset of Cardiac and COVID-19 Patients. **Data in Brief**, 2021.
14. UCI Machine Learning Repository. Heart Disease Dataset (Cleveland). Disponível em: <https://archive.ics.uci.edu/ml/datasets/Heart+Disease>.
15. PhysioNet. MIT-BIH Arrhythmia Database. Disponível em: <https://physionet.org/content/mitdb/1.0.0/>.

### Governança e Ética

16. BRASIL. Lei nº 13.709, de 14 de agosto de 2018. **Lei Geral de Proteção de Dados Pessoais (LGPD)**.
17. OBERMEYER, Z. et al. Dissecting racial bias in an algorithm used to manage the health of populations. **Science**, v. 366, n. 6464, p. 447-453, 2019.
18. WORLD HEALTH ORGANIZATION. Ethics and Governance of Artificial Intelligence for Health, 2021.

---

## Equipe

| Nome | RM | 
|------|:--:|
| Gabriela de Andrade Alves | RM567740 | 
| Leonardo de Mattos Oliveira | RM568219 | 

---

<div align="center">

**CardioIA** — Construindo as bases de uma cardiologia inteligente, ética e acessível.

*Projeto acadêmico desenvolvido para a disciplina de Inteligência Artificial — FIAP 2025*

</div>
