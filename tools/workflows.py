from typing import Any, List, Optional
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import build_management_url, get_management_headers, _handle_response, APIError

def register_workflows(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_multiple_workflows(
        content_type: Optional[str] = None
    ) -> Any:
        """
        Retrieves all workflows in a Storyblok space via the Management API.
        Optionally filter by content type (e.g., 'page', 'article', etc.)
        """
        try:
            params: dict[str, Any] = {}
            if content_type is not None:
                params['content_type'] = content_type

            url = build_management_url("/workflows")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def retrieve_single_workflow(
        workflow_id: int
    ) -> Any:
        """
        Retrieves a single workflow by its ID in a Storyblok space via the Management API.
        """
        try:
            url = build_management_url(f"/workflows/{workflow_id}")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def create_workflow(
        name: str,
        content_types: List[str]
    ) -> Any:
        """
        Creates a new workflow in a Storyblok space via the Management API.
        """
        try:
            payload = {
                "workflow": {
                    "name": name,
                    "content_types": content_types
                }
            }

            url = build_management_url("/workflows")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    
    @mcp.tool()
    async def update_workflow(
        workflow_id: int,
        name: str,
        content_types: List[str]
    ) -> Any:
        """
        Updates an existing workflow in a Storyblok space via the Management API.
        """
        try:
            payload = {
                "workflow": {
                    "name": name,
                    "content_types": content_types
                }
            }

            url = build_management_url(f"/workflows/{workflow_id}")
            resp = await client.put(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def duplicate_workflow(
        workflow_id: int,
        name: str,
        content_types: List[str]
    ) -> Any:
        """
        Duplicates an existing workflow in a Storyblok space via the Management API.
        """
        try:
            payload = {
                "workflow": {
                    "name": name,
                    "content_types": content_types
                }
            }

            url = build_management_url(f"/workflows/{workflow_id}/duplicate")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def delete_workflow(
        workflow_id: int
    ) -> Any:
        """
        Deletes a workflow by its ID in a Storyblok space via the Management API.
        The default workflow cannot be deleted.
        """
        try:
            url = build_management_url(f"/workflows/{workflow_id}")
            resp = await client.delete(url, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}