import os
from contextlib import asynccontextmanager
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from mcp.server.fastmcp import FastMCP
from tools.base64_tools import encode_credentials, decode_credentials

mcp = FastMCP("Base64 Tools Server", host="0.0.0.0")


@mcp.tool(description=(
    "Convert login credentials into Base64 format.\n\n"
    "Input:\n"
    "- login: string (username)\n"
    "- password: string\n\n"
    "Output:\n"
    "- Base64 encoded string of 'login:password'\n\n"
    "Use case:\n"
    "- Preparing credentials for HTTP Basic Authentication headers."
))
def encode_credentials_tool(login: str, password: str) -> str:
    return encode_credentials(login, password)


@mcp.tool(description=(
    "Decode Base64-encoded credentials.\n\n"
    "Input:\n"
    "- encoded_data: Base64 string representing 'login:password'\n\n"
    "Output:\n"
    "- JSON object with:\n"
    "  - login: string\n"
    "  - password: string\n\n"
    "Use case:\n"
    "- Extracting username and password from encoded credentials."
))
def decode_credentials_tool(encoded_data: str) -> dict:
    return decode_credentials(encoded_data)


async def healthcheck(request):
    return JSONResponse({
        "status": "ok",
        "message": "Base64 MCP Server is running",
        "mcp_endpoint": "/mcp"
    })


mcp_app = mcp.streamable_http_app()


@asynccontextmanager
async def lifespan(app):
    async with mcp.session_manager.run():
        yield

app = Starlette(routes=[
    Route("/health", healthcheck),
    Mount("/", app=mcp_app),
], lifespan=lifespan)


if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "http").lower()
    print(f"Starting MCP server with transport: {transport}")

    if transport in ["http", "https"]:
        import uvicorn

        port = int(os.environ.get("PORT", 8000))
        print(f"MCP HTTP server starting on port {port}...")

        uvicorn.run(
            "server:app",
            host="0.0.0.0",
            port=port,
            proxy_headers=True,
            forwarded_allow_ips="*",
        )
    else:
        mcp.run()
