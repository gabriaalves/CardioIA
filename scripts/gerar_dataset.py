# ==============================================================================
# CardioIA - Fase 1: Gerador de Dataset Cardiológico Simulado
# ==============================================================================
# Este script gera um dataset simulado com 500 registros de pacientes cardíacos,
# utilizando distribuições estatísticas clinicamente realistas baseadas em dados
# epidemiológicos brasileiros (DATASUS, ABC Cardiol, SBC).
#
# As correlações entre variáveis são modeladas para refletir relações clínicas
# reais (ex: IMC ↔ pressão arterial, diabetes ↔ glicemia).
# ==============================================================================

import numpy as np
import pandas as pd
import os

np.random.seed(42)

N = 500

# --- 1. Identificação ---
patient_id = [f"CARDIO_{str(i).zfill(4)}" for i in range(1, N + 1)]

# --- 2. Dados Demográficos ---
# Idade: distribuição que reflete a população cardíaca (maior incidência 45-75 anos)
idade = np.clip(np.random.normal(loc=58, scale=14, size=N), 18, 95).astype(int)

# Sexo: ~55% masculino (maior prevalência cardiovascular em homens)
sexo = np.random.choice(["M", "F"], size=N, p=[0.55, 0.45])

# --- 3. Antropometria ---
# Peso e altura com diferenças por sexo (baseado em dados do IBGE)
peso_kg = np.where(
    sexo == "M",
    np.clip(np.random.normal(82, 15, N), 50, 160),
    np.clip(np.random.normal(70, 14, N), 40, 140)
).round(1)

altura_cm = np.where(
    sexo == "M",
    np.clip(np.random.normal(172, 7, N), 150, 200),
    np.clip(np.random.normal(160, 6.5, N), 140, 185)
).round(1)

# IMC calculado
imc = (peso_kg / ((altura_cm / 100) ** 2)).round(1)

# --- 4. Sinais Vitais ---
# Pressão arterial: correlacionada com idade e IMC
base_sistolica = 110 + (idade - 40) * 0.5 + (imc - 25) * 0.8
pressao_sistolica = np.clip(
    base_sistolica + np.random.normal(0, 12, N), 90, 200
).astype(int)

base_diastolica = 70 + (idade - 40) * 0.2 + (imc - 25) * 0.5
pressao_diastolica = np.clip(
    base_diastolica + np.random.normal(0, 8, N), 55, 130
).astype(int)

# Frequência cardíaca em repouso
frequencia_cardiaca_repouso = np.clip(
    np.random.normal(72, 12, N) + (idade - 50) * 0.1,
    45, 110
).astype(int)

# --- 5. Perfil Lipídico ---
# Colesterol total: correlacionado com idade e IMC
colesterol_total = np.clip(
    np.random.normal(200, 40, N) + (imc - 25) * 2 + (idade - 50) * 0.5,
    120, 380
).astype(int)

# LDL (~60-70% do colesterol total com variação)
colesterol_ldl = np.clip(
    colesterol_total * np.random.uniform(0.55, 0.70, N) + np.random.normal(0, 10, N),
    50, 250
).astype(int)

# HDL: inversamente correlacionado com IMC, menor em homens
colesterol_hdl = np.where(
    sexo == "M",
    np.clip(np.random.normal(42, 10, N) - (imc - 25) * 0.5, 20, 90),
    np.clip(np.random.normal(52, 12, N) - (imc - 25) * 0.4, 25, 100)
).astype(int)

# Triglicerídeos: correlacionados com IMC
triglicerides = np.clip(
    np.random.normal(150, 60, N) + (imc - 25) * 5,
    50, 500
).astype(int)

# --- 6. Glicemia ---
# Glicemia de jejum: correlacionada com IMC e idade
glicemia_jejum = np.clip(
    np.random.normal(95, 25, N) + (imc - 25) * 1.5 + (idade - 50) * 0.3,
    65, 300
).astype(int)

# --- 7. Fatores de Risco (Binários) ---
# Fumante: ~18% da população adulta brasileira, maior em homens
prob_fumante = np.where(sexo == "M", 0.22, 0.14)
fumante = np.random.binomial(1, prob_fumante)

# Diabetes: correlacionada com IMC, idade e glicemia
prob_diabetes_base = 0.08 + (imc - 25) * 0.01 + (idade - 50) * 0.003
prob_diabetes = np.clip(prob_diabetes_base, 0.03, 0.60)
# Ajustar: se glicemia > 126, alta probabilidade de diabetes
prob_diabetes = np.where(glicemia_jejum >= 126, np.clip(prob_diabetes + 0.5, 0, 1), prob_diabetes)
diabetes = np.random.binomial(1, prob_diabetes)

# Histórico familiar cardíaco: ~25-30% da população
historico_familiar_cardiaco = np.random.binomial(1, 0.28, N)

# --- 8. Tipo de Dor Torácica ---
# 0=Assintomático, 1=Angina típica, 2=Angina atípica, 3=Dor não-anginosa
tipo_dor_toracica = np.random.choice([0, 1, 2, 3], size=N, p=[0.35, 0.20, 0.25, 0.20])

# --- 9. Resultado ECG em Repouso ---
# 0=Normal, 1=Anormalidade ST-T, 2=Hipertrofia ventricular esquerda
resultado_ecg_repouso = np.random.choice([0, 1, 2], size=N, p=[0.50, 0.35, 0.15])

# --- 10. Variável Alvo: Diagnóstico de Doença Cardíaca ---
# Score de risco baseado em múltiplos fatores
score_risco = (
    (idade - 50) * 0.03 +
    (pressao_sistolica - 120) * 0.02 +
    (colesterol_total - 200) * 0.01 +
    (imc - 25) * 0.04 +
    fumante * 0.8 +
    diabetes * 0.7 +
    historico_familiar_cardiaco * 0.5 +
    (tipo_dor_toracica == 1).astype(int) * 0.6 +
    (resultado_ecg_repouso > 0).astype(int) * 0.4 +
    np.where(sexo == "M", 0.3, 0) +
    np.where(colesterol_hdl < 40, 0.4, 0) +
    np.random.normal(0, 0.5, N)
)

prob_doenca = 1 / (1 + np.exp(-score_risco + 2))
diagnostico_doenca_cardiaca = np.random.binomial(1, prob_doenca)

# --- Montar DataFrame ---
df = pd.DataFrame({
    "patient_id": patient_id,
    "idade": idade,
    "sexo": sexo,
    "peso_kg": peso_kg,
    "altura_cm": altura_cm,
    "imc": imc,
    "pressao_sistolica": pressao_sistolica,
    "pressao_diastolica": pressao_diastolica,
    "frequencia_cardiaca_repouso": frequencia_cardiaca_repouso,
    "colesterol_total": colesterol_total,
    "colesterol_ldl": colesterol_ldl,
    "colesterol_hdl": colesterol_hdl,
    "triglicerides": triglicerides,
    "glicemia_jejum": glicemia_jejum,
    "fumante": fumante,
    "diabetes": diabetes,
    "historico_familiar_cardiaco": historico_familiar_cardiaco,
    "tipo_dor_toracica": tipo_dor_toracica,
    "resultado_ecg_repouso": resultado_ecg_repouso,
    "diagnostico_doenca_cardiaca": diagnostico_doenca_cardiaca
})

# --- Salvar ---
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "cardio_dataset.csv")
df.to_csv(output_path, index=False, encoding="utf-8-sig")

# --- Estatísticas ---
print("=" * 60)
print("  CARDIOIA - DATASET GERADO COM SUCESSO")
print("=" * 60)
print(f"\n  [DADOS] Total de registros: {len(df)}")
print(f"  [DADOS] Total de variaveis: {len(df.columns)}")
print(f"  [SAVE]  Arquivo salvo em: {output_path}")
print(f"\n  [ALVO]  Distribuicao da variavel-alvo:")
print(f"          Sem doenca cardiaca: {(df['diagnostico_doenca_cardiaca'] == 0).sum()} ({(df['diagnostico_doenca_cardiaca'] == 0).mean()*100:.1f}%)")
print(f"          Com doenca cardiaca: {(df['diagnostico_doenca_cardiaca'] == 1).sum()} ({(df['diagnostico_doenca_cardiaca'] == 1).mean()*100:.1f}%)")
print(f"\n  [SEXO]  Distribuicao por sexo:")
print(f"          Masculino: {(df['sexo'] == 'M').sum()} ({(df['sexo'] == 'M').mean()*100:.1f}%)")
print(f"          Feminino:  {(df['sexo'] == 'F').sum()} ({(df['sexo'] == 'F').mean()*100:.1f}%)")
print(f"\n  [IDADE] Estatisticas de idade:")
print(f"          Media: {df['idade'].mean():.1f} | Mediana: {df['idade'].median():.1f} | Min: {df['idade'].min()} | Max: {df['idade'].max()}")
print(f"\n  [RISCO] Prevalencia de fatores de risco:")
print(f"          Fumantes:          {df['fumante'].mean()*100:.1f}%")
print(f"          Diabetes:          {df['diabetes'].mean()*100:.1f}%")
print(f"          Hist. familiar:    {df['historico_familiar_cardiaco'].mean()*100:.1f}%")
print("=" * 60)
