from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp")

@mcp.tool()
def somar(a: int, b: int) -> int:
    """Soma dois números"""
    return a + b

@mcp.tool()
def subtrair(a: int, b: int) -> int:
    """Subtrai dois números"""
    return a - b    


@mcp.resource("frase://batata-doce")
def receita() -> str:
    """Retorna uma frase sobre batata doce"""
    return "Para fazer batata doce: asse no forno com azeite por 40 minutos."

if __name__ == "__main__":
    mcp.run(transport="stdio", port=3001)
