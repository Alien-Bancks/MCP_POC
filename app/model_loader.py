from llama_cpp import Llama

# Aqui a gente carrega o modelo local (Phi-3 Mini, por exemplo)
# Ele precisa estar no formato .gguf e no caminho indicado
llm = Llama(model_path="models/Phi-3-mini-4k-instruct-q4.gguf", n_ctx=2048)

# Essa função é a que usamos para conversar com o modelo
# A gente manda um texto (prompt) e ele responde com outro texto

def ask_model(prompt: str) -> str:
    resposta = llm.create_completion(prompt=prompt, max_tokens=256)
    return resposta["choices"][0]["text"].strip()

