import json
from typing import Any, Optional, Dict, List, Union
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import (
    build_management_url,
    get_management_headers,
    _handle_response,
    APIError,
)


def register_tags(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_multiple_tags(
        search: Optional[str] = None
    ) -> Any:
        """
        Retrieves multiple tags from a specified Storyblok space using the Management API.
        """
        try:
            params: dict[str, Any] = {}
            if search is not None:
                params["search"] = search

            url = build_management_url(f"/tags/")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}


    @mcp.tool()
    async def create_tag(
        name: str,
        story_id: Optional[int] = None
    ) -> Any:
        """
        Creates a new tag in a Storyblok space via the Management API.
        """
        try:
            payload: Dict[str, Any] = {"tag": {"name": name}}
            if story_id is not None:
                payload["tag"]["story_id"] = story_id

            url = build_management_url(f"/tags/")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}


    @mcp.tool()
    async def update_tag(
        tag_id: str,
        new_name: str
    ) -> Any:
        """
        Updates the name of an existing tag in a Storyblok space.

        """
        try:
            payload = {
                "id": tag_id,
                "tag": {"name": new_name}
            }

            url = build_management_url(f"/tags/{tag_id}")
            resp = await client.put(url, json=payload, headers=get_management_headers())
            if resp.status_code == 204:
                return {"isError": False, "content": [{"type": "text", "text": f"Tag updated successfully."}]}
            else:
                return {"isError": True, "content": [{"type": "text", "text": f"Failed to update tag. Status code: {resp.status_code}"}]}

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}


    @mcp.tool()
    async def delete_tag(id: str) -> Any:
        """Deletes a tag from Storyblok."""
        try:
            url = build_management_url(f"/tags/{id}")
            resp = await client.delete(url, headers=get_management_headers())
            if resp.status_code == 204:
                return {"isError": False, "content": [{"type": "text", "text": f"Tag deleted successfully."}]}
            else:
                return {"isError": True, "content": [{"type": "text", "text": f"Failed to delete tag. Status code: {resp.status_code}"}]}
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        

    @mcp.tool()
    async def tag_bulk_association(
        stories: List[Dict[str, Any]]
    ) -> Any:
        """
        Adds tags to multiple stories in a Storyblok space.
        """
        try:
            payload = {
                "tags": {
                    "stories": stories
                }
            }

            url = build_management_url(f"/tags/bulk_association")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

