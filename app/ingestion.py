import sys
import os
from core import processar_arquivo, processar_diretorio

def ingestao(path: str):
    if os.path.isdir(path):
        resultados = processar_diretorio(path)
        for arquivo, status in resultados.items():
            print(f"{arquivo}: {status}")
    elif os.path.isfile(path):
        n_chunks = processar_arquivo(path)
        print(f"{os.path.basename(path)} processado com {n_chunks} chunks.")
    else:
        print("Caminho inválido: informe um arquivo ou pasta válida.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python ingestion.py <caminho_para_arquivo_ou_pasta>")
        sys.exit(1)

    ingestao(sys.argv[1])