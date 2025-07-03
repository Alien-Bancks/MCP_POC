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
            "name": "obter_previsao_tempo",
            "description": "Retorna a previsão do tempo para uma cidade.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cidade": {
                        "type": "string",
                        "description": "nome da cidade"
                    },
                    "estado": {
                        "type": "string",
                        "description": "sigla do estado"
                    }
                },
                "required": ["cidade", "estado"]
            }
        }
    ]
}



resposta = requests.post("http://localhost:8000/chat", json=payload)

print("\nResposta:\n")
print(json.dumps(resposta.json(), indent=2, ensure_ascii=False))
