import requests 
from mcp.client import MCPClient


def main():

    client = MCPClient("http://localhost:3001")
    resposta = client.call("somar", a=1, b=2)
    print(f"Resposta da soma: {resposta}")



