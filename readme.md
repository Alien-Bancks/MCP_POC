POC: Comunicação com IA usando MCP e Function Calling

Este projeto é uma **prova de conceito (PoC)** bem simples que mostra como um sistema pode **se comunicar com um modelo de IA local (Phi-3 Mini)** usando um **padrão de arquitetura chamado MCP (Model Context Protocol)**.

A ideia é simular uma conversa com IA, onde:

- O cliente envia uma mensagem (pergunta)
- O servidor repassa para o modelo
- A IA responde
- E, se a IA quiser executar uma função, ela usa um formato padronizado (**function calling**)

---

## O que há no projeto:

- Como funciona a comunicação cliente-servidor com IA
- Como usar um modelo local (Phi-3 Mini)
- Como usar o padrão MCP para padronizar as mensagens
- Como simular "function calling" \*\* de forma simples

---

## Como rodar o projeto

### 1. Clone o repositório e entre na pasta:

```bash
git clone <url-do-repo>
cd poc-mcp
```

### 2. (Opcional, mas recomendado) Crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate        # No Linux/macOS
venv\Scripts\activate           # No Windows
```

### 3. Instale as dependências:

```bash
pip install -r requirements.txt
```

### 4. Baixe o modelo Phi-3 Mini no formato `.gguf`

- Link: Phi-3 Mini no HuggingFace

- Coloque o arquivo `.gguf` na pasta `models/` e renomeie como:

  ```
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

## Exemplo de uso:

### Mensagem normal:

```
Digite sua pergunta: Qual é a capital do Brasil?
Resposta: Brasília.
```

### Chamada de função:

```
Digite sua pergunta: CALL: {"function": "somar", "args": {"a": 2, "b": 3}}
Resposta: 5
```

---

- As mensagens seguem um padrão definido (o protocolo **MCP**), com campos `type` e `content`.
- O servidor entende quando a IA quer chamar uma função e executa com segurança.
- É possível expandir facilmente com mais funções, mais modelos ou integração com **front-end**.

---

## Formatos usados (MCP simplificado)

### Mensagem enviada:

```json
{
  "type": "message",
  "content": "Qual é a capital do Brasil?"
}
```

### Resposta simples:

```json
{
  "type": "response",
  "content": "Brasília."
}
```

### Resposta com function calling:

```json
{
  "type": "function_result",
  "content": "5"
}
```

### Erro:

```json
{
  "type": "error",
  "content": "Função não encontrada"
}
```