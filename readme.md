# PoC: Comunicação com IA local via MCP

Prova de conceito que demonstra como comunicar-se com um modelo de IA local usando o protocolo MCP

---

## Estrutura do projeto

mcp_poc/
├── app/
│ ├── server.py 
│ └── model_loader.py 
├── client/
│ └── client.py 
├── models/
│ └── phi-3-mini.gguf 
├── requirements.txt 

yaml
Copy
Edit

---

## Requisitos

- Python 3.8 ou superior  
- Biblioteca `llama-cpp-python`  
- Modelo `.gguf` 
- MCP client instalado (via requirements)

---

## Como rodar

1. Clone o repositório e entre na pasta:

```bash
git clone https://github.com/Alien-Bancks/MCP_POC.git
cd MCP_POC
Crie e ative ambiente virtual


python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
Instale dependências:


pip install -r requirements.txt
Baixe o modelo Phi-3 Mini .gguf e coloque em models/ com o nome:


models/phi-3-mini.gguf
Fonte: https://huggingface.co/microsoft/Phi-3-mini-4k-instruct

Inicie o servidor MCP:


python app/server.py
Em outro terminal, rode o cliente:


python client/client.py