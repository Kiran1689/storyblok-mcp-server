import json
from typing import List, Optional, Any, Dict
from mcp.server.fastmcp import FastMCP
from httpx import AsyncClient
from utils.api import (
    build_management_url,
    get_management_headers,
    _handle_response,
    APIError,
)

def register_datasources(mcp: FastMCP, client: AsyncClient) -> None:
    @mcp.tool()
    async def retrieve_multiple_datasources(
        search: Optional[str] = None,
        by_ids: Optional[str] = None
    ) -> Any:
        
        """
        Retrieves multiple datasources from a specified Storyblok space.
        """
        try:
            params = {}
            if search:
                params["search"] = search
            if by_ids:
                params["by_ids"] = by_ids

            url = build_management_url(f"/datasources")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        

    @mcp.tool()
    async def retrieve_single_datasource(
        datasource_id: int
    ) -> Any:
        """
        Retrieves a single datasource from a specified Storyblok space.
        """
        try:
            url = build_management_url(f"/datasources/{datasource_id}")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def create_datasource(
        name: str,
        slug: str,
        dimensions: Optional[List[dict]] = None
    ) -> Any:
        """
        Creates a new datasource in a specified Storyblok space.
        """
        try:
            payload = {
                "datasource": {
                    "name": name,
                    "slug": slug,
                    "dimensions_attributes": dimensions or []
                }
            }

            url = build_management_url(f"/datasources")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def update_datasource(
        datasource_id: int,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        dimensions: Optional[List[dict]] = None
    ) -> Any:
        """
        Updates an existing datasource in a specified Storyblok space.
        """
        try:
            payload = {
                "datasource": {
                    "name": name,
                    "slug": slug,
                    "dimensions_attributes": dimensions or []
                }
            }

            # Remove any keys with None values
            payload = {k: v for k, v in payload.items() if v is not None}

            url = build_management_url(f"/datasources/{datasource_id}")
            resp = await client.put(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def delete_datasource(datasource_id: int) -> Any:
        """
        Deletes a datasource from a specified Storyblok space.
        """
        try:
            url = build_management_url(f"/datasources/{datasource_id}")
            resp = await client.delete(url, headers=get_management_headers())
            return {"isError": False, "content": [{"type": "text", "text": "DataSource deleted successfully"}]}
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}






