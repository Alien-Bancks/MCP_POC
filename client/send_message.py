import requests

# Esse script é só pra testar a comunicação com o servidor que criamos
# Ele envia uma pergunta pro servidor e mostra a resposta que voltar

mensagem = input("Digite sua pergunta: ")

resposta = requests.post("http://localhost:8000/chat", json={
    "type": "message",
    "content": mensagem
})

print("Resposta:", resposta.json())
