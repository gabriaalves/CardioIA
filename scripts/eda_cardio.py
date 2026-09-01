# ==============================================================================
# CardioIA - Fase 1: Analise Exploratoria de Dados (EDA)
# ==============================================================================
# Este script realiza uma analise exploratoria completa do dataset cardiologico
# gerado, incluindo estatisticas descritivas, distribuicoes, correlacoes,
# deteccao de outliers e analises bivariadas.
# ==============================================================================

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Backend nao-interativo para salvar graficos
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Configuracao ---
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "..", "data", "cardio_dataset.csv")
df = pd.read_csv(data_path)

print("=" * 70)
print("  CARDIOIA - ANALISE EXPLORATORIA DE DADOS (EDA)")
print("=" * 70)

# --- 1. Visao Geral ---
print("\n" + "-" * 70)
print("  1. VISAO GERAL DO DATASET")
print("-" * 70)
print(f"\n  Dimensoes: {df.shape[0]} linhas x {df.shape[1]} colunas")
print(f"\n  Colunas:")
for i, col in enumerate(df.columns, 1):
    print(f"    {i:2d}. {col} ({df[col].dtype})")

print(f"\n  Valores ausentes (missing values):")
missing = df.isnull().sum()
if missing.sum() == 0:
    print("    Nenhum valor ausente encontrado! Dataset completo.")
else:
    for col in missing[missing > 0].index:
        print(f"    {col}: {missing[col]} ({missing[col]/len(df)*100:.1f}%)")

# --- 2. Estatisticas Descritivas ---
print("\n" + "-" * 70)
print("  2. ESTATISTICAS DESCRITIVAS - VARIAVEIS NUMERICAS")
print("-" * 70)

numeric_cols = ['idade', 'peso_kg', 'altura_cm', 'imc', 'pressao_sistolica',
                'pressao_diastolica', 'frequencia_cardiaca_repouso',
                'colesterol_total', 'colesterol_ldl', 'colesterol_hdl',
                'triglicerides', 'glicemia_jejum']

stats = df[numeric_cols].describe().T
stats['mediana'] = df[numeric_cols].median()
stats['cv(%)'] = (stats['std'] / stats['mean'] * 100).round(1)

print(f"\n  {'Variavel':<32} {'Media':>8} {'Mediana':>8} {'DP':>8} {'Min':>6} {'Max':>6} {'CV(%)':>7}")
print("  " + "-" * 85)
for col in numeric_cols:
    s = stats.loc[col]
    print(f"  {col:<32} {s['mean']:>8.1f} {s['mediana']:>8.1f} {s['std']:>8.1f} {s['min']:>6.0f} {s['max']:>6.0f} {s['cv(%)']:>7.1f}")

# --- 3. Distribuicao de Variaveis Categoricas ---
print("\n" + "-" * 70)
print("  3. DISTRIBUICAO DE VARIAVEIS CATEGORICAS/BINARIAS")
print("-" * 70)

# Sexo
print(f"\n  Sexo:")
for val, count in df['sexo'].value_counts().items():
    print(f"    {val}: {count} ({count/len(df)*100:.1f}%)")

# Fumante
print(f"\n  Fumante:")
for val in [0, 1]:
    count = (df['fumante'] == val).sum()
    label = "Nao" if val == 0 else "Sim"
    print(f"    {label}: {count} ({count/len(df)*100:.1f}%)")

# Diabetes
print(f"\n  Diabetes:")
for val in [0, 1]:
    count = (df['diabetes'] == val).sum()
    label = "Nao" if val == 0 else "Sim"
    print(f"    {label}: {count} ({count/len(df)*100:.1f}%)")

# Historico familiar
print(f"\n  Historico Familiar Cardiaco:")
for val in [0, 1]:
    count = (df['historico_familiar_cardiaco'] == val).sum()
    label = "Nao" if val == 0 else "Sim"
    print(f"    {label}: {count} ({count/len(df)*100:.1f}%)")

# Tipo dor toracica
print(f"\n  Tipo de Dor Toracica:")
labels_dor = {0: "Assintomatico", 1: "Angina tipica", 2: "Angina atipica", 3: "Dor nao-anginosa"}
for val in [0, 1, 2, 3]:
    count = (df['tipo_dor_toracica'] == val).sum()
    print(f"    {val} ({labels_dor[val]}): {count} ({count/len(df)*100:.1f}%)")

# ECG repouso
print(f"\n  Resultado ECG em Repouso:")
labels_ecg = {0: "Normal", 1: "Anormalidade ST-T", 2: "Hipertrofia VE"}
for val in [0, 1, 2]:
    count = (df['resultado_ecg_repouso'] == val).sum()
    print(f"    {val} ({labels_ecg[val]}): {count} ({count/len(df)*100:.1f}%)")

# Variavel alvo
print(f"\n  Diagnostico Doenca Cardiaca (variavel-alvo):")
for val in [0, 1]:
    count = (df['diagnostico_doenca_cardiaca'] == val).sum()
    label = "Sem doenca" if val == 0 else "Com doenca"
    print(f"    {val} ({label}): {count} ({count/len(df)*100:.1f}%)")

# --- 4. Analise de Correlacoes ---
print("\n" + "-" * 70)
print("  4. TOP 15 CORRELACOES COM A VARIAVEL-ALVO")
print("-" * 70)

# Calcular correlacoes com a variavel alvo
corr_target = df[numeric_cols + ['fumante', 'diabetes', 'historico_familiar_cardiaco',
                                  'tipo_dor_toracica', 'resultado_ecg_repouso',
                                  'diagnostico_doenca_cardiaca']].corr()['diagnostico_doenca_cardiaca']
corr_target = corr_target.drop('diagnostico_doenca_cardiaca').sort_values(ascending=False)

print(f"\n  {'Variavel':<35} {'Correlacao':>12} {'Direcao':<12}")
print("  " + "-" * 60)
for col, val in corr_target.items():
    direction = "POSITIVA" if val > 0 else "NEGATIVA"
    strength = "forte" if abs(val) > 0.3 else "moderada" if abs(val) > 0.15 else "fraca"
    print(f"  {col:<35} {val:>12.4f} {direction} ({strength})")

# --- 5. Analise Bivariada: Comparacao entre grupos ---
print("\n" + "-" * 70)
print("  5. COMPARACAO: PACIENTES COM vs SEM DOENCA CARDIACA")
print("-" * 70)

for col in numeric_cols:
    mean_0 = df[df['diagnostico_doenca_cardiaca'] == 0][col].mean()
    mean_1 = df[df['diagnostico_doenca_cardiaca'] == 1][col].mean()
    diff_pct = ((mean_1 - mean_0) / mean_0) * 100
    print(f"  {col:<32} Sem DC: {mean_0:>8.1f}  |  Com DC: {mean_1:>8.1f}  |  Diff: {diff_pct:>+6.1f}%")

# --- 6. Deteccao de Outliers (IQR) ---
print("\n" + "-" * 70)
print("  6. DETECCAO DE OUTLIERS (METODO IQR)")
print("-" * 70)

print(f"\n  {'Variavel':<32} {'Outliers':>10} {'% do Total':>12}")
print("  " + "-" * 55)
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = ((df[col] < lower) | (df[col] > upper)).sum()
    print(f"  {col:<32} {outliers:>10} {outliers/len(df)*100:>11.1f}%")

# --- 7. Classificacao de IMC ---
print("\n" + "-" * 70)
print("  7. CLASSIFICACAO DE IMC (OMS)")
print("-" * 70)

bins = [0, 18.5, 25, 30, 35, 40, 100]
labels = ['Baixo peso (<18.5)', 'Normal (18.5-24.9)', 'Sobrepeso (25-29.9)',
          'Obesidade I (30-34.9)', 'Obesidade II (35-39.9)', 'Obesidade III (>=40)']
df['imc_classe'] = pd.cut(df['imc'], bins=bins, labels=labels)

print(f"\n  {'Classe IMC':<28} {'N':>6} {'%':>8} {'% DC':>8}")
print("  " + "-" * 55)
for classe in labels:
    mask = df['imc_classe'] == classe
    n = mask.sum()
    pct = n / len(df) * 100
    pct_dc = df[mask]['diagnostico_doenca_cardiaca'].mean() * 100 if n > 0 else 0
    print(f"  {classe:<28} {n:>6} {pct:>7.1f}% {pct_dc:>7.1f}%")

# --- 8. Classificacao de Pressao Arterial ---
print("\n" + "-" * 70)
print("  8. CLASSIFICACAO DE PRESSAO ARTERIAL (Diretrizes Brasileiras)")
print("-" * 70)

def classificar_pa(row):
    """Classifica PA conforme Diretrizes Brasileiras de Hipertensao Arterial (2020).
    Utiliza o maior estagio entre sistolica e diastolica."""
    s = row['pressao_sistolica']
    d = row['pressao_diastolica']

    # Classificar sistolica
    if s < 120:
        cls_s = 0  # Otima
    elif s <= 129:
        cls_s = 1  # Normal
    elif s <= 139:
        cls_s = 2  # Pre-hipertensao
    elif s <= 159:
        cls_s = 3  # HAS Estagio 1
    elif s <= 179:
        cls_s = 4  # HAS Estagio 2
    else:
        cls_s = 5  # HAS Estagio 3

    # Classificar diastolica
    if d < 80:
        cls_d = 0
    elif d <= 84:
        cls_d = 1
    elif d <= 89:
        cls_d = 2
    elif d <= 99:
        cls_d = 3
    elif d <= 109:
        cls_d = 4
    else:
        cls_d = 5

    # Usar o maior estagio (Diretrizes Brasileiras de Hipertensao)
    nivel = max(cls_s, cls_d)
    niveis = ['Otima', 'Normal', 'Pre-hipertensao', 'HAS Estagio 1', 'HAS Estagio 2', 'HAS Estagio 3']
    return niveis[nivel]

df['pa_classe'] = df.apply(classificar_pa, axis=1)
pa_order = ['Otima', 'Normal', 'Pre-hipertensao', 'HAS Estagio 1', 'HAS Estagio 2', 'HAS Estagio 3']

print(f"\n  {'Classe PA':<22} {'N':>6} {'%':>8} {'% DC':>8}")
print("  " + "-" * 48)
for classe in pa_order:
    mask = df['pa_classe'] == classe
    n = mask.sum()
    if n > 0:
        pct = n / len(df) * 100
        pct_dc = df[mask]['diagnostico_doenca_cardiaca'].mean() * 100
        print(f"  {classe:<22} {n:>6} {pct:>7.1f}% {pct_dc:>7.1f}%")

# --- 9. Matriz de Correlacao Completa ---
print("\n" + "-" * 70)
print("  9. MATRIZ DE CORRELACAO (TOP 10 PARES MAIS CORRELACIONADOS)")
print("-" * 70)

all_numeric = numeric_cols + ['fumante', 'diabetes', 'historico_familiar_cardiaco',
                               'diagnostico_doenca_cardiaca']
corr_matrix = df[all_numeric].corr()

# Extrair pares unicos
pairs = []
for i in range(len(all_numeric)):
    for j in range(i+1, len(all_numeric)):
        pairs.append((all_numeric[i], all_numeric[j], corr_matrix.iloc[i, j]))

pairs_sorted = sorted(pairs, key=lambda x: abs(x[2]), reverse=True)

print(f"\n  {'Variavel 1':<30} {'Variavel 2':<30} {'Corr':>8}")
print("  " + "-" * 70)
for v1, v2, corr in pairs_sorted[:10]:
    print(f"  {v1:<30} {v2:<30} {corr:>8.4f}")

# --- Resumo Final ---
print("\n" + "=" * 70)
print("  RESUMO FINAL DA EDA")
print("=" * 70)
print(f"""
  Dataset: {df.shape[0]} registros, {df.shape[1]} variaveis
  Valores ausentes: 0
  Prevalencia de DC: {df['diagnostico_doenca_cardiaca'].mean()*100:.1f}%

  Insights principais:
  - {corr_target.index[0]} tem a maior correlacao positiva com DC
  - {corr_target.index[-1]} tem a maior correlacao negativa com DC
  - {(df['pressao_sistolica'] >= 140).mean()*100:.1f}% dos pacientes sao hipertensos (PA >= 140)
  - {(df['imc'] >= 30).mean()*100:.1f}% dos pacientes sao obesos (IMC >= 30)
  - {df['fumante'].mean()*100:.1f}% sao fumantes
  - {df['diabetes'].mean()*100:.1f}% tem diabetes
""")

# ==============================================================================
# 10. GERACAO DE GRAFICOS (salvos em figures/)
# ==============================================================================
print("-" * 70)
print("  10. GERANDO GRAFICOS...")
print("-" * 70)

figures_dir = os.path.join(os.path.dirname(script_dir), "figures")
os.makedirs(figures_dir, exist_ok=True)

# Configuracao global de estilo
sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['savefig.bbox'] = 'tight'

# --- Grafico 1: Distribuicao da variavel-alvo ---
fig, ax = plt.subplots(figsize=(8, 5))
colors_target = ['#2ecc71', '#e74c3c']
counts_target = df['diagnostico_doenca_cardiaca'].value_counts().sort_index()
ax.bar(['Sem Doenca (0)', 'Com Doenca (1)'], counts_target.values, color=colors_target, edgecolor='white', linewidth=1.5)
for i, v in enumerate(counts_target.values):
    ax.text(i, v + 5, f'{v} ({v/len(df)*100:.1f}%)', ha='center', fontweight='bold', fontsize=12)
ax.set_title('Distribuicao da Variavel-Alvo (Diagnostico de Doenca Cardiaca)', fontweight='bold', fontsize=14)
ax.set_ylabel('Numero de Pacientes')
plt.savefig(os.path.join(figures_dir, '01_distribuicao_variavel_alvo.png'))
plt.close()
print("  [OK] 01_distribuicao_variavel_alvo.png")

# --- Grafico 2: Histograma de Idade por diagnostico ---
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df[df['diagnostico_doenca_cardiaca']==0]['idade'], bins=20, alpha=0.6, label='Sem DC', color='#3498db', edgecolor='white')
ax.hist(df[df['diagnostico_doenca_cardiaca']==1]['idade'], bins=20, alpha=0.6, label='Com DC', color='#e74c3c', edgecolor='white')
ax.set_title('Distribuicao de Idade por Diagnostico', fontweight='bold', fontsize=14)
ax.set_xlabel('Idade (anos)')
ax.set_ylabel('Frequencia')
ax.legend()
plt.savefig(os.path.join(figures_dir, '02_histograma_idade_diagnostico.png'))
plt.close()
print("  [OK] 02_histograma_idade_diagnostico.png")

# --- Grafico 3: Heatmap de Correlacao ---
fig, ax = plt.subplots(figsize=(14, 10))
corr_cols = numeric_cols + ['fumante', 'diabetes', 'historico_familiar_cardiaco', 'diagnostico_doenca_cardiaca']
corr_full = df[corr_cols].corr()
mask = np.triu(np.ones_like(corr_full, dtype=bool))
sns.heatmap(corr_full, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            square=True, linewidths=0.5, ax=ax, vmin=-1, vmax=1,
            cbar_kws={'shrink': 0.8, 'label': 'Correlacao de Pearson'})
ax.set_title('Matriz de Correlacao - Variaveis Clinicas', fontweight='bold', fontsize=14, pad=20)
plt.savefig(os.path.join(figures_dir, '03_heatmap_correlacao.png'))
plt.close()
print("  [OK] 03_heatmap_correlacao.png")

# --- Grafico 4: Boxplots de variaveis por diagnostico ---
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
boxplot_vars = ['idade', 'pressao_sistolica', 'colesterol_total', 'imc', 'glicemia_jejum', 'frequencia_cardiaca_repouso']
for idx, var in enumerate(boxplot_vars):
    ax = axes[idx // 3, idx % 3]
    df.boxplot(column=var, by='diagnostico_doenca_cardiaca', ax=ax,
              boxprops=dict(color='#2c3e50'), medianprops=dict(color='#e74c3c', linewidth=2),
              whiskerprops=dict(color='#2c3e50'), capprops=dict(color='#2c3e50'))
    ax.set_title(var.replace('_', ' ').title(), fontweight='bold')
    ax.set_xlabel('Diagnostico DC (0=Sem, 1=Com)')
    ax.set_ylabel('')
fig.suptitle('Comparacao de Variaveis: Pacientes Com vs Sem Doenca Cardiaca', fontweight='bold', fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(figures_dir, '04_boxplots_comparacao.png'))
plt.close()
print("  [OK] 04_boxplots_comparacao.png")

# --- Grafico 5: Distribuicao de IMC por classe ---
fig, ax = plt.subplots(figsize=(10, 6))
imc_colors = ['#3498db', '#2ecc71', '#f39c12', '#e67e22', '#e74c3c', '#c0392b']
imc_counts_plot = df['imc_classe'].value_counts().reindex(labels)
ax.bar(range(len(labels)), imc_counts_plot.values, color=imc_colors, edgecolor='white', linewidth=1.5)
ax.set_xticks(range(len(labels)))
ax.set_xticklabels([l.split('(')[0].strip() for l in labels], rotation=30, ha='right')
for i, v in enumerate(imc_counts_plot.values):
    ax.text(i, v + 2, str(v), ha='center', fontweight='bold')
ax.set_title('Classificacao de IMC (OMS)', fontweight='bold', fontsize=14)
ax.set_ylabel('Numero de Pacientes')
plt.savefig(os.path.join(figures_dir, '05_classificacao_imc.png'))
plt.close()
print("  [OK] 05_classificacao_imc.png")

# --- Grafico 6: Prevalencia de DC por classe IMC ---
fig, ax = plt.subplots(figsize=(10, 6))
dc_by_imc = []
for classe in labels:
    mask_imc = df['imc_classe'] == classe
    n = mask_imc.sum()
    if n > 0:
        dc_by_imc.append(df[mask_imc]['diagnostico_doenca_cardiaca'].mean() * 100)
    else:
        dc_by_imc.append(0)
ax.plot(range(len(labels)), dc_by_imc, 'o-', color='#e74c3c', linewidth=2.5, markersize=10, markerfacecolor='white', markeredgewidth=2.5)
ax.fill_between(range(len(labels)), dc_by_imc, alpha=0.1, color='#e74c3c')
ax.set_xticks(range(len(labels)))
ax.set_xticklabels([l.split('(')[0].strip() for l in labels], rotation=30, ha='right')
for i, v in enumerate(dc_by_imc):
    ax.text(i, v + 1.5, f'{v:.1f}%', ha='center', fontweight='bold', fontsize=10)
ax.set_title('Prevalencia de Doenca Cardiaca por Classe de IMC', fontweight='bold', fontsize=14)
ax.set_ylabel('Prevalencia DC (%)')
plt.savefig(os.path.join(figures_dir, '06_prevalencia_dc_por_imc.png'))
plt.close()
print("  [OK] 06_prevalencia_dc_por_imc.png")

# --- Grafico 7: Scatter idade vs pressao sistolica ---
fig, ax = plt.subplots(figsize=(10, 7))
colors_scatter = df['diagnostico_doenca_cardiaca'].map({0: '#3498db', 1: '#e74c3c'})
ax.scatter(df['idade'], df['pressao_sistolica'], c=colors_scatter, alpha=0.5, edgecolors='white', linewidth=0.5, s=40)
ax.set_xlabel('Idade (anos)', fontsize=12)
ax.set_ylabel('Pressao Sistolica (mmHg)', fontsize=12)
ax.set_title('Idade vs Pressao Sistolica por Diagnostico', fontweight='bold', fontsize=14)
ax.axhline(y=140, color='#e74c3c', linestyle='--', alpha=0.5, label='Limiar Hipertensao (140 mmHg)')
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#3498db', label='Sem DC'), Patch(facecolor='#e74c3c', label='Com DC')]
ax.legend(handles=legend_elements, loc='upper left')
plt.savefig(os.path.join(figures_dir, '07_scatter_idade_pressao.png'))
plt.close()
print("  [OK] 07_scatter_idade_pressao.png")

# --- Grafico 8: Distribuicao de fatores de risco ---
fig, ax = plt.subplots(figsize=(10, 6))
fatores = ['Fumante', 'Diabetes', 'Hist. Familiar', 'Hipertensao\n(PA>=140)', 'Obesidade\n(IMC>=30)']
prev = [
    df['fumante'].mean()*100,
    df['diabetes'].mean()*100,
    df['historico_familiar_cardiaco'].mean()*100,
    (df['pressao_sistolica'] >= 140).mean()*100,
    (df['imc'] >= 30).mean()*100
]
bar_colors = ['#e74c3c', '#e67e22', '#9b59b6', '#3498db', '#f39c12']
bars = ax.barh(fatores, prev, color=bar_colors, edgecolor='white', linewidth=1.5, height=0.6)
for bar, p in zip(bars, prev):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, f'{p:.1f}%', va='center', fontweight='bold', fontsize=11)
ax.set_xlabel('Prevalencia (%)')
ax.set_title('Prevalencia de Fatores de Risco Cardiovascular', fontweight='bold', fontsize=14)
ax.invert_yaxis()
plt.savefig(os.path.join(figures_dir, '08_prevalencia_fatores_risco.png'))
plt.close()
print("  [OK] 08_prevalencia_fatores_risco.png")

# --- Grafico 9: Distribuicao por sexo e diagnostico ---
fig, ax = plt.subplots(figsize=(8, 5))
sexo_dc = df.groupby(['sexo', 'diagnostico_doenca_cardiaca']).size().unstack(fill_value=0)
sexo_dc.plot(kind='bar', ax=ax, color=['#3498db', '#e74c3c'], edgecolor='white', linewidth=1.5)
ax.set_title('Distribuicao por Sexo e Diagnostico', fontweight='bold', fontsize=14)
ax.set_xlabel('Sexo')
ax.set_ylabel('Numero de Pacientes')
ax.legend(['Sem DC', 'Com DC'])
ax.set_xticklabels(['Feminino', 'Masculino'], rotation=0)
plt.savefig(os.path.join(figures_dir, '09_sexo_diagnostico.png'))
plt.close()
print("  [OK] 09_sexo_diagnostico.png")

print(f"\n  [SAVE] Todos os graficos salvos em: {figures_dir}")

print("\n" + "=" * 70)
print("  EDA concluida com sucesso!")
print("=" * 70)
