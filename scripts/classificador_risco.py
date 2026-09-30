# -*- coding: utf-8 -*-
"""
CardioIA - Fase 2 | Parte 2: Classificador Básico de Texto (Triagem Clínica)
==============================================================================

Este script realiza:
1. Carregamento da base de frases médicas rotuladas (alto/baixo risco)
2. Vetorização das frases com TF-IDF
3. Treinamento de modelos de classificação (Logistic Regression + Decision Tree)
4. Avaliação do desempenho com métricas detalhadas
5. Teste com novas frases para demonstração

Autores: Equipe CardioIA - FIAP 2025
"""

import os
import csv
import numpy as np
from collections import Counter

# ============================================================================
# CONFIGURAÇÕES DE CAMINHOS
# ============================================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
ARQUIVO_FRASES_RISCO = os.path.join(DATA_DIR, "frases_risco.csv")


# ============================================================================
# IMPLEMENTAÇÃO TF-IDF DO ZERO (sem sklearn)
# ============================================================================

def tokenizar(texto):
    """
    Tokeniza um texto em palavras, removendo pontuação e convertendo
    para minúsculas. Remove stopwords comuns do português.

    Args:
        texto (str): Texto para tokenizar.

    Returns:
        list[str]: Lista de tokens.
    """
    import re
    # Stopwords comuns em português
    stopwords_pt = {
        'a', 'o', 'e', 'é', 'de', 'do', 'da', 'em', 'um', 'uma', 'para',
        'com', 'no', 'na', 'que', 'os', 'as', 'dos', 'das', 'por', 'ao',
        'se', 'ou', 'mas', 'como', 'já', 'eu', 'ele', 'ela', 'nos', 'não',
        'mais', 'muito', 'há', 'me', 'meu', 'minha', 'seu', 'sua', 'ter',
        'ser', 'ir', 'está', 'estou', 'isso', 'esse', 'essa', 'este',
        'esta', 'aqui', 'ali', 'lá', 'quando', 'onde', 'até', 'depois',
        'antes', 'sobre', 'entre', 'sem', 'também', 'foi', 'são', 'tem',
        'tenho', 'sinto', 'estou', 'tinha', 'tive', 'às', 'uns', 'umas'
    }
    texto = texto.lower()
    tokens = re.findall(r'[a-záàâãéèêíìîóòôõúùûç]+', texto)
    tokens = [t for t in tokens if t not in stopwords_pt and len(t) > 2]
    return tokens


class VetorizadorTFIDF:
    """
    Implementação simplificada de TF-IDF para vetorização de texto.

    TF (Term Frequency): frequência do termo no documento
    IDF (Inverse Document Frequency): log(N / df) onde N = total de documentos
                                      e df = documentos que contêm o termo
    """

    def __init__(self):
        self.vocabulario = {}
        self.idf = {}
        self.num_documentos = 0

    def fit(self, documentos):
        """
        Ajusta o vetorizador ao corpus, construindo vocabulário e calculando IDF.

        Args:
            documentos (list[str]): Lista de textos do corpus.
        """
        self.num_documentos = len(documentos)
        doc_freq = Counter()
        todos_tokens = set()

        # Contar frequência de documentos para cada termo
        for doc in documentos:
            tokens = set(tokenizar(doc))
            for token in tokens:
                doc_freq[token] += 1
            todos_tokens.update(tokens)

        # Construir vocabulário (índice de cada termo)
        self.vocabulario = {termo: idx for idx, termo in enumerate(sorted(todos_tokens))}

        # Calcular IDF: log(N / df) + 1 (suavizado)
        import math
        self.idf = {}
        for termo, idx in self.vocabulario.items():
            df = doc_freq.get(termo, 0)
            self.idf[termo] = math.log((self.num_documentos + 1) / (df + 1)) + 1

    def transform(self, documentos):
        """
        Transforma documentos em vetores TF-IDF.

        Args:
            documentos (list[str]): Lista de textos para vetorizar.

        Returns:
            list[list[float]]: Matriz de vetores TF-IDF.
        """
        matriz = []
        for doc in documentos:
            tokens = tokenizar(doc)
            tf = Counter(tokens)
            total_tokens = len(tokens) if tokens else 1

            vetor = [0.0] * len(self.vocabulario)
            for termo, contagem in tf.items():
                if termo in self.vocabulario:
                    idx = self.vocabulario[termo]
                    tf_valor = contagem / total_tokens
                    vetor[idx] = tf_valor * self.idf.get(termo, 1.0)

            # Normalização L2
            norma = sum(v**2 for v in vetor) ** 0.5
            if norma > 0:
                vetor = [v / norma for v in vetor]

            matriz.append(vetor)

        return matriz

    def fit_transform(self, documentos):
        """Ajusta e transforma em um passo."""
        self.fit(documentos)
        return self.transform(documentos)


# ============================================================================
# IMPLEMENTAÇÃO DE CLASSIFICADORES
# ============================================================================

class RegressaoLogisticaSimples:
    """
    Implementação simplificada de Regressão Logística com gradiente descendente.
    """

    def __init__(self, taxa_aprendizado=0.1, iteracoes=1000):
        self.taxa_aprendizado = taxa_aprendizado
        self.iteracoes = iteracoes
        self.pesos = None
        self.bias = 0.0

    def _sigmoid(self, z):
        """Função sigmoide."""
        return [1.0 / (1.0 + np.exp(-min(max(zi, -500), 500))) for zi in z]

    def fit(self, X, y):
        """Treina o modelo."""
        X = np.array(X)
        y = np.array(y, dtype=float)
        n_amostras, n_features = X.shape
        self.pesos = np.zeros(n_features)
        self.bias = 0.0

        for _ in range(self.iteracoes):
            z = X.dot(self.pesos) + self.bias
            predicoes = np.array(self._sigmoid(z))

            # Gradientes
            erro = predicoes - y
            grad_pesos = (1 / n_amostras) * X.T.dot(erro)
            grad_bias = (1 / n_amostras) * np.sum(erro)

            # Atualização
            self.pesos -= self.taxa_aprendizado * grad_pesos
            self.bias -= self.taxa_aprendizado * grad_bias

    def predict(self, X):
        """Prediz classes."""
        X = np.array(X)
        z = X.dot(self.pesos) + self.bias
        predicoes = self._sigmoid(z)
        return [1 if p >= 0.5 else 0 for p in predicoes]


class ArvoreDecisaoSimples:
    """
    Implementação simplificada de Árvore de Decisão (Decision Stump).
    Usa o critério de Gini para encontrar o melhor split.
    """

    def __init__(self, profundidade_max=5):
        self.profundidade_max = profundidade_max
        self.arvore = None

    def _gini(self, y):
        """Calcula o índice de Gini."""
        if len(y) == 0:
            return 0
        contagem = Counter(y)
        impureza = 1.0
        for classe in contagem:
            prob = contagem[classe] / len(y)
            impureza -= prob ** 2
        return impureza

    def _melhor_split(self, X, y):
        """Encontra o melhor split baseado no Gini."""
        melhor_ganho = -1
        melhor_feature = None
        melhor_threshold = None

        n_features = len(X[0])
        gini_pai = self._gini(y)

        for feature in range(n_features):
            valores = sorted(set(x[feature] for x in X))
            for i in range(len(valores) - 1):
                threshold = (valores[i] + valores[i+1]) / 2

                y_esq = [y[j] for j in range(len(X)) if X[j][feature] <= threshold]
                y_dir = [y[j] for j in range(len(X)) if X[j][feature] > threshold]

                if len(y_esq) == 0 or len(y_dir) == 0:
                    continue

                gini_esq = self._gini(y_esq)
                gini_dir = self._gini(y_dir)

                peso_esq = len(y_esq) / len(y)
                peso_dir = len(y_dir) / len(y)

                ganho = gini_pai - (peso_esq * gini_esq + peso_dir * gini_dir)

                if ganho > melhor_ganho:
                    melhor_ganho = ganho
                    melhor_feature = feature
                    melhor_threshold = threshold

        return melhor_feature, melhor_threshold, melhor_ganho

    def _construir_arvore(self, X, y, profundidade=0):
        """Constrói a árvore recursivamente."""
        # Condições de parada
        if profundidade >= self.profundidade_max or len(set(y)) == 1 or len(y) <= 2:
            contagem = Counter(y)
            return {"folha": True, "classe": contagem.most_common(1)[0][0]}

        feature, threshold, ganho = self._melhor_split(X, y)

        if feature is None or ganho <= 0:
            contagem = Counter(y)
            return {"folha": True, "classe": contagem.most_common(1)[0][0]}

        # Dividir dados
        idx_esq = [i for i in range(len(X)) if X[i][feature] <= threshold]
        idx_dir = [i for i in range(len(X)) if X[i][feature] > threshold]

        X_esq = [X[i] for i in idx_esq]
        y_esq = [y[i] for i in idx_esq]
        X_dir = [X[i] for i in idx_dir]
        y_dir = [y[i] for i in idx_dir]

        return {
            "folha": False,
            "feature": feature,
            "threshold": threshold,
            "esquerda": self._construir_arvore(X_esq, y_esq, profundidade + 1),
            "direita": self._construir_arvore(X_dir, y_dir, profundidade + 1)
        }

    def fit(self, X, y):
        """Treina a árvore de decisão."""
        self.arvore = self._construir_arvore(X, y)

    def _prever_um(self, x, no):
        """Prediz para uma única amostra."""
        if no["folha"]:
            return no["classe"]
        if x[no["feature"]] <= no["threshold"]:
            return self._prever_um(x, no["esquerda"])
        else:
            return self._prever_um(x, no["direita"])

    def predict(self, X):
        """Prediz classes para múltiplas amostras."""
        return [self._prever_um(x, self.arvore) for x in X]


# ============================================================================
# FUNÇÕES DE AVALIAÇÃO
# ============================================================================

def calcular_metricas(y_real, y_pred, nome_modelo):
    """
    Calcula e exibe métricas de avaliação do classificador.

    Args:
        y_real (list): Rótulos reais.
        y_pred (list): Rótulos previstos.
        nome_modelo (str): Nome do modelo para exibição.
    """
    # Acurácia
    acertos = sum(1 for r, p in zip(y_real, y_pred) if r == p)
    acuracia = acertos / len(y_real) if y_real else 0

    # Métricas por classe
    classes = sorted(set(y_real + y_pred))

    print(f"\n  📊 Métricas do modelo: {nome_modelo}")
    print(f"  {'─'*60}")
    print(f"  Acurácia: {acuracia:.2%} ({acertos}/{len(y_real)})")
    print()

    # Matriz de confusão
    print(f"  Matriz de Confusão:")
    print(f"  {'':>20} {'Previsto':^30}")
    print(f"  {'':>20} {'Alto Risco':^15} {'Baixo Risco':^15}")
    print(f"  {'Real':>6} {'Alto Risco':>13}", end="")

    # VP, FP, FN, VN
    vp = sum(1 for r, p in zip(y_real, y_pred) if r == 1 and p == 1)
    fp = sum(1 for r, p in zip(y_real, y_pred) if r == 0 and p == 1)
    fn = sum(1 for r, p in zip(y_real, y_pred) if r == 1 and p == 0)
    vn = sum(1 for r, p in zip(y_real, y_pred) if r == 0 and p == 0)

    print(f"   {vp:^15} {fn:^15}")
    print(f"  {'':>6} {'Baixo Risco':>13}   {fp:^15} {vn:^15}")
    print()

    # Precisão, Recall, F1
    precisao_alto = vp / (vp + fp) if (vp + fp) > 0 else 0
    recall_alto = vp / (vp + fn) if (vp + fn) > 0 else 0
    f1_alto = 2 * precisao_alto * recall_alto / (precisao_alto + recall_alto) if (precisao_alto + recall_alto) > 0 else 0

    precisao_baixo = vn / (vn + fn) if (vn + fn) > 0 else 0
    recall_baixo = vn / (vn + fp) if (vn + fp) > 0 else 0
    f1_baixo = 2 * precisao_baixo * recall_baixo / (precisao_baixo + recall_baixo) if (precisao_baixo + recall_baixo) > 0 else 0

    print(f"  {'Classe':<15} {'Precisão':>10} {'Recall':>10} {'F1-Score':>10}")
    print(f"  {'─'*50}")
    print(f"  {'Alto Risco':<15} {precisao_alto:>10.2%} {recall_alto:>10.2%} {f1_alto:>10.2%}")
    print(f"  {'Baixo Risco':<15} {precisao_baixo:>10.2%} {recall_baixo:>10.2%} {f1_baixo:>10.2%}")
    print(f"  {'─'*50}")
    print(f"  {'Média':<15} {(precisao_alto+precisao_baixo)/2:>10.2%} {(recall_alto+recall_baixo)/2:>10.2%} {(f1_alto+f1_baixo)/2:>10.2%}")

    return acuracia


def dividir_dados(X, y, proporcao_teste=0.25, seed=42):
    """
    Divide os dados em treino e teste de forma estratificada simples.

    Args:
        X (list): Features.
        y (list): Labels.
        proporcao_teste (float): Proporção de dados para teste.
        seed (int): Seed para reprodutibilidade.

    Returns:
        tuple: (X_treino, X_teste, y_treino, y_teste)
    """
    import random
    random.seed(seed)

    # Separar índices por classe
    idx_alto = [i for i, label in enumerate(y) if label == 1]
    idx_baixo = [i for i, label in enumerate(y) if label == 0]

    random.shuffle(idx_alto)
    random.shuffle(idx_baixo)

    # Dividir proporcionalmente
    n_teste_alto = max(1, int(len(idx_alto) * proporcao_teste))
    n_teste_baixo = max(1, int(len(idx_baixo) * proporcao_teste))

    idx_teste = idx_alto[:n_teste_alto] + idx_baixo[:n_teste_baixo]
    idx_treino = idx_alto[n_teste_alto:] + idx_baixo[n_teste_baixo:]

    random.shuffle(idx_teste)
    random.shuffle(idx_treino)

    X_treino = [X[i] for i in idx_treino]
    X_teste = [X[i] for i in idx_teste]
    y_treino = [y[i] for i in idx_treino]
    y_teste = [y[i] for i in idx_teste]

    return X_treino, X_teste, y_treino, y_teste


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """
    Função principal que orquestra o pipeline completo de classificação.
    """
    print()
    print("╔" + "═"*78 + "╗")
    print("║" + " CardioIA — Fase 2: Diagnóstico Automatizado".center(78) + "║")
    print("║" + " Parte 2: Classificador de Texto para Triagem Clínica".center(78) + "║")
    print("╚" + "═"*78 + "╝")
    print()

    # ── Etapa 1: Carregar dados ──────────────────────────────────────────────
    print("📂 Etapa 1: Carregando base de frases rotuladas...")

    frases = []
    rotulos = []
    rotulos_texto = []

    with open(ARQUIVO_FRASES_RISCO, "r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            frase = linha["frase"].strip().strip('"')
            situacao = linha["situacao"].strip().strip('"')
            frases.append(frase)
            rotulos_texto.append(situacao)
            rotulos.append(1 if situacao == "alto risco" else 0)

    n_alto = sum(rotulos)
    n_baixo = len(rotulos) - n_alto
    print(f"  [OK] {len(frases)} frases carregadas")
    print(f"       ├── Alto risco:  {n_alto} ({n_alto/len(frases):.0%})")
    print(f"       └── Baixo risco: {n_baixo} ({n_baixo/len(frases):.0%})")
    print()

    # ── Etapa 2: Vetorização TF-IDF ──────────────────────────────────────────
    print("🔢 Etapa 2: Vetorização TF-IDF...")

    vetorizador = VetorizadorTFIDF()
    X = vetorizador.fit_transform(frases)

    print(f"  [OK] Vocabulário: {len(vetorizador.vocabulario)} termos únicos")
    print(f"  [OK] Matriz TF-IDF: {len(X)} documentos × {len(X[0])} features")

    # Mostrar top termos por IDF
    termos_idf = sorted(vetorizador.idf.items(), key=lambda x: x[1], reverse=True)
    print(f"\n  Top 10 termos mais discriminantes (maior IDF):")
    for i, (termo, idf) in enumerate(termos_idf[:10], 1):
        print(f"    {i:2d}. {termo:<25} IDF = {idf:.4f}")
    print()

    # ── Etapa 3: Divisão treino/teste ────────────────────────────────────────
    print("✂️  Etapa 3: Dividindo dados em treino e teste...")

    X_treino, X_teste, y_treino, y_teste = dividir_dados(X, rotulos, proporcao_teste=0.25)

    print(f"  [OK] Treino: {len(X_treino)} amostras")
    print(f"  [OK] Teste:  {len(X_teste)} amostras")
    print()

    # ── Etapa 4: Treinamento e avaliação ─────────────────────────────────────
    print("🤖 Etapa 4: Treinando classificadores...\n")

    # Modelo 1: Regressão Logística
    print("  ┌─ Modelo 1: Regressão Logística ──────────────────────────┐")
    rl = RegressaoLogisticaSimples(taxa_aprendizado=0.5, iteracoes=2000)
    rl.fit(X_treino, y_treino)
    y_pred_rl = rl.predict(X_teste)
    acuracia_rl = calcular_metricas(y_teste, y_pred_rl, "Regressão Logística")
    print("  └─────────────────────────────────────────────────────────┘")

    # Modelo 2: Árvore de Decisão
    print("\n  ┌─ Modelo 2: Árvore de Decisão ────────────────────────────┐")
    ad = ArvoreDecisaoSimples(profundidade_max=5)
    ad.fit(X_treino, y_treino)
    y_pred_ad = ad.predict(X_teste)
    acuracia_ad = calcular_metricas(y_teste, y_pred_ad, "Árvore de Decisão")
    print("  └─────────────────────────────────────────────────────────┘")

    # ── Etapa 5: Teste com novas frases ──────────────────────────────────────
    print("\n\n🧪 Etapa 5: Testando com novas frases (não vistas no treino)...\n")

    novas_frases = [
        "sinto uma dor muito forte no peito e estou suando frio",
        "tive uma leve dor nas costas depois de carregar peso",
        "meu coração está acelerado e sinto tontura com falta de ar",
        "sinto um pouco de cansaço após a academia mas passa rápido",
        "tenho dor no peito intensa que irradia para a mandíbula"
    ]

    X_novas = vetorizador.transform(novas_frases)

    # Usar o melhor modelo
    melhor_modelo = rl if acuracia_rl >= acuracia_ad else ad
    nome_melhor = "Regressão Logística" if acuracia_rl >= acuracia_ad else "Árvore de Decisão"

    print(f"  Usando melhor modelo: {nome_melhor}\n")

    for frase, vetor in zip(novas_frases, X_novas):
        pred = melhor_modelo.predict([vetor])[0]
        classe = "🔴 ALTO RISCO" if pred == 1 else "🟢 BAIXO RISCO"
        print(f"  {classe}")
        print(f"  Frase: \"{frase}\"")
        print()

    # ── Resumo final ─────────────────────────────────────────────────────────
    print()
    print("╔" + "═"*78 + "╗")
    print("║" + " RESUMO COMPARATIVO DOS MODELOS".center(78) + "║")
    print("╠" + "═"*78 + "╣")
    print("║" + f"  Regressão Logística — Acurácia: {acuracia_rl:.2%}".ljust(78) + "║")
    print("║" + f"  Árvore de Decisão   — Acurácia: {acuracia_ad:.2%}".ljust(78) + "║")
    print("║" + f"  Melhor modelo: {nome_melhor}".ljust(78) + "║")
    print("╚" + "═"*78 + "╝")
    print()
    print("⚠️  AVISO: Este classificador é uma simulação acadêmica para fins de")
    print("    aprendizado. Em sistemas reais, a triagem deve considerar múltiplos")
    print("    fatores e sempre ser supervisionada por profissionais de saúde.")
    print()


# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    main()
