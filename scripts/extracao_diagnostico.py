# -*- coding: utf-8 -*-
"""
CardioIA - Fase 2 | Parte 1: Extração de Informações e Diagnóstico Automatizado
=================================================================================

Este script realiza:
1. Leitura das frases de sintomas do arquivo .txt
2. Identificação de sintomas com base no mapa de conhecimento (.csv)
3. Sugestão de diagnósticos para cada frase/paciente

Autores: Equipe CardioIA - FIAP 2025
"""

import csv
import os
import re
import sys
from collections import defaultdict

# Garante suporte a UTF-8 em terminais Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# ============================================================================
# CONFIGURAÇÕES DE CAMINHOS
# ============================================================================

# Diretório base do projeto (relativo ao script)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

ARQUIVO_FRASES = os.path.join(DATA_DIR, "sintomas_pacientes.txt")
ARQUIVO_MAPA = os.path.join(DATA_DIR, "mapa_conhecimento.csv")


# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def carregar_frases(caminho_arquivo):
    """
    Carrega as frases de sintomas do arquivo .txt.

    Args:
        caminho_arquivo (str): Caminho para o arquivo de frases.

    Returns:
        list[str]: Lista de frases (uma por linha).
    """
    frases = []
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha:  # Ignora linhas vazias
                frases.append(linha)
    print(f"  [OK] {len(frases)} frases carregadas de '{os.path.basename(caminho_arquivo)}'")
    return frases


def carregar_mapa_conhecimento(caminho_arquivo):
    """
    Carrega o mapa de conhecimento (sintomas → doenças) do arquivo .csv.

    Cada linha do CSV contém: sintoma_1, sintoma_2, doenca_associada.
    O mapa é armazenado como uma lista de dicionários para facilitar a busca.

    Args:
        caminho_arquivo (str): Caminho para o arquivo CSV do mapa.

    Returns:
        list[dict]: Lista de entradas do mapa de conhecimento.
    """
    mapa = []
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            mapa.append({
                "sintoma_1": linha["sintoma_1"].strip().lower(),
                "sintoma_2": linha["sintoma_2"].strip().lower(),
                "doenca": linha["doenca_associada"].strip()
            })
    print(f"  [OK] {len(mapa)} regras carregadas de '{os.path.basename(caminho_arquivo)}'")
    return mapa


def normalizar_texto(texto):
    """
    Normaliza o texto para facilitar a correspondência com os sintomas.

    Aplica:
    - Conversão para minúsculas
    - Remoção de acentos comuns (substituição simples)
    - Remoção de pontuação extra

    Args:
        texto (str): Texto original.

    Returns:
        str: Texto normalizado.
    """
    texto = texto.lower()
    # Manter acentos pois os sintomas do mapa também os possuem
    # Remover pontuação excessiva mantendo espaços
    texto = re.sub(r'[^\w\sáàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto


def identificar_sintomas(frase, mapa_conhecimento):
    """
    Identifica sintomas presentes em uma frase com base no mapa de conhecimento.

    A busca é feita verificando se as expressões de sintoma (do mapa) estão
    contidas na frase normalizada. São aplicados dois níveis de correspondência:
    - Match completo: ambos os sintomas encontrados → alta confiança
    - Match parcial: apenas um sintoma encontrado → confiança moderada

    Args:
        frase (str): Frase relatada pelo paciente.
        mapa_conhecimento (list[dict]): Mapa de conhecimento carregado.

    Returns:
        list[dict]: Lista de diagnósticos sugeridos com nível de confiança.
    """
    frase_normalizada = normalizar_texto(frase)
    diagnosticos = []
    doencas_encontradas = set()

    # Primeiro: buscar matches completos (ambos sintomas presentes)
    for regra in mapa_conhecimento:
        sintoma1_encontrado = regra["sintoma_1"] in frase_normalizada
        sintoma2_encontrado = regra["sintoma_2"] in frase_normalizada

        if sintoma1_encontrado and sintoma2_encontrado:
            chave = regra["doenca"]
            if chave not in doencas_encontradas:
                diagnosticos.append({
                    "doenca": regra["doenca"],
                    "sintomas_detectados": [regra["sintoma_1"], regra["sintoma_2"]],
                    "confianca": "ALTA",
                    "match_tipo": "completo"
                })
                doencas_encontradas.add(chave)

    # Segundo: buscar matches parciais (apenas um sintoma presente)
    for regra in mapa_conhecimento:
        sintoma1_encontrado = regra["sintoma_1"] in frase_normalizada
        sintoma2_encontrado = regra["sintoma_2"] in frase_normalizada

        if (sintoma1_encontrado or sintoma2_encontrado) and not (sintoma1_encontrado and sintoma2_encontrado):
            chave = regra["doenca"]
            if chave not in doencas_encontradas:
                sintoma_encontrado = regra["sintoma_1"] if sintoma1_encontrado else regra["sintoma_2"]
                diagnosticos.append({
                    "doenca": regra["doenca"],
                    "sintomas_detectados": [sintoma_encontrado],
                    "confianca": "MODERADA",
                    "match_tipo": "parcial"
                })
                doencas_encontradas.add(chave)

    return diagnosticos


def exibir_diagnostico(numero_paciente, frase, diagnosticos):
    """
    Exibe o resultado da análise de uma frase de paciente de forma formatada.

    Args:
        numero_paciente (int): Número sequencial do paciente.
        frase (str): Frase original relatada.
        diagnosticos (list[dict]): Lista de diagnósticos sugeridos.
    """
    print(f"\n{'='*80}")
    print(f"  PACIENTE #{numero_paciente:02d}")
    print(f"{'='*80}")
    print(f"  Relato: \"{frase[:100]}{'...' if len(frase) > 100 else ''}\"")
    print(f"{'─'*80}")

    if diagnosticos:
        # Ordenar: alta confiança primeiro
        diagnosticos_ordenados = sorted(
            diagnosticos,
            key=lambda d: 0 if d["confianca"] == "ALTA" else 1
        )

        print(f"  {'DIAGNÓSTICOS SUGERIDOS':^76}")
        print(f"  {'─'*76}")

        for i, diag in enumerate(diagnosticos_ordenados, 1):
            icone_confianca = "🔴" if diag["confianca"] == "ALTA" else "🟡"
            print(f"  {icone_confianca} {i}. {diag['doenca']}")
            print(f"     Sintomas detectados: {', '.join(diag['sintomas_detectados'])}")
            print(f"     Confiança: {diag['confianca']} (match {diag['match_tipo']})")
            if i < len(diagnosticos_ordenados):
                print()
    else:
        print("  ⚪ Nenhum diagnóstico sugerido com base no mapa de conhecimento.")
        print("     Recomenda-se avaliação clínica presencial.")

    print(f"{'='*80}")


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """
    Função principal que orquestra todo o processo de extração de diagnósticos.
    """
    print()
    print("╔" + "═"*78 + "╗")
    print("║" + " CardioIA — Fase 2: Diagnóstico Automatizado".center(78) + "║")
    print("║" + " Parte 1: Extração de Informações + Sugestão de Diagnóstico".center(78) + "║")
    print("╚" + "═"*78 + "╝")
    print()

    # ── Etapa 1: Carregar dados ──────────────────────────────────────────────
    print("📂 Etapa 1: Carregando dados...")
    frases = carregar_frases(ARQUIVO_FRASES)
    mapa = carregar_mapa_conhecimento(ARQUIVO_MAPA)
    print()

    # ── Etapa 2: Análise de cada frase ───────────────────────────────────────
    print("🔍 Etapa 2: Analisando frases e extraindo diagnósticos...")

    resultados = []
    total_diagnosticos = 0
    total_alta_confianca = 0

    for i, frase in enumerate(frases, 1):
        diagnosticos = identificar_sintomas(frase, mapa)
        resultados.append((i, frase, diagnosticos))
        total_diagnosticos += len(diagnosticos)
        total_alta_confianca += sum(1 for d in diagnosticos if d["confianca"] == "ALTA")

    # ── Etapa 3: Exibir resultados ───────────────────────────────────────────
    print("\n📋 Etapa 3: Resultados da análise\n")

    for numero, frase, diagnosticos in resultados:
        exibir_diagnostico(numero, frase, diagnosticos)

    # ── Resumo final ─────────────────────────────────────────────────────────
    print("\n")
    print("╔" + "═"*78 + "╗")
    print("║" + " RESUMO DA ANÁLISE".center(78) + "║")
    print("╠" + "═"*78 + "╣")
    print("║" + f"  Total de frases analisadas:           {len(frases)}".ljust(78) + "║")
    print("║" + f"  Total de diagnósticos sugeridos:       {total_diagnosticos}".ljust(78) + "║")
    print("║" + f"  Diagnósticos de alta confiança:        {total_alta_confianca}".ljust(78) + "║")
    print("║" + f"  Diagnósticos de confiança moderada:    {total_diagnosticos - total_alta_confianca}".ljust(78) + "║")
    print("║" + f"  Regras no mapa de conhecimento:        {len(mapa)}".ljust(78) + "║")
    print("╚" + "═"*78 + "╝")
    print()
    print("⚠️  AVISO: Este sistema é apenas uma simulação acadêmica.")
    print("    Diagnósticos reais devem ser realizados por profissionais de saúde.")
    print()


# ============================================================================
# EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    main()
