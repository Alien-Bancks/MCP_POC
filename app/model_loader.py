from llama_cpp import Llama
import json

class LocalOpenAIClient:
    def __init__(self, model_path: str):
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,
        )

    class Responses:
        def __init__(self, llm):
            self.llm = llm

        def create(self, model: str, tools: list, input: str):
            prompt = f"""
            Você tem as seguintes ferramentas disponíveis: "somar", "subtrair", "multiplicar", "dividir".

            Responda APENAS com JSON neste formato:
            {{
            "tool": "nome_da_ferramenta",
            "args": {{"a": 1, "b": 2}}
            }}

            Pedido do usuário:
            "{input}"
            """
            response = self.llm.create_chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=256,
            )
            content = response["choices"][0]["message"]["content"].strip()

            resposta_limpa = extract_first_json(content)
            if not resposta_limpa:
                raise ValueError(f"Resposta inesperada do modelo: {content}")

            resposta_json = json.loads(resposta_limpa)
            tool = resposta_json.get("tool")
            args = resposta_json.get("args")

            class FakeToolCall:
                def __init__(self, name, arguments):
                    self.name = name
                    self.arguments = arguments

            class FakeResponse:
                def __init__(self, tool_calls):
                    self.tool_calls = tool_calls

            return FakeResponse([FakeToolCall(tool, args)])

    @property
    def responses(self):
        return self.Responses(self.llm)


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
    client = LocalOpenAIClient(model_path="./models/Qwen2.5-7B-Instruct-1M-Q3_K_L.gguf")

    response = client.responses.create(
        model="qwen",
        tools=[{"type": "mcp"}],  
        input=user_input,
    )

    tool_call = response.tool_calls[0]
    tool_name = tool_call.name
    args = tool_call.arguments

    print(f"\n=== DEBUG ===\nFerramenta: {tool_name}, Args: {args}\n=====")

    return tool_name, args

#exemplo
if __name__ == "__main__":
    tool, args = decide_tool("Quanto é 2 multiplicado por 6?")
    print(f"Decidido: {tool} com argumentos {args}")
