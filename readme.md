# PoC: Comunicação com IA local via MCP e Function Calling

Este projeto é uma **prova de conceito (PoC)** que demonstra como se comunicar com um modelo de IA local (Phi-3 Mini) usando o protocolo **MCP (Model Context Protocol)**, incluindo suporte real à funcionalidade de **Function Calling**, seguindo o padrão oficial usado por APIs como a da OpenAI.

---

## O que esta PoC mostra:

- Como um cliente envia mensagens no formato MCP  
- Como um servidor FastAPI interpreta essas mensagens  
- Como o modelo Phi-3 Mini responde com texto direto ou `function_call`  
- Como detectar chamadas de função (`function_call`) e tratá-las  
- Como manter separação entre camada de IA e lógica de execução  

---

## Estrutura do Projeto

```
poc-mcp/
├── app/
│   ├── mcp_server.py        # Servidor FastAPI que lida com mensagens MCP
│   └── model_loader.py      # Integração com o modelo Phi-3 local
├── client/
│   └── send_message.py      # Cliente simples que envia mensagens
├── models/
│   └── phi-3-mini.gguf      # (você deve baixar e colocar aqui)
├── requirements.txt
```


## Requisitos

- Python 3.8+
- FastAPI
- llama-cpp-python
- Modelo `.gguf` do Phi-3 Mini

---

## Como rodar o projeto

### 1. Clone o repositório:

```bash
git clone https://github.com/Alien-Bancks/mcp-function-calling-poc.git
cd poc-mcp
```

### 2. (Recomendado) Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows
```

### 3. Instale as dependências:

```bash
pip install -r requirements.txt
```

### 4. Baixe o modelo Phi-3 Mini (.gguf):

- Vá para: [https://huggingface.co/microsoft/Phi-3-mini-4k-instruct](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct)
- Baixe a versão `.gguf` (ex: `phi-3-mini-4k-instruct-q4.gguf`)
- Coloque na pasta `models/` com o nome:

```bash
models/phi-3-mini.gguf
```

### 5. Inicie o servidor:

```bash
uvicorn app.mcp_server:app --reload
```

### 6. Em outro terminal, execute o cliente:

```bash
python client/send_message.py
```

---

## Exemplo de uso

### Pergunta comum:

```
Digite sua pergunta: Qual é a capital do Brasil?
```

**Resposta:**

```json
{
  "type": "chat.completion",
  "content": "Brasília."
}
```

---

### Pergunta que aciona function_call:

```
Digite sua pergunta: Qual é a previsão do tempo em Curitiba, PR?
```

**Resposta:**

```json
{
  "type": "function_call",
  "function_call": {
    "name": "obter_previsao_tempo",
    "arguments": {
      "cidade": "Curitiba",
      "estado": "PR"
    }
  }
}
```

---

## Estrutura MCP usada

### Mensagem enviada:

```json
{
  "type": "chat.completion",
  "messages": [
    {
      "role": "user",
      "content": "Qual é a previsão do tempo em Curitiba, PR?"
    }
  ],
  "functions": [
    {
      "name": "obter_previsao_tempo",
      "description": "Retorna a previsão do tempo para uma cidade.",
      "parameters": {
        "type": "object",
        "properties": {
          "cidade": {
            "type": "string"
          },
          "estado": {
            "type": "string"
          }
        },
        "required": ["cidade", "estado"]
      }
    }
  ]
}
```

---

### Resposta com texto direto (sem função):

```json
{
  "type": "chat.completion",
  "content": "A capital do Brasil é Brasília."
}
```

---

### Resposta com function_call:

```json
{
  "type": "function_call",
  "function_call": {
    "name": "obter_previsao_tempo",
    "arguments": {
      "cidade": "Curitiba",
      "estado": "PR"
    }
  }
}
```

---

### (Opcional) Simulação de function_response:

```json
{
  "type": "function_response",
  "function_response": {
    "name": "obter_previsao_tempo",
    "arguments": {
      "cidade": "Curitiba",
      "estado": "PR"
    },
    "result": "Hoje em Curitiba está ensolarado com máxima de 26°C."
  }
}
```

---



