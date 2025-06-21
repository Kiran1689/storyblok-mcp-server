import json
from typing import Any, List, Optional
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import (
    build_management_url,
    get_management_headers,
    _handle_response,
    APIError,
)

def register_webhooks(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_multiple_webhooks(
        page: Optional[int] = 1,
        per_page: Optional[int] = 25
    ) -> Any:
        """
        Retrieves multiple webhook endpoints from a specified Storyblok space using the Management API.
        """
        try:
            params = {
                "page": page,
                "per_page": per_page
            }

            url = build_management_url(f"/webhook_endpoints/")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def retrieve_single_webhook(
        webhook_endpoint_id: int
    ) -> Any:
        """
        Retrieves a single webhook from a specified Storyblok space using the Management API.
        """
        try:
            url = build_management_url(f"/webhook_endpoints/{webhook_endpoint_id}")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def add_webhook(
        name: str,
        endpoint: str,
        actions: List[str],
        description: Optional[str] = None,
        secret: Optional[str] = None,
        activated: Optional[bool] = True
    ) -> Any:
        """
        Adds a new webhook to a specified Storyblok space using the Management API.
        """
        try:
            payload = {
                "webhook_endpoint": {
                    "name": name,
                    "description": description,
                    "endpoint": endpoint,
                    "secret": secret,
                    "actions": actions,
                    "activated": activated
                }
            }

            url = build_management_url("/webhook_endpoints/")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def update_webhook(
        webhook_endpoint_id: int,
        name: Optional[str] = None,
        endpoint: Optional[str] = None,
        actions: Optional[List[str]] = None,
        description: Optional[str] = None,
        secret: Optional[str] = None,
        activated: Optional[bool] = None
    ) -> Any:
        """
        Updates an existing webhook endpoint in a specified Storyblok space.
        """
        try:
            webhook_payload: dict[str, Any] = {}
            if name is not None:
                webhook_payload["name"] = name
            if endpoint is not None:
                webhook_payload["endpoint"] = endpoint
            if actions is not None:
                webhook_payload["actions"] = actions
            if description is not None:
                webhook_payload["description"] = description
            if secret is not None:
                webhook_payload["secret"] = secret
            if activated is not None:
                webhook_payload["activated"] = activated

            payload = {"webhook_endpoint": webhook_payload}

            url = build_management_url(
                f"/webhook_endpoints/{webhook_endpoint_id}"
            )
            resp = await client.put(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def delete_webhook(
        webhook_endpoint_id: int
    ) -> Any:
        """
        Deletes an existing webhook endpoint in a specified Storyblok space.
        """
        try:
            url = build_management_url(
                f"/webhook_endpoints/{webhook_endpoint_id}"
            )
            resp = await client.delete(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}