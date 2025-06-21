import json
from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import FastMCP
from httpx import AsyncClient
from utils.api import (
    build_management_url,
    get_management_headers,
    _handle_response,
    APIError,
)

def register_datasource_entries(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_multiple_datasource_entries(
        datasource_id: Optional[int] = None,
        datasource_slug: Optional[str] = None,
        dimension: Optional[str] = None
    ) -> Any:
        """
        Retrieves multiple datasource entries from a specified Storyblok space.
        """
        try:
            if not (datasource_id or datasource_slug):
                raise ValueError("At least one of 'datasource_id' or 'datasource_slug' must be provided.")

            params = {}
            if datasource_id:
                params["datasource_id"] = datasource_id
            if datasource_slug:
                params["datasource_slug"] = datasource_slug
            if dimension:
                params["dimension"] = dimension

            url = build_management_url(f"/datasource_entries/")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        except ValueError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}


    @mcp.tool()
    async def retrieve_single_datasource_entry(
        datasource_entry_id: int
    ) -> Any:
        """
        Retrieves a single datasource entry via the Storyblok Management API.
        """
        try:
            url = build_management_url(
                f"/datasource_entries/{datasource_entry_id}"
            )
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        

    @mcp.tool()
    async def create_datasource_entry(
        datasource_id: int,
        name: str,
        value: str
    ) -> Any:
        """
        Creates a new datasource entry in a specified Storyblok space.
        """
        try:
            payload = {
                "datasource_entry": {
                    "datasource_id": datasource_id,
                    "name": name,
                    "value": value
                }
            }

            url = build_management_url(f"/datasource_entries")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        

    @mcp.tool()
    async def update_datasource_entry(
        datasource_entry_id: int,
        name: Optional[str] = None,
        value: Optional[str] = None,
        dimension_value: Optional[str] = None,
        dimension_id: Optional[int] = None
    ) -> Any:
        """
        Updates an existing datasource entry in a specified Storyblok space.
        """
        try:
            # At minimum, one of 'name', 'value', or 'dimension_value' must be provided
            if not any([name, value, dimension_value]):
                return {
                    "isError": True,
                    "content": [{"type": "text", "text": "At least one of name, value, or dimension_value must be provided"}]
                }

            payload: dict[str, Any] = {"datasource_entry": {}}
            if name is not None:
                payload["datasource_entry"]["name"] = name
            if value is not None:
                payload["datasource_entry"]["value"] = value
            if dimension_value is not None:
                payload["datasource_entry"]["dimension_value"] = dimension_value
                if dimension_id is None:
                    return {
                        "isError": True,
                        "content": [{"type": "text", "text": "dimension_id must be provided when setting dimension_value"}]
                    }
                payload["dimension_id"] = dimension_id

            url = build_management_url(f"/datasource_entries/{datasource_entry_id}")
            resp = await client.put(
                url,
                json=payload,
                headers=get_management_headers()
            )
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def delete_datasource_entry(
        datasource_entry_id: int
    ) -> Any:
        """
        Deletes a datasource entry from a specified Storyblok space using the Management API.
        """
        try:
            url = build_management_url(
                f"/datasource_entries/{datasource_entry_id}"
            )
            resp = await client.delete(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

