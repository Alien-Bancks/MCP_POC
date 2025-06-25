import requests
import json

mensagem = input("Digite sua pergunta: ")

payload = {
    "type": "chat.completion",
    "messages": [
        {"role": "user", "content": mensagem}
    ],
    "functions": [
        {
            "name": "somar",
            "description": "Soma dois números inteiros",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer"},
                    "b": {"type": "integer"}
                },
                "required": ["a", "b"]
            }
        }
    ]
}

resposta = requests.post("http://localhost:8000/chat", json=payload)

print("Resposta:", json.dumps(resposta.json(), indent=2, ensure_ascii=False))
