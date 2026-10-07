# -*- coding: utf-8 -*-
"""
CardioIA - Fase 2 | Ir Além 2: Diagnóstico Visual com Rede Neural MLP
=======================================================================

Este script realiza:
1. Carregamento do dataset MIT-BIH (Heartbeat) do Kaggle
2. Pré-processamento dos sinais ECG
3. Construção de uma rede neural MLP (Perceptron Multicamadas)
4. Treinamento e validação do modelo
5. Avaliação com métricas detalhadas e visualizações

Dataset: https://www.kaggle.com/datasets/shayanfazeli/heartbeat
  - mitbih_train.csv / mitbih_test.csv
  - Cada linha = 187 amostras do sinal ECG + 1 coluna de classe
  - Classificação binária: Normal (0) vs Anormal (1,2,3,4)

Autores: Equipe CardioIA - FIAP 2025

Requisitos: numpy, pandas, matplotlib, seaborn
            tensorflow/keras (pip install tensorflow)
"""

import os
import sys
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Garante suporte a UTF-8 em terminais Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# ============================================================================
# CONFIGURAÇÕES
# ============================================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
FIGURES_DIR = os.path.join(BASE_DIR, "figures")

# Arquivos do dataset Heartbeat (devem ser baixados do Kaggle)
TRAIN_FILE = os.path.join(DATA_DIR, "mitbih_train.csv")
TEST_FILE = os.path.join(DATA_DIR, "mitbih_test.csv")

# Se os arquivos não existirem, usa dados simulados para demonstração
USAR_DADOS_SIMULADOS = not (os.path.exists(TRAIN_FILE) and os.path.exists(TEST_FILE))


# ============================================================================
# FUNÇÕES DE DADOS
# ============================================================================

def gerar_dados_simulados(n_treino=4000, n_teste=1000, n_features=187, seed=42):
    """
    Gera dados simulados de sinais ECG para demonstração caso o dataset
    real não esteja disponível.

    Simula sinais ECG com:
    - Classe 0 (Normal): Onda P + complexo QRS + onda T regulares
    - Classe 1 (Anormal): Padrões com irregularidades (picos extras, ST elevado)

    Args:
        n_treino (int): Número de amostras de treino.
        n_teste (int): Número de amostras de teste.
        n_features (int): Dimensão do sinal ECG.
        seed (int): Seed para reprodutibilidade.

    Returns:
        tuple: (X_treino, y_treino, X_teste, y_teste)
    """
    np.random.seed(seed)

    def gerar_ecg_normal(n, features):
        """Gera sinais ECG normais simulados."""
        t = np.linspace(0, 1, features)
        sinais = []
        for _ in range(n):
            # Onda P (pequena gaussiana)
            p_wave = 0.15 * np.exp(-((t - 0.15)**2) / (2 * 0.01**2))
            # Complexo QRS (pico alto)
            qrs = 0.8 * np.exp(-((t - 0.35)**2) / (2 * 0.008**2))
            qrs -= 0.2 * np.exp(-((t - 0.32)**2) / (2 * 0.005**2))
            # Onda T (gaussiana média)
            t_wave = 0.3 * np.exp(-((t - 0.55)**2) / (2 * 0.02**2))
            # Ruído
            ruido = np.random.normal(0, 0.02, features)
            # Variação individual
            amplitude = np.random.uniform(0.8, 1.2)
            sinal = amplitude * (p_wave + qrs + t_wave) + ruido
            sinais.append(sinal)
        return np.array(sinais)

    def gerar_ecg_anormal(n, features):
        """Gera sinais ECG anormais simulados (arritmias/infartos)."""
        t = np.linspace(0, 1, features)
        sinais = []
        for _ in range(n):
            tipo = np.random.choice(['arritmia', 'infarto', 'taquicardia'])
            ruido = np.random.normal(0, 0.03, features)

            if tipo == 'arritmia':
                # QRS alargado e irregular
                qrs = 0.6 * np.exp(-((t - 0.35)**2) / (2 * 0.015**2))
                extra_beat = 0.4 * np.exp(-((t - 0.7)**2) / (2 * 0.01**2))
                sinal = qrs + extra_beat + ruido
            elif tipo == 'infarto':
                # ST elevado
                p_wave = 0.1 * np.exp(-((t - 0.15)**2) / (2 * 0.01**2))
                qrs = 0.9 * np.exp(-((t - 0.35)**2) / (2 * 0.008**2))
                st_elevation = 0.3 * np.ones(features)
                st_elevation[:int(features*0.4)] = 0
                st_elevation[int(features*0.6):] = 0
                sinal = p_wave + qrs + st_elevation + ruido
            else:
                # Taquicardia - batimentos rápidos
                qrs1 = 0.7 * np.exp(-((t - 0.2)**2) / (2 * 0.008**2))
                qrs2 = 0.65 * np.exp(-((t - 0.5)**2) / (2 * 0.008**2))
                qrs3 = 0.6 * np.exp(-((t - 0.8)**2) / (2 * 0.008**2))
                sinal = qrs1 + qrs2 + qrs3 + ruido

            amplitude = np.random.uniform(0.7, 1.3)
            sinais.append(amplitude * sinal)
        return np.array(sinais)

    # Proporção: 70% normal, 30% anormal (reflete distribuição real)
    n_normal_treino = int(n_treino * 0.7)
    n_anormal_treino = n_treino - n_normal_treino
    n_normal_teste = int(n_teste * 0.7)
    n_anormal_teste = n_teste - n_normal_teste

    X_normal_treino = gerar_ecg_normal(n_normal_treino, n_features)
    X_anormal_treino = gerar_ecg_anormal(n_anormal_treino, n_features)
    X_normal_teste = gerar_ecg_normal(n_normal_teste, n_features)
    X_anormal_teste = gerar_ecg_anormal(n_anormal_teste, n_features)

    X_treino = np.vstack([X_normal_treino, X_anormal_treino])
    y_treino = np.array([0]*n_normal_treino + [1]*n_anormal_treino)

    X_teste = np.vstack([X_normal_teste, X_anormal_teste])
    y_teste = np.array([0]*n_normal_teste + [1]*n_anormal_teste)

    # Embaralhar
    idx_treino = np.random.permutation(len(y_treino))
    idx_teste = np.random.permutation(len(y_teste))

    return (X_treino[idx_treino], y_treino[idx_treino],
            X_teste[idx_teste], y_teste[idx_teste])


def carregar_dados_kaggle():
    """
    Carrega o dataset MIT-BIH Heartbeat do Kaggle.

    Returns:
        tuple: (X_treino, y_treino, X_teste, y_teste)
    """
    import pandas as pd

    print("  Carregando dados do Kaggle...")
    df_treino = pd.read_csv(TRAIN_FILE, header=None)
    df_teste = pd.read_csv(TEST_FILE, header=None)

    # Última coluna é o rótulo
    X_treino = df_treino.iloc[:, :-1].values
    y_treino_multi = df_treino.iloc[:, -1].values.astype(int)

    X_teste = df_teste.iloc[:, :-1].values
    y_teste_multi = df_teste.iloc[:, -1].values.astype(int)

    # Converter para binário: 0 = Normal, 1 = Anormal (classes 1,2,3,4)
    y_treino = (y_treino_multi > 0).astype(int)
    y_teste = (y_teste_multi > 0).astype(int)

    print(f"  [OK] Treino: {X_treino.shape[0]} amostras, {X_treino.shape[1]} features")
    print(f"  [OK] Teste:  {X_teste.shape[0]} amostras")

    return X_treino, y_treino, X_teste, y_teste


# ============================================================================
# REDE NEURAL MLP (implementação com NumPy puro)
# ============================================================================

class MLP:
    """
    Perceptron Multicamadas (MLP) implementado com NumPy.

    Arquitetura padrão:
    - Camada de entrada: n_features neurônios
    - Camada oculta 1: 128 neurônios (ReLU)
    - Camada oculta 2: 64 neurônios (ReLU)
    - Camada de saída: 1 neurônio (Sigmoid)

    Otimizador: Mini-batch gradient descent com momentum
    """

    def __init__(self, camadas, taxa_aprendizado=0.001, epocas=50,
                 batch_size=32, momentum=0.9):
        """
        Inicializa a MLP.

        Args:
            camadas (list[int]): Número de neurônios em cada camada.
                Exemplo: [187, 128, 64, 1]
            taxa_aprendizado (float): Learning rate.
            epocas (int): Número de épocas de treinamento.
            batch_size (int): Tamanho do mini-batch.
            momentum (float): Fator de momentum para o gradiente.
        """
        self.camadas = camadas
        self.taxa_aprendizado = taxa_aprendizado
        self.epocas = epocas
        self.batch_size = batch_size
        self.momentum = momentum
        self.pesos = []
        self.biases = []
        self.historico = {"loss_treino": [], "loss_val": [],
                         "acc_treino": [], "acc_val": []}

        # Inicialização He (para ReLU)
        np.random.seed(42)
        for i in range(len(camadas) - 1):
            w = np.random.randn(camadas[i], camadas[i+1]) * np.sqrt(2.0 / camadas[i])
            b = np.zeros((1, camadas[i+1]))
            self.pesos.append(w)
            self.biases.append(b)

    @staticmethod
    def relu(z):
        """Ativação ReLU."""
        return np.maximum(0, z)

    @staticmethod
    def relu_derivada(z):
        """Derivada da ReLU."""
        return (z > 0).astype(float)

    @staticmethod
    def sigmoid(z):
        """Ativação Sigmoid."""
        z = np.clip(z, -500, 500)
        return 1.0 / (1.0 + np.exp(-z))

    def forward(self, X):
        """
        Propagação direta (forward pass).

        Args:
            X (np.ndarray): Dados de entrada.

        Returns:
            tuple: (ativações, pré-ativações) para backpropagation.
        """
        ativacoes = [X]
        pre_ativacoes = []

        for i in range(len(self.pesos)):
            z = ativacoes[-1].dot(self.pesos[i]) + self.biases[i]
            pre_ativacoes.append(z)

            if i < len(self.pesos) - 1:
                a = self.relu(z)
            else:
                a = self.sigmoid(z)  # Última camada: sigmoid
            ativacoes.append(a)

        return ativacoes, pre_ativacoes

    def backward(self, X, y, ativacoes, pre_ativacoes):
        """
        Retropropagação (backward pass).

        Args:
            X (np.ndarray): Dados de entrada.
            y (np.ndarray): Rótulos reais (coluna).
            ativacoes (list): Ativações de cada camada.
            pre_ativacoes (list): Pré-ativações de cada camada.

        Returns:
            tuple: (gradientes_pesos, gradientes_biases)
        """
        m = X.shape[0]
        grad_pesos = [None] * len(self.pesos)
        grad_biases = [None] * len(self.biases)

        # Erro da camada de saída
        delta = ativacoes[-1] - y.reshape(-1, 1)

        for i in range(len(self.pesos) - 1, -1, -1):
            grad_pesos[i] = ativacoes[i].T.dot(delta) / m
            grad_biases[i] = np.sum(delta, axis=0, keepdims=True) / m

            if i > 0:
                delta = delta.dot(self.pesos[i].T) * self.relu_derivada(pre_ativacoes[i-1])

        return grad_pesos, grad_biases

    def calcular_loss(self, y_real, y_pred):
        """
        Calcula a Binary Cross-Entropy Loss.

        Args:
            y_real (np.ndarray): Rótulos reais.
            y_pred (np.ndarray): Predições.

        Returns:
            float: Valor da loss.
        """
        y_pred = np.clip(y_pred, 1e-7, 1 - 1e-7)
        y_real = y_real.reshape(-1, 1)
        loss = -np.mean(y_real * np.log(y_pred) + (1 - y_real) * np.log(1 - y_pred))
        return loss

    def fit(self, X_treino, y_treino, X_val=None, y_val=None):
        """
        Treina a rede neural.

        Args:
            X_treino (np.ndarray): Dados de treino.
            y_treino (np.ndarray): Rótulos de treino.
            X_val (np.ndarray, optional): Dados de validação.
            y_val (np.ndarray, optional): Rótulos de validação.
        """
        # Inicializar velocidades do momentum
        vel_pesos = [np.zeros_like(w) for w in self.pesos]
        vel_biases = [np.zeros_like(b) for b in self.biases]

        n_amostras = X_treino.shape[0]
        n_batches = max(1, n_amostras // self.batch_size)

        print(f"\n  Treinando MLP: {self.camadas}")
        print(f"  Épocas: {self.epocas} | Batch: {self.batch_size} | LR: {self.taxa_aprendizado}")
        print(f"  {'─'*65}")

        for epoca in range(1, self.epocas + 1):
            # Embaralhar dados a cada época
            indices = np.random.permutation(n_amostras)
            X_shuffled = X_treino[indices]
            y_shuffled = y_treino[indices]

            loss_epoca = 0

            for batch in range(n_batches):
                inicio = batch * self.batch_size
                fim = min(inicio + self.batch_size, n_amostras)

                X_batch = X_shuffled[inicio:fim]
                y_batch = y_shuffled[inicio:fim]

                # Forward
                ativacoes, pre_ativacoes = self.forward(X_batch)

                # Loss
                loss_epoca += self.calcular_loss(y_batch, ativacoes[-1])

                # Backward
                grad_pesos, grad_biases = self.backward(
                    X_batch, y_batch, ativacoes, pre_ativacoes
                )

                # Atualizar pesos com momentum
                for i in range(len(self.pesos)):
                    vel_pesos[i] = self.momentum * vel_pesos[i] - self.taxa_aprendizado * grad_pesos[i]
                    vel_biases[i] = self.momentum * vel_biases[i] - self.taxa_aprendizado * grad_biases[i]

                    self.pesos[i] += vel_pesos[i]
                    self.biases[i] += vel_biases[i]

            loss_media = loss_epoca / n_batches

            # Acurácia de treino
            y_pred_treino = self.predict(X_treino)
            acc_treino = np.mean(y_pred_treino == y_treino)

            self.historico["loss_treino"].append(loss_media)
            self.historico["acc_treino"].append(acc_treino)

            # Validação
            if X_val is not None and y_val is not None:
                ativacoes_val, _ = self.forward(X_val)
                loss_val = self.calcular_loss(y_val, ativacoes_val[-1])
                y_pred_val = self.predict(X_val)
                acc_val = np.mean(y_pred_val == y_val)

                self.historico["loss_val"].append(loss_val)
                self.historico["acc_val"].append(acc_val)

                if epoca % 5 == 0 or epoca == 1:
                    print(f"  Época {epoca:3d}/{self.epocas} | "
                          f"Loss Treino: {loss_media:.4f} | Acc Treino: {acc_treino:.4f} | "
                          f"Loss Val: {loss_val:.4f} | Acc Val: {acc_val:.4f}")
            else:
                if epoca % 5 == 0 or epoca == 1:
                    print(f"  Época {epoca:3d}/{self.epocas} | "
                          f"Loss: {loss_media:.4f} | Acc: {acc_treino:.4f}")

        print(f"  {'─'*65}")
        print(f"  ✅ Treinamento concluído!")

    def predict(self, X):
        """
        Prediz classes para os dados de entrada.

        Args:
            X (np.ndarray): Dados de entrada.

        Returns:
            np.ndarray: Classes preditas (0 ou 1).
        """
        ativacoes, _ = self.forward(X)
        return (ativacoes[-1] >= 0.5).astype(int).flatten()

    def predict_proba(self, X):
        """
        Retorna probabilidades para os dados de entrada.

        Args:
            X (np.ndarray): Dados de entrada.

        Returns:
            np.ndarray: Probabilidades de ser classe 1.
        """
        ativacoes, _ = self.forward(X)
        return ativacoes[-1].flatten()


# ============================================================================
# FUNÇÕES DE AVALIAÇÃO E VISUALIZAÇÃO
# ============================================================================

def avaliar_modelo(y_real, y_pred, nome="MLP"):
    """
    Avalia o modelo com métricas detalhadas.

    Args:
        y_real (np.ndarray): Rótulos reais.
        y_pred (np.ndarray): Rótulos previstos.
        nome (str): Nome do modelo.
    """
    acuracia = np.mean(y_real == y_pred)

    vp = np.sum((y_real == 1) & (y_pred == 1))
    vn = np.sum((y_real == 0) & (y_pred == 0))
    fp = np.sum((y_real == 0) & (y_pred == 1))
    fn = np.sum((y_real == 1) & (y_pred == 0))

    precisao = vp / (vp + fp) if (vp + fp) > 0 else 0
    recall = vp / (vp + fn) if (vp + fn) > 0 else 0
    f1 = 2 * precisao * recall / (precisao + recall) if (precisao + recall) > 0 else 0
    especificidade = vn / (vn + fp) if (vn + fp) > 0 else 0

    print(f"\n  ╔{'═'*60}╗")
    print(f"  ║{'AVALIAÇÃO DO MODELO: ' + nome:^60}║")
    print(f"  ╠{'═'*60}╣")
    print(f"  ║{'Acurácia:':>25} {acuracia:.4f} ({acuracia:.2%}){'':>18}║")
    print(f"  ║{'Precisão:':>25} {precisao:.4f}{'':>28}║")
    print(f"  ║{'Recall (Sensibilidade):':>25} {recall:.4f}{'':>28}║")
    print(f"  ║{'Especificidade:':>25} {especificidade:.4f}{'':>28}║")
    print(f"  ║{'F1-Score:':>25} {f1:.4f}{'':>28}║")
    print(f"  ╠{'═'*60}╣")
    print(f"  ║{'MATRIZ DE CONFUSÃO':^60}║")
    print(f"  ║{'':>15}{'Previsto Normal':>18}{'Previsto Anormal':>20}{'':>7}║")
    print(f"  ║{'Real Normal':>15}{vn:>18}{fp:>20}{'':>7}║")
    print(f"  ║{'Real Anormal':>15}{fn:>18}{vp:>20}{'':>7}║")
    print(f"  ╚{'═'*60}╝")

    return {
        "acuracia": acuracia,
        "precisao": precisao,
        "recall": recall,
        "f1": f1,
        "especificidade": especificidade
    }


def gerar_graficos(historico, y_teste, y_pred, X_teste):
    """
    Gera gráficos de avaliação e salva em figures/.

    Args:
        historico (dict): Histórico de treino (loss, acurácia).
        y_teste (np.ndarray): Rótulos reais de teste.
        y_pred (np.ndarray): Predições do modelo.
        X_teste (np.ndarray): Dados de teste (para exemplos de ECG).
    """
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        os.makedirs(FIGURES_DIR, exist_ok=True)

        # Gráfico 1: Loss ao longo das épocas
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        axes[0].plot(historico["loss_treino"], label="Treino", color="#e74c3c", linewidth=2)
        if historico["loss_val"]:
            axes[0].plot(historico["loss_val"], label="Validação", color="#3498db", linewidth=2)
        axes[0].set_xlabel("Época", fontsize=12)
        axes[0].set_ylabel("Loss (Binary Cross-Entropy)", fontsize=12)
        axes[0].set_title("Curva de Loss", fontsize=14, fontweight="bold")
        axes[0].legend(fontsize=11)
        axes[0].grid(True, alpha=0.3)

        axes[1].plot(historico["acc_treino"], label="Treino", color="#e74c3c", linewidth=2)
        if historico["acc_val"]:
            axes[1].plot(historico["acc_val"], label="Validação", color="#3498db", linewidth=2)
        axes[1].set_xlabel("Época", fontsize=12)
        axes[1].set_ylabel("Acurácia", fontsize=12)
        axes[1].set_title("Curva de Acurácia", fontsize=14, fontweight="bold")
        axes[1].legend(fontsize=11)
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        caminho = os.path.join(FIGURES_DIR, "mlp_curvas_treinamento.png")
        plt.savefig(caminho, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  [OK] Gráfico salvo: {caminho}")

        # Gráfico 2: Exemplos de ECG
        fig, axes = plt.subplots(2, 3, figsize=(15, 8))
        fig.suptitle("Exemplos de Sinais ECG — Normal vs Anormal", fontsize=16, fontweight="bold")

        # 3 normais
        idx_normal = np.where(y_teste == 0)[0][:3]
        for i, idx in enumerate(idx_normal):
            axes[0][i].plot(X_teste[idx], color="#27ae60", linewidth=1)
            pred_label = "✓ Normal" if y_pred[idx] == 0 else "✗ Anormal"
            axes[0][i].set_title(f"ECG Normal (pred: {pred_label})", fontsize=11)
            axes[0][i].set_xlabel("Amostra")
            axes[0][i].set_ylabel("Amplitude")
            axes[0][i].grid(True, alpha=0.3)

        # 3 anormais
        idx_anormal = np.where(y_teste == 1)[0][:3]
        for i, idx in enumerate(idx_anormal):
            axes[1][i].plot(X_teste[idx], color="#e74c3c", linewidth=1)
            pred_label = "✓ Anormal" if y_pred[idx] == 1 else "✗ Normal"
            axes[1][i].set_title(f"ECG Anormal (pred: {pred_label})", fontsize=11)
            axes[1][i].set_xlabel("Amostra")
            axes[1][i].set_ylabel("Amplitude")
            axes[1][i].grid(True, alpha=0.3)

        plt.tight_layout()
        caminho = os.path.join(FIGURES_DIR, "mlp_exemplos_ecg.png")
        plt.savefig(caminho, dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  [OK] Gráfico salvo: {caminho}")

    except ImportError:
        print("  [AVISO] matplotlib não disponível. Gráficos não gerados.")


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """
    Função principal — pipeline completo de classificação de ECG com MLP.
    """
    print()
    print("╔" + "═"*78 + "╗")
    print("║" + " CardioIA — Fase 2: Diagnóstico Visual com Rede Neural".center(78) + "║")
    print("║" + " Ir Além 2: Classificação de ECG com MLP".center(78) + "║")
    print("╚" + "═"*78 + "╝")
    print()

    # ── Etapa 1: Carregar dados ──────────────────────────────────────────────
    print("📂 Etapa 1: Carregando dados...")

    if USAR_DADOS_SIMULADOS:
        print("  ⚠️  Dataset Kaggle não encontrado. Usando dados SIMULADOS para demonstração.")
        print("  💡 Para usar o dataset real, baixe de:")
        print("     https://www.kaggle.com/datasets/shayanfazeli/heartbeat")
        print(f"     Coloque os arquivos em: {DATA_DIR}")
        X_treino, y_treino, X_teste, y_teste = gerar_dados_simulados()
    else:
        X_treino, y_treino, X_teste, y_teste = carregar_dados_kaggle()

    print(f"\n  Resumo dos dados:")
    print(f"  ├── Treino: {X_treino.shape[0]} amostras × {X_treino.shape[1]} features")
    print(f"  │   ├── Normal:  {np.sum(y_treino == 0)} ({np.mean(y_treino == 0):.1%})")
    print(f"  │   └── Anormal: {np.sum(y_treino == 1)} ({np.mean(y_treino == 1):.1%})")
    print(f"  └── Teste: {X_teste.shape[0]} amostras × {X_teste.shape[1]} features")
    print(f"      ├── Normal:  {np.sum(y_teste == 0)} ({np.mean(y_teste == 0):.1%})")
    print(f"      └── Anormal: {np.sum(y_teste == 1)} ({np.mean(y_teste == 1):.1%})")

    # ── Etapa 2: Pré-processamento ───────────────────────────────────────────
    print("\n🔧 Etapa 2: Pré-processamento dos sinais...")

    # Normalização Z-score (por feature)
    media = X_treino.mean(axis=0)
    desvio = X_treino.std(axis=0) + 1e-8  # Evitar divisão por zero

    X_treino_norm = (X_treino - media) / desvio
    X_teste_norm = (X_teste - media) / desvio

    print(f"  [OK] Normalização Z-score aplicada")
    print(f"       Média das features: {X_treino_norm.mean():.6f} (esperado ≈ 0)")
    print(f"       Desvio das features: {X_treino_norm.std():.6f} (esperado ≈ 1)")

    # Separar validação do treino (20%)
    n_val = int(X_treino_norm.shape[0] * 0.2)
    indices = np.random.permutation(X_treino_norm.shape[0])

    X_val = X_treino_norm[indices[:n_val]]
    y_val = y_treino[indices[:n_val]]
    X_treino_final = X_treino_norm[indices[n_val:]]
    y_treino_final = y_treino[indices[n_val:]]

    print(f"  [OK] Treino final: {X_treino_final.shape[0]} | Validação: {X_val.shape[0]}")

    # ── Etapa 3: Construção e treinamento da MLP ─────────────────────────────
    print("\n🧠 Etapa 3: Construção e treinamento da MLP...")

    n_features = X_treino_final.shape[1]

    # Arquitetura: Input(187) → Dense(128, ReLU) → Dense(64, ReLU) → Dense(1, Sigmoid)
    modelo = MLP(
        camadas=[n_features, 128, 64, 1],
        taxa_aprendizado=0.001,
        epocas=50,
        batch_size=32,
        momentum=0.9
    )

    modelo.fit(X_treino_final, y_treino_final, X_val, y_val)

    # ── Etapa 4: Avaliação ───────────────────────────────────────────────────
    print("\n📊 Etapa 4: Avaliação no conjunto de teste...")

    y_pred = modelo.predict(X_teste_norm)
    metricas = avaliar_modelo(y_teste, y_pred, "MLP - Classificador de ECG")

    # ── Etapa 5: Gráficos ───────────────────────────────────────────────────
    print("\n📈 Etapa 5: Gerando gráficos...")
    gerar_graficos(modelo.historico, y_teste, y_pred, X_teste)

    # ── Resumo final ─────────────────────────────────────────────────────────
    print("\n")
    print("╔" + "═"*78 + "╗")
    print("║" + " RESUMO FINAL".center(78) + "║")
    print("╠" + "═"*78 + "╣")
    print("║" + f"  Arquitetura: {modelo.camadas}".ljust(78) + "║")
    print("║" + f"  Épocas treinadas: {modelo.epocas}".ljust(78) + "║")
    print("║" + f"  Acurácia final (teste): {metricas['acuracia']:.4f} ({metricas['acuracia']:.2%})".ljust(78) + "║")
    print("║" + f"  F1-Score: {metricas['f1']:.4f}".ljust(78) + "║")
    print("║" + f"  Dados: {'SIMULADOS' if USAR_DADOS_SIMULADOS else 'MIT-BIH Heartbeat (Kaggle)'}".ljust(78) + "║")
    print("╚" + "═"*78 + "╝")
    print()
    print("⚠️  AVISO: Este modelo é uma demonstração acadêmica.")
    print("    Não deve ser utilizado para diagnóstico clínico real.")
    print()


# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    main()
