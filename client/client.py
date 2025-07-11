import asyncio
from fastmcp import Client
from fastmcp.client.logging import LogMessage


client = Client("/home/work02/Documentos/Aline/IA/MCP_POC/app/server.py")

# config = {
#     "local_server":{
#         "transport": "stdio",
#         "command": "python",
#         "args": ["../server.py", "--verbose"],
#         "env": {"DEBUG": "true"},
#         "cwd": "/home/work02/Documentos/Aline/IA/MCP_POC/app/server.py",
#     }
# }


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
 

        try:
            result = await client.call_tool("somar", {"a": 5, "b": 7})
            if hasattr(result, "data"):
                print("Result of the tool 'somar':", result.data)
            else:
                print("Result of the tool 'somar':", result)
        except Exception as e:
            print("Error executing the tool 'somar':", str(e))

        async def log_handler(message: LogMessage):
            print(f"Server log: {message.data}")

        async def progress_handler(progress: float, total: float | None, message: str | None):
            print(f"Progress: {progress}/{total} - {message}")        



if __name__ == "__main__":
    asyncio.run(main())


    
