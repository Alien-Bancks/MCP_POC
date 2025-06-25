# Aqui é onde se define as funções que a IA pode "chamar"

def somar(a: int, b: int) -> int:
    return a + b  # Soma dois números

# Aqui registramos todas as funções que o modelo pode usar por nome
functions = {
    "somar": somar
}

# Aqui vai o schema no formato do MCP (pra passar pro modelo)
function_schemas = [
    {
        "name": "somar",
        "description": "Soma dois números inteiros",
        "parameters": {
            "type": "object",
            "properties": {
                "a": { "type": "integer", "description": "Primeiro número" },
                "b": { "type": "integer", "description": "Segundo número" }
            },
            "required": ["a", "b"]
        }
    }
]

# pode adicionar outras funções aqui depois, tipo:
# def subtrair(a, b): return a - b
# functions["subtrair"] = subtrair
# function_schemas.append({...})
