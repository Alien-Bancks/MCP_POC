from fastapi import FastAPI, Request
from app.model_loader import ask_model
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
    functions = data.get("functions", [])

    resposta = ask_model(messages=messages, functions=functions)
    message = resposta.get("choices", [{}])[0].get("message", {})

    if "function_call" in message:
        return {
            "type": "function_call",
            "function_call": message["function_call"]
        }

    return {
        "type": "chat.completion",
        "content": message.get("content", "")
    }

@app.get("/")
async def root():
    return {"message": "Servidor rodando. Use o endpoint /chat para interagir."}
