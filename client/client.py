import asyncio
from fastmcp import Client
from fastmcp.client.logging import LogMessage
from app.model_loader import decide_tool  

SERVER_PATH = "/home/work02/Documentos/Aline/IA/MCP_POC/app/server.py"

client = Client(SERVER_PATH)

async def main():
    async with client:
        await client.ping()
        print("Server is reachable")

        tools = await client.list_tools()
        if tools:
            print("Available tools:")
            for tool in tools:
                print(f" {tool.name}: {tool.description}")
        else:
            print("No tools available.")

        user_input = input("Digite sua pergunta ou caminho do áudio (.ogg/.wav): ")

        if user_input.endswith(".ogg") or user_input.endswith(".wav"):
            tool = "transcrever_audio"
            args = {"path": user_input}
        else:

      
            try:
                tool, args = decide_tool(user_input)
            except ValueError as e:
                print("Erro ao decidir tool:", e)
                return

        try:
            result = await client.call_tool(tool, args)
            if hasattr(result, "data"):
                print(f"Result of the tool '{tool}':", result.data)
            else:
                print(f"Result of the tool '{tool}':", result)
        except Exception as e:
            print(f"Error executing the tool '{tool}':", str(e))

        async def log_handler(message: LogMessage):
            print(f"Server log: {message.data}")

        async def progress_handler(progress: float, total: float | None, message: str | None):
            print(f"Progress: {progress}/{total} - {message}")

if __name__ == "__main__":
    asyncio.run(main())
