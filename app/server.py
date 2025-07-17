from mcp.server.fastmcp import FastMCP
import whisper

mcp = FastMCP("mcp")


@mcp.tool()
def somar(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def subtrair(a: int, b: int) -> int:
    return a - b

@mcp.tool()
def multiplicar(a: int, b: int) -> int:
    return a * b

@mcp.tool()
def dividir(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("Não é possível dividir por zero.")
    return a / b

@mcp.tool()
def transcrever_audio(path: str) -> str:
    """
    Transcreve o áudio (ogg/wav) para texto usando Whisper.
    """
    model = whisper.load_model("medium")
    result = model.transcribe(path, language="pt")
    return result["text"]



if __name__ == "__main__":
    mcp.run(transport="stdio")
