from llama_cpp import Llama
import json

llm = Llama(model_path="models/Phi-3-mini-4k-instruct-q4.gguf", n_ctx=2048)

def ask_model(messages: list, functions: list = []) -> dict:
    prompt = (
        "Você é um assistente de IA local chamado Phi-3.\n"
        "Responda de forma direta, sem formatação ou explicação.\n"
        "Se precisar usar função, retorne APENAS este JSON:\n"
        '{ "function_call": { "name": "nome", "arguments": { "param": "valor" } } }\n'
        "NÃO retorne texto junto. NÃO explique. Só JSON ou só texto puro."
    )

    if functions:
        prompt += "\nFunções disponíveis:\n"
        for f in functions:
            prompt += f"- " + f["name"] + ": " + f.get("description", "") + "\n"
            prompt += f"  Parâmetros: {json.dumps(f['parameters'], ensure_ascii=False)}\n"

    for msg in messages:
        prompt += f"{msg['role']}: {msg['content']}\n"
    prompt += "assistant: "

    output = llm.create_completion(
        prompt=prompt,
        max_tokens=512,
        stop=["user:", "system:"]
    )

    texto = output["choices"][0]["text"].strip()

    try:
        parsed = json.loads(texto)
        if "function_call" in parsed:
            return {
                "model": "phi-3-mini",
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": None,
                            "function_call": parsed["function_call"]
                        }
                    }
                ]
            }
    except Exception:
        pass

    return {
        "model": "phi-3-mini",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": texto
                }
            }
        ]
    }
