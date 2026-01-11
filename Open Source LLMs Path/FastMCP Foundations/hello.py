from fastmcp import FastMCP

mcp = FastMCP("Hello World Server")

@mcp.tool
def say_hello(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    print("🚀 Starting MCP server at http://localhost:8000/mcp")
    mcp.run(transport="http", port=8000)

