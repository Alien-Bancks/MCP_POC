from llama_cpp import Llama

llm = Llama(
    model_path="models/phi-3-mini.gguf",
    n_ctx=2048
)

def ask_model(prompt: str) -> str:
    """
    Roda o prompt no modelo e retorna a resposta 
    """
    resposta = llm.create_completion(
        prompt=prompt,
        max_tokens=256,
        stop=["user:", "system:"]
    )
    return resposta["choices"][0]["text"].strip()
