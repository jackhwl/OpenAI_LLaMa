import asyncio
from fastmcp import Client

async def main():
    async with Client("http://127.0.0.1:8000/mcp") as c:
        result = await c.call_tool("say_hello", {"name": "World"})
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
