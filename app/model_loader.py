from llama_cpp import Llama
import json


llm = Llama(
    model_path="./models/Qwen2.5-7B-Instruct-1M-Q3_K_L.gguf",
    n_ctx=2048,
)


def ask_model(prompt: str) -> str:
    response = llm.create_chat_completion(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        max_tokens=256,
    )
    return response["choices"][0]["message"]["content"].strip()


def extract_first_json(text: str) -> str:
    stack = []
    start_idx = None
    for i, c in enumerate(text):
        if c == '{':
            if start_idx is None:
                start_idx = i
            stack.append(c)
        elif c == '}' and stack:
            stack.pop()
            if not stack:
                return text[start_idx:i+1]
    return None


def decide_tool(user_input: str) -> tuple[str, dict]:
    prompt = f"""
Responda APENAS com um JSON válido, sem explicações.

As ferramentas disponíveis são: "somar" e "subtrair".

Formato esperado:
{{
  "tool": "nome_da_ferramenta",
  "args": {{"a": 1, "b": 2}}
}}

Aqui está o pedido do usuário:
"{user_input}"
"""
    resposta_texto = ask_model(prompt)
    print("\n=== DEBUG ===\n", resposta_texto, "\n=====\n")

    resposta_limpa = extract_first_json(resposta_texto)
    if not resposta_limpa:
        raise ValueError("O modelo não retornou JSON reconhecível.")

    try:
        resposta_json = json.loads(resposta_limpa)
        return resposta_json["tool"], resposta_json["args"]
    except Exception as e:
        raise ValueError(f"Erro ao interpretar a resposta JSON: {e}")

