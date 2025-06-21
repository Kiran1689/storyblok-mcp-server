import json
from typing import Any, Optional, Dict
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import (
    build_management_url,
    get_management_headers,
    _handle_response,
    APIError,
)

def register_internal_tags(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_multiple_internal_tags(
        by_object_type: Optional[str] = None,
        search: Optional[str] = None
    ) -> Any:
        """
        Retrieves internal tags (asset/component) from a specified Storyblok space.

        - by_object_type: 'asset' or 'component' to filter tags.
        - search: optional substring to search by tag name.
        """
        try:
            params: Dict[str, Any] = {}
            if by_object_type:
                params["by_object_type"] = by_object_type
            if search:
                params["search"] = search

            url = build_management_url(f"/internal_tags/")
            resp = await client.get(
                url, params=params, headers=get_management_headers()
            )
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def create_internal_tag(
        name: str,
        object_type: Optional[str] = None
    ) -> Any:
        """
        Creates a new internal tag in a specified Storyblok space.

        :param name: Name of the internal tag.
        :param object_type: Optional. 'asset' or 'component'.
        """
        try:
            tag_obj: dict[str, Any] = {"name": name}
            if object_type:
                tag_obj["object_type"] = object_type

            payload = {"internal_tag": tag_obj}

            url = build_management_url(f"/internal_tags")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def update_internal_tag(
        internal_tag_id: int,
        name: Optional[str] = None,
        object_type: Optional[str] = None
    ) -> Any:
        """
        Updates an internal tag (asset/component) in a specified Storyblok space.

        :param space_id: ID of the Storyblok space.
        :param internal_tag_id: Numeric ID of the internal tag.
        :param name: Optional new name for the internal tag.
        :param object_type: Optional new object type ("asset" or "component").
        """
        try:
            tag_payload: dict[str, Any] = {}
            if name is not None:
                tag_payload["name"] = name
            if object_type is not None:
                tag_payload["object_type"] = object_type

            payload = {"internal_tag": tag_payload}

            url = build_management_url(
                f"/internal_tags/{internal_tag_id}"
            )
            resp = await client.put(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def delete_internal_tag(
        internal_tag_id: int
    ) -> Any:
        """
        Deletes an internal tag (asset/component) in a specified Storyblok space.

        :param internal_tag_id: Numeric ID of the internal tag to delete.
        """
        try:
            url = build_management_url(
                f"/internal_tags/{internal_tag_id}"
            )
            resp = await client.delete(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}