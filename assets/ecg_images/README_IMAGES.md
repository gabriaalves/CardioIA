# 🖼️ Imagens ECG — CardioIA

## Sobre as Imagens

Este diretório contém imagens de eletrocardiogramas (ECGs) de 12 derivações utilizadas no projeto CardioIA para fins de treinamento e avaliação de algoritmos de Visão Computacional.

---

## Fonte dos Dados

### Dataset Recomendado: ECG Images Dataset of Cardiac Patients

- **Fonte primária**: [ECG Images dataset of Cardiac and COVID-19 Patients](https://data.mendeley.com/datasets/gwbz3fsgp8/1) — Mendeley Data
- **Fonte alternativa (Kaggle)**: [ECG Images Dataset](https://www.kaggle.com/datasets/erhmrai/ecg-images-dataset-of-cardiac-patients)
- **Publicação**: Khan AH, et al. "ECG Images dataset of Cardiac and COVID-19 Patients." Data in Brief, 2021.
- **Licença**: CC BY 4.0 (Creative Commons Attribution 4.0 International)

### Outros Datasets Recomendados

| Dataset | Fonte | Nº de Imagens | Tipo |
|---------|-------|:---:|------|
| Cardiovascular ECG Images | [Kaggle](https://www.kaggle.com/datasets) | 1.000+ | ECG 12 derivações |
| PM-ECG-ID | [Zenodo](https://zenodo.org) | 6.000 | ECGs diversos |
| ECG Heartbeat (Image Version) | [Kaggle](https://www.kaggle.com/datasets/mohamedeldrkroury/ecg-heart-categorization-dataset-image-version) | 109.000+ | Sinais convertidos em imagens |
| NIH Chest X-ray | [NIH Box](https://nihcc.app.box.com/v/ChestXray-NIHCC) | 112.120 | Raio-X torácico |

---

## Instruções de Download

### Opção 1: Download Manual (Recomendado)

1. Acesse o dataset no Mendeley Data ou Kaggle (links acima)
2. Faça login (gratuito) se necessário
3. Baixe as imagens em formato `.jpg` ou `.png`
4. Organize em subpastas por categoria:
   ```
   ecg_images/
   ├── normal/          (mínimo 40 imagens)
   ├── infarto_miocardio/ (mínimo 40 imagens)
   └── arritmia/        (mínimo 40 imagens)
   ```

### Opção 2: Download via Kaggle API

```bash
# Instalar a API do Kaggle
pip install kaggle

# Configurar credenciais (~/.kaggle/kaggle.json)
# Baixar o dataset
kaggle datasets download -d erhmrai/ecg-images-dataset-of-cardiac-patients

# Descompactar
unzip ecg-images-dataset-of-cardiac-patients.zip -d ecg_images/
```

### Opção 3: Download via Script Python

```python
import os
import requests
from pathlib import Path

# Se estiver usando Kaggle API:
from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()
api.dataset_download_files(
    'erhmrai/ecg-images-dataset-of-cardiac-patients',
    path='./ecg_images/',
    unzip=True
)
```

---

## Organização Recomendada

Após o download, organize as imagens na seguinte estrutura:

```
ecg_images/
├── normal/
│   ├── ecg_normal_001.jpg
│   ├── ecg_normal_002.jpg
│   ├── ...
│   └── ecg_normal_040.jpg
│
├── infarto_miocardio/
│   ├── ecg_im_001.jpg
│   ├── ecg_im_002.jpg
│   ├── ...
│   └── ecg_im_040.jpg
│
├── arritmia/
│   ├── ecg_arr_001.jpg
│   ├── ecg_arr_002.jpg
│   ├── ...
│   └── ecg_arr_040.jpg
│
└── README_IMAGES.md   (este arquivo)
```

**Total mínimo: 120 imagens** (40 por categoria)

---

## Link para as Imagens (Armazenamento em Nuvem)

> ⚠️ **IMPORTANTE**: Após o download e organização das imagens, faça o upload para seu serviço de armazenamento e insira o link abaixo:

🔗 **Link público para as imagens ECG**: `[INSERIR_LINK_GOOGLE_DRIVE_OU_ONEDRIVE_AQUI]`

Garanta que o link esteja configurado como **público** (qualquer pessoa com o link pode acessar).

---

## Relevância para Visão Computacional

Essas imagens ECG serão utilizadas nas fases seguintes do projeto CardioIA para:

### Tarefas de Visão Computacional

| Tarefa | Descrição | Técnica |
|--------|-----------|---------|
| **Classificação de arritmias** | Identificar tipo de ritmo cardíaco a partir da imagem do ECG | CNN (ResNet, EfficientNet, VGG) |
| **Detecção de infarto** | Identificar padrões de supradesnivelamento de ST indicativos de infarto | Transfer Learning |
| **Segmentação de ondas** | Separar as ondas P, QRS e T do sinal eletrocardiográfico | U-Net, Segmentação Semântica |
| **Detecção de bordas** | Identificar contornos e formas das ondas cardíacas | Filtros Canny, Sobel |
| **Reconhecimento de anomalias** | Detectar padrões anormais em ECGs | Autoencoder, GAN |
| **Digitalização de ECGs** | Converter ECGs em papel para sinais digitais | OCR + CNN |

### Por que imagens ECG são importantes para IA em saúde?

1. **Prevalência**: O ECG é o exame cardiológico mais realizado mundialmente — são bilhões de registros disponíveis para análise
2. **Acessibilidade**: Equipamentos de ECG são relativamente baratos e amplamente disponíveis, inclusive em áreas remotas
3. **Diagnóstico rápido**: A análise automatizada pode reduzir o tempo de diagnóstico de minutos para segundos
4. **Triagem em massa**: IA pode realizar triagem de grandes volumes de ECGs, priorizando casos urgentes
5. **Telemedicina**: ECGs portáteis combinados com IA permitem diagnóstico remoto em áreas sem cardiologistas

---

## Considerações Éticas

- Todas as imagens provêm de datasets públicos aprovados por comitês de ética
- Os identificadores dos pacientes foram removidos (anonimização) nas fontes originais
- O uso é exclusivamente para fins acadêmicos e de pesquisa
- As imagens são distribuídas sob licença Creative Commons (CC BY 4.0)
