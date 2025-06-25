from fastapi import FastAPI, Request
from app.model_loader import ask_model  
from app.function_registry import functions  # Dicionário com as funções disponíveis
import json

app = FastAPI()

# Essa rota vai receber as mensagens do cliente, tipo um chatbot
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()

    # Verifica se está no formato esperado
    if data.get("type") != "message" or "content" not in data:
        return {
            "type": "error",
            "content": "Formato inválido. Esperado: { type: 'message', content: 'texto aqui' }"
        }

    # Pega o texto enviado
    prompt = data["content"]

    # Aqui o modelo responde com algum texto
    resposta = ask_model(prompt)

    # Se a IA responder com algo do tipo: CALL: { "function": "...", "args": {...} }
    if resposta.startswith("CALL:"):
        try:
            # Remove o prefixo e converte pra dicionário Python
            chamada = json.loads(resposta.replace("CALL:", "").strip())
            nome_funcao = chamada.get("function")
            argumentos = chamada.get("args", {})

            # Verifica se a função realmente existe no nosso dicionário
            if nome_funcao in functions:
                resultado = functions[nome_funcao](**argumentos)
                return {
                    "type": "function_result",
                    "content": str(resultado)
                }
            else:
                return {
                    "type": "error",
                    "content": f"A função '{nome_funcao}' não foi encontrada."
                }

        except Exception as erro:
            return {
                "type": "error",
                "content": f"Erro ao executar a função: {str(erro)}"
            }

    # Caso seja só uma resposta normal do modelo, devolve assim mesmo
    return {
        "type": "response",
        "content": resposta
    }
