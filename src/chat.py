#!/usr/bin/env python3
"""
Interface CLI para chat com o sistema de busca semântica
"""
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from search import search_prompt

def print_header():
    print("=" * 40)
    print("🤖 PDF RAG CHAT")
    print("=" * 40)
    print("Faça perguntas sobre o conteúdo do documento PDF.")
    print("=" * 40)
    print()

def print_separator():
    print("\n" + "-" * 60 + "\n")

def main():
    print_header()

    while True:
        try:
            pergunta = input("Faça sua pergunta: ").strip()

            if not pergunta:
                print("⚠️  Input inválido.\n")
                continue

            print(f"\nPERGUNTA: {pergunta}")

            print("🔍 Carregando...")
            resposta = search_prompt(pergunta)

            print(f"RESPOSTA: {resposta}")

            print_separator()

        except Exception as e:
            print(f"\n❌ Erro: {e}")

if __name__ == "__main__":
    main()