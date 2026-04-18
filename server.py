import os
from mcp.server.fastmcp import FastMCP
from tools.base64_tools import encode_credentials, decode_credentials

mcp = FastMCP("Base64 Tools Server")

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


if __name__ == "__main__":
    transport = os.getenv("MCP_TRANSPORT", "stdio").lower()

    print(f"Starting MCP server with transport: {transport}")

    if transport in ["http", "https"]:
        import uvicorn
        # from fastapi import FastAPI
         # Create FastAPI app
        # app = FastAPI()
         # MCP app mounted inside FastAPI
        # mcp_app = mcp.streamable_http_app()
        app = mcp.streamable_http_app()   # 🔥 IMPORTANT
         # Mount MCP under /mcp
        # app.mount("/mcp", mcp_app)
         # ✅ ADD THIS: health check route
        # @app.get("/")
        # def root():
        #     return {
        #         "status": "Base64 MCP Server is running",
        #         "message": "Use /mcp for MCP communication"
        #     }
        port = int(os.environ.get("PORT", 8000))
        print("MCP HTTP server starting...")
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        mcp.run()