
# Aqui é onde se define as funções que a IA pode "chamar"
# Por enquanto só fiz uma função bem simples pra teste mesmo

def somar(a: int, b: int) -> int:
    return a + b  # Soma dois números

# Aqui registramos todas as funções que o modelo pode usar por nome
functions = {
    "somar": somar
}

# Você pode adicionar outras funções aqui depois, tipo:
# def subtrair(a, b): return a - b
# e colocar no dicionário: "subtrair": subtrair
