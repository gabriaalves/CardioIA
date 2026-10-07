# -*- coding: utf-8 -*-
"""
CardioIA - Fase 2 | Parte 2: Classificador de Texto para Triagem Clínica
========================================================================

Este módulo realiza:
1. Carregamento e análise exploratória da base rotulada de frases (alto/baixo risco)
2. Vetorização de texto utilizando TF-IDF (Scikit-Learn e implementação de referência)
3. Treinamento comparativo de modelos de Machine Learning:
   - Regressão Logística (Scikit-Learn)
   - Árvore de Decisão (Scikit-Learn)
4. Avaliação completa de desempenho:
   - Acurácia, Precisão, Sensibilidade (Recall), F1-Score
   - Matrizes de Confusão gráficas salvas em figures/
   - Identificação dos termos mais preditivos (features mais informativas)
5. Teste clínico com frases inéditas (triagem automatizada)
6. Análise de Vieses, Falhas e Governança em IA aplicada à Saúde

Autores: Gabriela de Andrade Alves (RM567740), Leonardo de Mattos Oliveira (RM568219)
Curso: Inteligência Artificial - FIAP 2025
"""

import os
import sys
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Garante suporte a UTF-8 em terminais Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Scikit-Learn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

# ============================================================================
# CONFIGURAÇÕES DE CAMINHOS
# ============================================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

ARQUIVO_FRASES_RISCO = os.path.join(DATA_DIR, "frases_risco.csv")

# Stopwords personalizadas em português para o domínio clínico
STOPWORDS_PT = [
    'a', 'o', 'e', 'é', 'de', 'do', 'da', 'em', 'um', 'uma', 'para',
    'com', 'no', 'na', 'que', 'os', 'as', 'dos', 'das', 'por', 'ao',
    'se', 'ou', 'mas', 'como', 'já', 'eu', 'ele', 'ela', 'nos', 'não',
    'mais', 'muito', 'há', 'me', 'meu', 'minha', 'seu', 'sua', 'ter',
    'ser', 'ir', 'está', 'estou', 'isso', 'esse', 'essa', 'este',
    'esta', 'aqui', 'ali', 'lá', 'quando', 'onde', 'até', 'depois',
    'antes', 'sobre', 'entre', 'sem', 'também', 'foi', 'são', 'tem',
    'tenho', 'sinto', 'tinha', 'tive', 'às', 'uns', 'umas'
]


# ============================================================================
# FUNÇÕES DE CARREGAMENTO E PRÉ-PROCESSAMENTO
# ============================================================================

def carregar_dados(caminho_csv):
    """
    Carrega o dataset de frases médicas rotuladas.

    Args:
        caminho_csv (str): Caminho para o arquivo CSV.

    Returns:
        pd.DataFrame: DataFrame contendo as colunas 'frase', 'situacao' e 'rotulo_num'.
    """
    df = pd.read_csv(caminho_csv)
    # Limpeza básica de strings
    df['frase'] = df['frase'].str.strip().str.strip('"')
    df['situacao'] = df['situacao'].str.strip().str.strip('"').str.lower()
    # Mapeamento binário: 1 = alto risco, 0 = baixo risco
    df['rotulo_num'] = df['situacao'].map({'alto risco': 1, 'baixo risco': 0})
    return df


def vetorizar_tfidf(textos_treino, textos_teste):
    """
    Aplica o método TF-IDF usando Scikit-Learn com unigramas e bigramas.

    Args:
        textos_treino (iterable): Frases de treinamento.
        textos_teste (iterable): Frases de teste.

    Returns:
        tuple: (X_treino, X_teste, vectorizer)
    """
    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words=STOPWORDS_PT,
        ngram_range=(1, 2),  # Captura expressões como "falta de ar", "dor forte"
        min_df=1,
        norm='l2'
    )
    X_treino = vectorizer.fit_transform(textos_treino)
    X_teste = vectorizer.transform(textos_teste)
    return X_treino, X_teste, vectorizer


# ============================================================================
# GERAÇÃO DE VISUALIZAÇÕES
# ============================================================================

def gerar_grafico_matrizes_confusao(cm_lr, cm_dt, acuracia_lr, acuracia_dt):
    """
    Gera e salva gráfico comparativo com as Matrizes de Confusão dos dois modelos.
    """
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    rotulos_classes = ['Baixo Risco', 'Alto Risco']

    # Regressão Logística
    sns.heatmap(
        cm_lr, annot=True, fmt='d', cmap='Blues', cbar=False, ax=axes[0],
        xticklabels=rotulos_classes, yticklabels=rotulos_classes,
        annot_kws={'size': 14, 'weight': 'bold'}
    )
    axes[0].set_title(f"Regressão Logística (Acurácia: {acuracia_lr:.1%})", fontsize=12, fontweight='bold')
    axes[0].set_xlabel("Risco Previsto", fontsize=11)
    axes[0].set_ylabel("Risco Real Clínico", fontsize=11)

    # Árvore de Decisão
    sns.heatmap(
        cm_dt, annot=True, fmt='d', cmap='Greens', cbar=False, ax=axes[1],
        xticklabels=rotulos_classes, yticklabels=rotulos_classes,
        annot_kws={'size': 14, 'weight': 'bold'}
    )
    axes[1].set_title(f"Árvore de Decisão (Acurácia: {acuracia_dt:.1%})", fontsize=12, fontweight='bold')
    axes[1].set_xlabel("Risco Previsto", fontsize=11)
    axes[1].set_ylabel("Risco Real Clínico", fontsize=11)

    plt.suptitle("CardioIA — Matrizes de Confusão da Triagem Clínica (TF-IDF)", fontsize=14, fontweight='bold', y=1.03)
    plt.tight_layout()
    caminho = os.path.join(FIGURES_DIR, "10_classificador_matriz_confusao.png")
    plt.savefig(caminho, dpi=180, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Gráfico salvo: {caminho}")


def gerar_grafico_importancia_termos(vectorizer, model_lr):
    """
    Gera e salva gráfico com os termos mais associados a Alto Risco e Baixo Risco
    baseado nos coeficientes da Regressão Logística.
    """
    feature_names = np.array(vectorizer.get_feature_names_out())
    coeficientes = model_lr.coef_[0]

    # Top 8 termos com coeficientes mais positivos (Alto Risco)
    top_alto_idx = np.argsort(coeficientes)[-8:]
    # Top 8 termos com coeficientes mais negativos (Baixo Risco)
    top_baixo_idx = np.argsort(coeficientes)[:8]

    termos = np.concatenate([feature_names[top_baixo_idx], feature_names[top_alto_idx]])
    valores = np.concatenate([coeficientes[top_baixo_idx], coeficientes[top_alto_idx]])
    cores = ['#27ae60' if v < 0 else '#e74c3c' for v in valores]

    plt.figure(figsize=(11, 6))
    y_pos = np.arange(len(termos))
    bars = plt.barh(y_pos, valores, color=cores, edgecolor='black', alpha=0.85)

    plt.yticks(y_pos, termos, fontsize=11)
    plt.axvline(0, color='gray', linestyle='--', linewidth=0.8)
    plt.xlabel("Peso do Coeficiente no Modelo (Importância Relativa)", fontsize=11)
    plt.title("CardioIA — Termos Mais Determinantes na Triagem (TF-IDF + Logistic Regression)", fontsize=13, fontweight='bold')

    # Legenda explicativa
    plt.text(0.02, 0.05, "[Verde] Direciona para Baixo Risco\n[Vermelho] Direciona para Alto Risco",
             transform=plt.gca().transAxes, fontsize=10,
             bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="#bdc3c7"))

    plt.grid(axis='x', linestyle=':', alpha=0.6)
    plt.tight_layout()
    caminho = os.path.join(FIGURES_DIR, "11_classificador_top_termos.png")
    plt.savefig(caminho, dpi=180, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Gráfico salvo: {caminho}")


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    print()
    print("╔" + "═"*78 + "╗")
    print("║" + " CardioIA — Fase 2: Diagnóstico Automatizado".center(78) + "║")
    print("║" + " Parte 2: Classificador de Risco de Triagem Clínica com TF-IDF".center(78) + "║")
    print("╚" + "═"*78 + "╝")
    print()

    # 1. Carregamento dos dados
    print("📂 Etapa 1: Carregando e inspecionando dataset...")
    df = carregar_dados(ARQUIVO_FRASES_RISCO)

    total = len(df)
    n_alto = (df['rotulo_num'] == 1).sum()
    n_baixo = (df['rotulo_num'] == 0).sum()

    print(f"  [OK] Total de frases carregadas: {total}")
    print(f"       ├── Alto risco:  {n_alto} ({n_alto/total:.1%})")
    print(f"       └── Baixo risco: {n_baixo} ({n_baixo/total:.1%})")
    print()

    # 2. Divisão estratificada (75% treino, 25% teste)
    print("✂️  Etapa 2: Divisão estratificada treino (75%) e teste (25%)...")
    X_train_text, X_test_text, y_train, y_test = train_test_split(
        df['frase'], df['rotulo_num'],
        test_size=0.25,
        random_state=42,
        stratify=df['rotulo_num']
    )
    print(f"  [OK] Conjunto de treino: {len(X_train_text)} amostras")
    print(f"  [OK] Conjunto de teste:  {len(X_test_text)} amostras")
    print()

    # 3. Vetorização TF-IDF
    print("🔢 Etapa 3: Aplicando Vetorização TF-IDF (Scikit-Learn)...")
    X_train_tfidf, X_test_tfidf, vectorizer = vetorizar_tfidf(X_train_text, X_test_text)
    vocab_size = len(vectorizer.vocabulary_)
    print(f"  [OK] Vocabulário TF-IDF gerado: {vocab_size} n-gramas únicos (unigramas e bigramas)")
    print(f"  [OK] Formato da matriz de treino: {X_train_tfidf.shape}")
    print()

    # 4. Treinamento dos Modelos
    print("🤖 Etapa 4: Treinamento e avaliação dos classificadores...")

    # Modelo 1: Regressão Logística
    modelo_lr = LogisticRegression(C=1.0, random_state=42)
    modelo_lr.fit(X_train_tfidf, y_train)
    y_pred_lr = modelo_lr.predict(X_test_tfidf)

    acc_lr = accuracy_score(y_test, y_pred_lr)
    prec_lr = precision_score(y_test, y_pred_lr, pos_label=1)
    rec_lr = recall_score(y_test, y_pred_lr, pos_label=1)
    f1_lr = f1_score(y_test, y_pred_lr, pos_label=1)
    cm_lr = confusion_matrix(y_test, y_pred_lr)

    print("\n  ┌─ MODELO 1: Regressão Logística (Scikit-Learn) ──────────┐")
    print(f"  │ Acurácia:       {acc_lr:6.2%}                                │")
    print(f"  │ Precisão (Alto):{prec_lr:6.2%}                                │")
    print(f"  │ Recall (Alto):  {rec_lr:6.2%} (Sensibilidade para emergências) │")
    print(f"  │ F1-Score:       {f1_lr:6.2%}                                │")
    print("  └─────────────────────────────────────────────────────────┘")

    # Modelo 2: Árvore de Decisão
    modelo_dt = DecisionTreeClassifier(max_depth=4, random_state=42, criterion='gini')
    modelo_dt.fit(X_train_tfidf, y_train)
    y_pred_dt = modelo_dt.predict(X_test_tfidf)

    acc_dt = accuracy_score(y_test, y_pred_dt)
    prec_dt = precision_score(y_test, y_pred_dt, pos_label=1)
    rec_dt = recall_score(y_test, y_pred_dt, pos_label=1)
    f1_dt = f1_score(y_test, y_pred_dt, pos_label=1)
    cm_dt = confusion_matrix(y_test, y_pred_dt)

    print("\n  ┌─ MODELO 2: Árvore de Decisão (Scikit-Learn) ────────────┐")
    print(f"  │ Acurácia:       {acc_dt:6.2%}                                │")
    print(f"  │ Precisão (Alto):{prec_dt:6.2%}                                │")
    print(f"  │ Recall (Alto):  {rec_dt:6.2%} (Sensibilidade para emergências) │")
    print(f"  │ F1-Score:       {f1_dt:6.2%}                                │")
    print("  └─────────────────────────────────────────────────────────┘")

    # 5. Geração de Gráficos
    print("\n📈 Etapa 5: Exportando gráficos explicativos para /figures...")
    gerar_grafico_matrizes_confusao(cm_lr, cm_dt, acc_lr, acc_dt)
    gerar_grafico_importancia_termos(vectorizer, modelo_lr)

    # 6. Teste com frases inéditas (Simulação de Triagem Clínica em Tempo Real)
    print("\n🧪 Etapa 6: Simulação de Triagem Clínica com Casos Inéditos...")

    casos_teste = [
        ("Sinto uma queimação forte no centro do peito que vai para o braço e muito suor frio", "alto risco"),
        ("Tive uma leve dor muscular no peito depois de carregar compras pesadas", "baixo risco"),
        ("Acordei no meio da noite com falta de ar desesperadora e coração disparado", "alto risco"),
        ("Sinto um leve cansaço no final da tarde após um dia cheio de reuniões", "baixo risco"),
        ("Estou com dor intensa no peito e sinto que vou desmaiar a qualquer momento", "alto risco"),
        ("Tive uma azia passageira após o almoço que melhorou com água", "baixo risco")
    ]

    melhor_modelo = modelo_lr if f1_lr >= f1_dt else modelo_dt
    nome_modelo_escolhido = "Regressão Logística" if f1_lr >= f1_dt else "Árvore de Decisão"

    print(f"  Modelo selecionado para triagem operacional: {nome_modelo_escolhido}\n")

    for frase, risco_esperado in casos_teste:
        vetor = vectorizer.transform([frase])
        pred_num = melhor_modelo.predict(vetor)[0]
        # Probabilidade (se suportado)
        prob_alto = melhor_modelo.predict_proba(vetor)[0][1] if hasattr(melhor_modelo, "predict_proba") else None

        tag = "🔴 ALTO RISCO " if pred_num == 1 else "🟢 BAIXO RISCO"
        prob_str = f"(Confiança: {prob_alto:.1%})" if prob_alto is not None else ""
        print(f"  {tag} {prob_str}")
        print(f"     Relato: \"{frase}\"")
        print(f"     Esperado: {risco_esperado.upper()}")
        print()

    # 7. Resumo e Reflexão Crítica sobre Governança e Vieses (Requisito PBL)
    print("╔" + "═"*78 + "╗")
    print("║" + " REFLEXÃO DE GOVERNANÇA, BIOÉTICA E VIESES (PBL) ".center(78) + "║")
    print("╠" + "═"*78 + "╣")
    print("║ 1. Sensibilidade vs Especificidade em Saúde:                                 ║")
    print("║    Em triagens de emergência (como o Protocolo de Manchester), um Falso      ║")
    print("║    Negativo (classificar paciente com infarto como 'baixo risco') pode ser   ║")
    print("║    fatal. Por isso, a métrica de Recall (Sensibilidade) tem prioridade       ║")
    print("║    máxima sobre a acurácia global.                                           ║")
    print("║                                                                              ║")
    print("║ 2. Viés Lexical e Frases Atípicas:                                           ║")
    print("║    Mulheres e idosos frequentemente apresentam sintomas atípicos de infarto  ║")
    print("║    (náusea, dor epigástrica, fadiga extrema sem dor torácica típica). Se a   ║")
    print("║    base de treino não contemplar essas variações, o modelo subnotificará     ║")
    print("║    o risco desses grupos, gerando disparidade no atendimento.                ║")
    print("║                                                                              ║")
    print("║ 3. IA como Apoio à Decisão (Human-in-the-Loop):                              ║")
    print("║    O sistema CardioIA deve atuar como estetoscópio digital de priorização,   ║")
    print("║    nunca substituindo o juízo clínico soberano do médico ou enfermeiro.      ║")
    print("╚" + "═"*78 + "╝")
    print()


if __name__ == "__main__":
    main()
