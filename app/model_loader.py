from llama_cpp import Llama
import json

# Aqui a gente carrega o modelo local (Phi-3 Mini, por exemplo)
# Ele precisa estar no formato .gguf e no caminho indicado
llm = Llama(model_path="models/Phi-3-mini-4k-instruct-q4.gguf", n_ctx=2048)

# Essa função é a que usamos pra conversar com o modelo (versão MCP)
# Ela recebe uma lista de mensagens e as funções disponíveis
def ask_model(messages: list, functions: list = []) -> dict:
    # Prompt de sistema explicando que ele pode chamar funções
    prompt = "Você é um assistente que pode usar funções se necessário.\n"

    if functions:
        prompt += "\nFunções disponíveis:\n"
        for func in functions:
            prompt += f"\n- {func['name']}: {func.get('description', '')}"
            prompt += f"\nParâmetros: {json.dumps(func['parameters'], ensure_ascii=False)}\n"

    # Junta o histórico de mensagens no estilo: user: ..., assistant: ...
    prompt += "\nHistórico:\n"
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content")
        prompt += f"{role}: {content}\n"
    prompt += "assistant:"

    # Envia pro modelo
    resposta = llm.create_completion(prompt=prompt, max_tokens=256)
    texto = resposta["choices"][0]["text"].strip()

    # Tenta extrair uma chamada de função MCP (se o modelo devolver JSON)
    try:
        resposta_json = json.loads(texto)
        if "function_call" in resposta_json:
            return resposta_json  # Resposta no formato MCP
    except:
        pass

    # Se não for chamada de função, devolve como resposta normal
    return {
        "content": texto
    }
