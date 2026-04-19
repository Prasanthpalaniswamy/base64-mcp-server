import asyncio
import httpx
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession
import json

async def main():
    # Remove the manual Host header entirely
    headers = {} 

    # Keep your factory, but let it be simple
    def httpx_client_factory(headers=None, timeout=None, auth=None):
            return httpx.AsyncClient(
                headers=headers, # Use the headers passed by the SDK
                timeout=timeout,
                auth=auth,
                follow_redirects=True,
                http2=False, # Crucial
                # This forces the client to be less aggressive with connection reuse
                limits=httpx.Limits(max_connections=10, max_keepalive_connections=0),
            )

    headers_override = headers

    async with streamablehttp_client(
        "https://base64-mcp-server.onrender.com/mcp",
        headers=headers,
        httpx_client_factory=httpx_client_factory,
    ) as streams:

        reader = streams[0]
        writer = streams[1]
        # ignore streams[2] → it's get_session_id

        async with ClientSession(reader, writer) as client:

            await client.initialize()

            tools = await client.list_tools()
            print("Available tools:", tools)
            encoded = await client.call_tool(
            "encode_credentials_tool",
            {"login": "admin", "password": "1234"}
            )

            encoded_value = encoded.structuredContent["result"]

            print("Encoded:", encoded_value)

            decoded_response = await client.call_tool(
                "decode_credentials_tool",
                {"encoded_data": encoded_value}
            )

            decoded_text = decoded_response.content[0].text

            decoded_value = json.loads(decoded_text)["result"]

            print("Decoded:", decoded_value)

asyncio.run(main())