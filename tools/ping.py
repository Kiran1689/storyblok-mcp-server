from mcp.server.fastmcp import FastMCP
from httpx import AsyncClient, HTTPStatusError
from config import Config, API_ENDPOINTS

cfg = Config()

def register_ping(mcp: FastMCP, client: AsyncClient) -> None:
    # Tool: ping
    @mcp.tool()
    async def ping() -> dict:
        """
        Checks server health and Storyblok API connectivity.
        """
        try:
            url = f"https://mapi.storyblok.com/?token={cfg.management_token}"
            resp = await client.get(url)

            if 200 <= resp.status_code < 300:
                return {
                    "content": [
                        {"type": "text", "text": "Server is running and Storyblok API is reachable."}
                    ]
                }
            else:
                error_body = resp.text
                return {
                    "isError": True,
                    "errorCode": "STORYBLOK_API_ERROR",
                    "errorMessage": f"Storyblok API returned an error. Details: Status: {resp.status_code} {resp.reason_phrase}, Body: {error_body}",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Error: STORYBLOK_API_ERROR - Storyblok API returned an error. Details: Status: {resp.status_code} {resp.reason_phrase}, Body: {error_body}"
                        }
                    ]
                }
        except Exception as e:
            return {
                "isError": True,
                "content": [
                    {
                        "type": "text",
                        "text": f"Error: {str(e)}"
                    }
                ]
            }
