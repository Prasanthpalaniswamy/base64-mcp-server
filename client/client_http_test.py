import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession
import json

async def main():
    # async with streamablehttp_client("http://127.0.0.1:8000/mcp") as streams:
    async with streamablehttp_client("https://base64-mcp-server.onrender.com") as streams:

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