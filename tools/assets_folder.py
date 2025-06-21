import json
from typing import Optional, Dict, Any, List
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import (
    build_management_url,
    get_management_headers,
    _handle_response,
    APIError,
)


def register_assets_folder(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_asset_folders(
        search: Optional[str] = None,
        with_parent: Optional[int] = None,
        by_ids: Optional[List[int]] = None,
        by_uuids: Optional[List[str]] = None
    ) -> Any:
        """
        Retrieve a list of asset folders from the current Storyblok space.

        Parameters:
            search (Optional[str]): A search query to filter asset folders by name.
            with_parent (Optional[int]): ID of the parent folder to filter results.
            by_ids (Optional[List[int]]): Specific folder IDs to fetch.
            by_uuids (Optional[List[str]]): Specific folder UUIDs to fetch.

        Returns:
            Any: The API response with a list of asset folders or an error message.
        """
        try:
            params: dict[str, Any] = {}
            if search:
                params["search"] = search
            if with_parent is not None:
                params["with_parent"] = with_parent
            if by_ids:
                params["by_ids"] = ",".join(str(i) for i in by_ids)
            if by_uuids:
                params["by_uuids"] = ",".join(by_uuids)

            url = build_management_url("/asset_folders/")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def fetch_asset_folder(
        folder_id: str
    ) -> Dict[str, Any]:
        """
        Fetch details of a specific asset folder by its ID.

        Parameters:
            folder_id (str): ID of the asset folder to retrieve.

        Returns:
            Dict[str, Any]: The API response containing the folder data or an error message.
        """
        try:
            url = build_management_url(f"/asset_folders/{folder_id}")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def create_asset_folder(
        name: str,
        parent_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create a new asset folder in the current Storyblok space.

        Parameters:
            name (str): Name of the new asset folder.
            parent_id (Optional[int]): ID of the parent folder (if nested).

        Request Body Example:
            {
                "asset_folder": {
                    "name": "My Folder",
                    "parent_id": 123
                }
            }

        Returns:
            Dict[str, Any]: The API response with created folder info or an error message.
        """
        try:
            url = build_management_url("/asset_folders/")
            payload = {"asset_folder": {"name": name}}
            if parent_id is not None:
                payload["asset_folder"]["parent_id"] = parent_id

            resp = await client.post(
                url,
                headers=get_management_headers(),
                content=json.dumps(payload),
            )
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def update_asset_folder(
        folder_id: str,
        name: Optional[str] = None,
        parent_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Update an existing asset folder's name or parent in the current Storyblok space.

        Parameters:
            folder_id (str): ID of the folder to update.
            name (Optional[str]): New name for the folder.
            parent_id (Optional[int]): New parent folder ID.

        Request Body Example:
            {
                "asset_folder": {
                    "name": "Updated Folder",
                    "parent_id": 456
                }
            }

        Returns:
            Dict[str, Any]: A success message or error content depending on response.
        """
        try:
            url = build_management_url(f"/asset_folders/{folder_id}")
            payload = {"asset_folder": {}}
            if name:
                payload["asset_folder"]["name"] = name
            if parent_id is not None:
                payload["asset_folder"]["parent_id"] = parent_id

            resp = await client.put(
                url,
                headers=get_management_headers(),
                content=json.dumps(payload)
            )
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def delete_asset_folder(folder_id: str) -> Dict[str, Any]:
        """
        Delete an asset folder from the current Storyblok space.

        Parameters:
            folder_id (str): ID of the folder to delete.

        Returns:
            Dict[str, Any]: A success message or error content depending on response.
        """
        try:
            url = build_management_url(f"/asset_folders/{folder_id}")
            resp = await client.delete(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
