from fastapi import FastAPI, Request
from app.model_loader import ask_model  
from app.function_registry import functions, function_schemas  
import json

app = FastAPI()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()

    if data.get("type") != "chat.completion" or "messages" not in data:
        return {
            "type": "error",
            "content": "Formato inválido. Esperado: { type: 'chat.completion', messages: [...], functions: [...] }"
        }

    messages = data["messages"]
    functions_input = data.get("functions", function_schemas)  # Usa o padrão se não mandarem

    # Envia tudo pro modelo e pega a resposta
    resposta = ask_model(messages=messages, functions=functions_input)

    # Se a IA quiser chamar uma função
    if "function_call" in resposta:
        try:
            nome_funcao = resposta["function_call"]["name"]
            argumentos_raw = resposta["function_call"]["arguments"]
            argumentos = json.loads(argumentos_raw)

            # Executa a função se estiver registrada
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

    # Se for só uma resposta normal
    return {
        "type": "response",
        "content": resposta.get("content", "")
    }
