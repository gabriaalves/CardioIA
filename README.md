<div align="center">

# 🫀 CardioIA — A Nova Era da Cardiologia Inteligente

### Fase 1: Batimentos de Dados | Fase 2: Diagnóstico Automatizado

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-19-61dafb?style=for-the-badge&logo=react&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-8-646cff?style=for-the-badge&logo=vite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Fase%202%20Completa-success?style=for-the-badge)
![FIAP](https://img.shields.io/badge/FIAP-IA%202025-red?style=for-the-badge)

*Plataforma digital inteligente que simula o ecossistema de uma cardiologia moderna, integrando dados clínicos, Machine Learning, NLP, Visão Computacional e interface web responsiva.*

---

[Parte 1 – NLP](#parte-1--frases-de-sintomas--extração-de-informações) •
[Parte 2 – Classificador](#parte-2--classificador-básico-de-texto) •
[Ir Além 1 – Portal React](#ir-além-1--interface-do-cardioia-portal-react--vite) •
[Ir Além 2 – MLP ECG](#ir-além-2--diagnóstico-visual-com-rede-neural-mlp) •
[Fase 1](#fase-1--batimentos-de-dados)

</div>

---

## 📋 Sumário

- [Sobre o Projeto](#sobre-o-projeto)
- [Vídeo de Demonstração](#-vídeo-de-demonstração)
- [Estrutura do Repositório](#estrutura-do-repositório)
- **Fase 2 — Diagnóstico Automatizado**
  - [Parte 1 – Frases de Sintomas + Extração de Informações](#parte-1--frases-de-sintomas--extração-de-informações)
  - [Parte 2 – Classificador Básico de Texto](#parte-2--classificador-básico-de-texto)
  - [Ir Além 1 – Interface do CardioIA (Portal React + Vite)](#ir-além-1--interface-do-cardioia-portal-react--vite)
  - [Ir Além 2 – Diagnóstico Visual com Rede Neural MLP](#ir-além-2--diagnóstico-visual-com-rede-neural-mlp)
- [Fase 1 – Batimentos de Dados](#fase-1--batimentos-de-dados)
- [Como Executar](#como-executar)
- [Referências Bibliográficas](#referências-bibliográficas)
- [Equipe](#equipe)

---

## Sobre o Projeto

O **CardioIA** é um projeto acadêmico inovador do curso de Inteligência Artificial da FIAP, desenvolvido sob a metodologia PBL (Project Based Learning). O projeto simula o ecossistema completo de uma cardiologia inteligente, sendo desenvolvido ao longo de 7 fases.

### Fase 2 — Diagnóstico Automatizado: IA no Estetoscópio Digital

Nesta segunda fase, desenvolvemos um **módulo inteligente** capaz de:
- 📝 **Analisar relatos de pacientes** e extrair sintomas automaticamente
- 🔍 **Sugerir diagnósticos** com base em um mapa de conhecimento (ontologia)
- ⚕️ **Classificar nível de risco** (alto/baixo) usando TF-IDF e Machine Learning
- 🌐 **Portal web interativo** em React + Vite para visualização de dados
- 🧠 **Rede neural MLP** para classificação de sinais ECG

---

## 🎬 Vídeo de Demonstração

> 📹 **Link do vídeo (YouTube — não listado):** [INSERIR LINK DO VÍDEO AQUI]

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
│   ├── cardio_dataset.csv             # 📊 Dataset numérico da Fase 1 (500 registros)
│   ├── sintomas_pacientes.txt         # 📝 10 frases de sintomas de pacientes (Fase 2)
│   ├── mapa_conhecimento.csv          # 🗺️ Mapa sintomas → doenças (36 regras)
│   └── frases_risco.csv               # ⚠️ Base rotulada alto/baixo risco (40 frases)
│
├── docs/
│   ├── texto_01_estatistica_cardiovascular_brasil.txt
│   ├── texto_02_fatores_risco_doencas_cardiacas.txt
│   ├── texto_03_diretrizes_hipertensao_arterial.txt
│   └── texto_04_inteligencia_artificial_cardiologia.txt
│
├── scripts/
│   ├── gerar_dataset.py               # ⚙️ Gerador do dataset (Fase 1)
│   ├── eda_cardio.py                  # 📈 Análise Exploratória (Fase 1)
│   ├── extracao_diagnostico.py        # 🔍 Extração de sintomas + diagnóstico (Fase 2)
│   ├── classificador_risco.py         # 🤖 Classificador TF-IDF (Fase 2)
│   └── mlp_ecg_classifier.py          # 🧠 Rede Neural MLP para ECG (Fase 2)
│
├── figures/                           # 📊 Gráficos gerados (EDA + MLP)
│
├── cardioia-portal/                   # 🌐 Portal React + Vite (Ir Além 1)
│   ├── src/
│   │   ├── contexts/                  # Context API (AuthContext)
│   │   ├── components/                # Componentes (Sidebar, ProtectedRoute)
│   │   ├── services/                  # Serviço de API simulada
│   │   └── pages/                     # Páginas (Login, Dashboard, Pacientes, Agendamentos)
│   ├── package.json
│   └── vite.config.js
│
├── assets/ecg_images/                 # 🖼️ Imagens ECG (Fase 1)
├── dicionario_dados.md                # 📖 Dicionário de variáveis
├── governanca_dados.md                # 🛡️ Governança de dados
└── index.html                         # 🌐 Dashboard interativo (Fase 1)
```

---

## Parte 1 – Frases de Sintomas + Extração de Informações

### Descrição

Nesta parte, construímos um **sistema de extração de informações** que:
1. Lê 10 frases simuladas de relatos de pacientes
2. Identifica sintomas usando um mapa de conhecimento
3. Sugere diagnósticos com dois níveis de confiança

### Arquivo de Frases: [`data/sintomas_pacientes.txt`](data/sintomas_pacientes.txt)

Contém **10 frases completas** que simulam relatos reais de pacientes, incluindo:
- O que o paciente sente
- Quando os sintomas começaram
- Como afetam a rotina

Exemplos:
> *"Há dois dias estou com uma dor forte no peito que piora quando faço esforço físico, como subir escadas ou carregar compras, e melhora quando fico em repouso."*

> *"Sinto um cansaço constante há mais de uma semana, mesmo depois de dormir a noite inteira, e qualquer atividade simples como caminhar até a padaria me deixa completamente exausto."*

### Mapa de Conhecimento: [`data/mapa_conhecimento.csv`](data/mapa_conhecimento.csv)

Arquivo CSV com **36 regras** de associação entre sintomas e doenças:

| Sintoma 1 | Sintoma 2 | Doença Associada |
|-----------|-----------|------------------|
| dor no peito | esforço físico | Angina de Peito |
| aperto no tórax | pressão no peito | Infarto Agudo do Miocárdio |
| cansaço constante | fadiga | Insuficiência Cardíaca |
| falta de ar | dificuldade para respirar | Insuficiência Cardíaca |
| palpitações | coração dispara | Arritmia Cardíaca |
| inchaço nos tornozelos | pés inchados | Insuficiência Cardíaca Congestiva |
| dor de cabeça na nuca | visão embaçada | Hipertensão Arterial |
| ... | ... | ... |

> Total: 36 linhas cobrindo 16 doenças cardíacas diferentes.

### Código de Extração: [`scripts/extracao_diagnostico.py`](scripts/extracao_diagnostico.py)

O script realiza:
- **Normalização do texto** (minúsculas, remoção de pontuação)
- **Match completo** (ambos sintomas encontrados) → Confiança **ALTA** 🔴
- **Match parcial** (um sintoma encontrado) → Confiança **MODERADA** 🟡
- **Relatório formatado** para cada paciente

<<<<<<< HEAD
#### Resultado da Execução
=======
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
>>>>>>> 8e343b3ce9907d7eef50fcfceac7532f7e96f8a8

```
Total de frases analisadas:           10
Total de diagnósticos sugeridos:       20
Diagnósticos de alta confiança:        7
Diagnósticos de confiança moderada:    13
Regras no mapa de conhecimento:        36
```

<<<<<<< HEAD
=======
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

>>>>>>> 8e343b3ce9907d7eef50fcfceac7532f7e96f8a8
---

## Parte 2 – Classificador Básico de Texto

### Descrição

Desenvolvemos um **classificador de triagem clínica** que analisa frases com sintomas e classifica o nível de risco como **"alto risco"** ou **"baixo risco"**.

### Base de Dados: [`data/frases_risco.csv`](data/frases_risco.csv)

Contém **40 frases** médicas rotuladas:
- **20 frases** de alto risco (dor no peito intensa, falta de ar severa, etc.)
- **20 frases** de baixo risco (cansaço leve, dor muscular, etc.)

### Código do Classificador: [`scripts/classificador_risco.py`](scripts/classificador_risco.py)

O pipeline completo inclui:

1. **TF-IDF do zero** — Implementação manual sem dependências externas
   - Tokenização com remoção de stopwords em português
   - Cálculo de TF (Term Frequency) e IDF (Inverse Document Frequency)
   - Normalização L2 dos vetores

2. **Dois modelos de classificação** (implementados do zero):
   - **Regressão Logística** com gradiente descendente
   - **Árvore de Decisão** com critério de Gini

3. **Divisão estratificada** treino/teste (75/25)

4. **Métricas de avaliação**:
   - Acurácia, Precisão, Recall, F1-Score
   - Matriz de confusão

5. **Teste com frases novas** não vistas no treino

#### Resultados

| Modelo | Acurácia |
|--------|:--------:|
| Regressão Logística | 60% |
| **Árvore de Decisão** | **80%** |

O classificador demonstra corretamente a diferença entre frases de risco:
- 🔴 `"sinto uma dor muito forte no peito e estou suando frio"` → **ALTO RISCO**
- 🟢 `"tive uma leve dor nas costas depois de carregar peso"` → **BAIXO RISCO**

---

## Ir Além 1 – Interface do CardioIA (Portal React + Vite)

### Descrição

Portal web responsivo construído em **React 19 + Vite**, simulando a rotina de um portal de diagnóstico em cardiologia.

### Funcionalidades Implementadas

| Funcionalidade | Tecnologia | Status |
|---|---|:---:|
| Autenticação simulada | Context API + JWT fake no localStorage | ✅ |
| Listagem de pacientes | API fake com dados simulados | ✅ |
| Formulário de agendamento | `useState` + `useReducer` | ✅ |
| Dashboard com métricas | `useEffect` + API service | ✅ |
| Proteção de rotas | `AuthContext` + `ProtectedRoute` | ✅ |
| Estilização responsiva | CSS Modules | ✅ |
| Navegação SPA | React Router v6 | ✅ |

### Estrutura do Portal

```
cardioia-portal/src/
├── contexts/
│   └── AuthContext.jsx          # Context API com JWT fake
├── components/
│   ├── ProtectedRoute.jsx       # Proteção de rotas
│   ├── Sidebar.jsx              # Navegação lateral
│   └── Sidebar.module.css
├── services/
│   └── api.js                   # API fake (12 pacientes, consultas)
├── pages/
│   ├── LoginPage.jsx            # Tela de login
│   ├── DashboardPage.jsx        # Dashboard com métricas
│   ├── PacientesPage.jsx        # Listagem de pacientes
│   └── AgendamentosPage.jsx     # Agendamento de consultas
├── App.jsx                      # Roteamento principal
├── main.jsx                     # Entry point
└── index.css                    # Design system
```

### Hooks Utilizados

| Hook | Uso |
|------|-----|
| `useState` | Estado local em todas as páginas (busca, filtros, loading) |
| `useEffect` | Carregamento de dados da API, verificação de token |
| `useContext` | Autenticação via `AuthContext` em toda a aplicação |
| `useReducer` | Gerenciamento do formulário de agendamento |

### Credenciais de Acesso

| Email | Senha | Perfil |
|-------|-------|--------|
| `ricardo@cardioia.com` | `123456` | Dr. Ricardo Mendes — Cardiologia |
| `maria@cardioia.com` | `123456` | Enf. Maria Santos — Enfermagem |

---

## Ir Além 2 – Diagnóstico Visual com Rede Neural MLP

### Descrição

Implementação de uma **Rede Neural Artificial (MLP)** para classificar sinais de ECG em **Normal** vs **Anormal**.

### Código: [`scripts/mlp_ecg_classifier.py`](scripts/mlp_ecg_classifier.py)

### Arquitetura da Rede

```
Input (187) → Dense(128, ReLU) → Dense(64, ReLU) → Dense(1, Sigmoid)
```

| Parâmetro | Valor |
|-----------|-------|
| Camadas ocultas | 2 (128 + 64 neurônios) |
| Ativação | ReLU (ocultas) + Sigmoid (saída) |
| Otimizador | Mini-batch SGD com Momentum (0.9) |
| Learning Rate | 0.001 |
| Épocas | 50 |
| Batch Size | 32 |
| Loss Function | Binary Cross-Entropy |
| Inicialização | He (para ReLU) |

### Dataset

- **Recomendado**: [MIT-BIH Heartbeat (Kaggle)](https://www.kaggle.com/datasets/shayanfazeli/heartbeat)
- **Fallback**: Dados simulados (4000 treino + 1000 teste) com ondas ECG geradas matematicamente

### Pipeline Completo

1. **Carregamento** dos dados (Kaggle ou simulados)
2. **Pré-processamento**: Normalização Z-score
3. **Divisão**: Treino (80%) / Validação (20%) / Teste
4. **Treinamento**: 50 épocas com mini-batch + momentum
5. **Avaliação**: Acurácia, Precisão, Recall, F1-Score, Matriz de Confusão
6. **Visualização**: Curvas de loss/acurácia + exemplos de ECG

### Resultados (Dados Simulados)

| Métrica | Valor |
|---------|:-----:|
| Acurácia | 100% |
| Precisão | 1.00 |
| Recall | 1.00 |
| F1-Score | 1.00 |

> ⚠️ A acurácia de 100% é esperada com dados simulados, pois os padrões são matematicamente distintos. Com dados reais (MIT-BIH), espera-se acurácia de ~85-95%.

### Gráficos Gerados

- `figures/mlp_curvas_treinamento.png` — Curvas de Loss e Acurácia
- `figures/mlp_exemplos_ecg.png` — Exemplos de ECGs classificados

---

## Fase 1 – Batimentos de Dados

A documentação completa da Fase 1 inclui:

- **Dados Numéricos (IoT)**: Dataset com 500 registros e 20 variáveis clínicas ([`data/cardio_dataset.csv`](data/cardio_dataset.csv))
- **Dados Textuais (NLP)**: 4 textos científicos sobre cardiologia ([`docs/`](docs/))
- **Dados Visuais (VC)**: 120+ imagens de ECG ([`assets/ecg_images/`](assets/ecg_images/))
- **Governança de Dados**: LGPD, análise de viés e princípios bioéticos ([`governanca_dados.md`](governanca_dados.md))

> Para detalhes completos da Fase 1, consulte o [dicionário de dados](dicionario_dados.md) e o [documento de governança](governanca_dados.md).

---

## Como Executar

### Pré-requisitos

```bash
# Python 3.10+
pip install -r requirements.txt

# Node.js 18+ (para o portal React)
cd cardioia-portal && npm install
```

### Parte 1 — Extração de Diagnósticos

```bash
python scripts/extracao_diagnostico.py
```

### Parte 2 — Classificador de Risco

```bash
python scripts/classificador_risco.py
```

### Ir Além 1 — Portal React

```bash
cd cardioia-portal
npm run dev
# Acesse http://localhost:5173
```

### Ir Além 2 — MLP ECG

```bash
# Com dados simulados (automático):
python scripts/mlp_ecg_classifier.py

# Com dados reais (baixar do Kaggle primeiro):
# Coloque mitbih_train.csv e mitbih_test.csv em data/
python scripts/mlp_ecg_classifier.py
```

<<<<<<< HEAD
> ⚠️ **Nota para Windows**: Se encontrar erros de encoding, use: `$env:PYTHONUTF8="1"` antes dos comandos Python.
=======
| Tipo de Dado | Formato | Quantidade | Link Público (Google Drive) | Link no Repositório |
|:---:|:---:|:---:|:---:|:---:|
| Dados Numéricos | CSV | 500 registros × 20 variáveis | [🔗 Google Drive](https://drive.google.com/drive/folders/12m6HMAOG698t0vBn6kGeKNU_aVWNo5Ry?usp=sharing) | [`data/cardio_dataset.csv`](data/cardio_dataset.csv) |
| Dados Textuais | TXT | 4 textos (~8.000 palavras) | [🔗 Google Drive](https://drive.google.com/drive/folders/1YORdOnraxeqBKunYGYGP64O-0ThYkxpt?usp=sharing) | [`docs/`](docs/) |
| Dados Visuais | JPG | 120 imagens ECG (3×40) | [🔗 Google Drive](https://drive.google.com/drive/folders/1D6pXrsmjo5gJzfLwCx31hHX0H86eZY2W?usp=sharing) | [`assets/ecg_images/`](assets/ecg_images/) |
>>>>>>> 8e343b3ce9907d7eef50fcfceac7532f7e96f8a8

---

## Referências Bibliográficas

### Fase 2 — NLP e Machine Learning

1. JURAFSKY, D.; MARTIN, J. H. *Speech and Language Processing*. 3rd ed. Stanford University, 2023.
2. MANNING, C. D. et al. *Introduction to Information Retrieval*. Cambridge University Press, 2008.
3. PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. *JMLR*, v. 12, p. 2825-2830, 2011.
4. RAJKOMAR, A. et al. Machine Learning in Medicine. *NEJM*, v. 380, n. 14, p. 1347-1358, 2019.
5. GOODFELLOW, I.; BENGIO, Y.; COURVILLE, A. *Deep Learning*. MIT Press, 2016.

### Fase 1 — Dados e Governança

6. SOCIEDADE BRASILEIRA DE CARDIOLOGIA. Estatística Cardiovascular – Brasil. *ABC Cardiol*, 2023.
7. BARROSO, W. K. S. et al. Diretrizes Brasileiras de Hipertensão Arterial – 2020. *ABC Cardiol*, v. 116, 2021.
8. HANNUN, A. Y. et al. Cardiologist-level arrhythmia detection using a deep neural network. *Nature Medicine*, v. 25, 2019.
9. BRASIL. Lei nº 13.709/2018. *LGPD*.
10. OBERMEYER, Z. et al. Dissecting racial bias in an algorithm. *Science*, v. 366, 2019.

### Datasets

11. KACHUEE, M. et al. ECG Heartbeat Classification: A Deep Transferable Representation. *arXiv*, 2018.
12. KHAN, A. H. et al. ECG Images dataset of Cardiac and COVID-19 Patients. *Data in Brief*, 2021.

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
