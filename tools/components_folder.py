import json
import requests
from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import FastMCP
from httpx import AsyncClient
from config import API_ENDPOINTS
from utils.api import (
    build_management_url,
    get_management_headers,
    _handle_response,
    APIError,
)

def register_components_folder(mcp: FastMCP, client: AsyncClient) -> None:
    @mcp.tool()
    async def create_component_folder(
        name: str,
        parent_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Creates a new component folder.
        """
        try:
    
            url = build_management_url("/component_groups/")

            # Construct payload
            payload = {"component_group": {"name": name}}
            if parent_id is not None:
                payload["component_group"]["parent_id"] = parent_id

            resp = await client.post(
                url,
                headers=get_management_headers(),
                content=json.dumps(payload),
            )
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def update_component_folder(
        folder_id: str,
        name: Optional[str] = None,
        parent_id: Optional[int] = None,
        space_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Updates an existing component folder (component group).
        """
        try:
            
            url = build_management_url(f"/component_groups/{folder_id}")

            # Prepare the payload
            payload = {"component_group": {}}
            if name:
                payload["component_group"]["name"] = name
            if parent_id is not None:
                payload["component_group"]["parent_id"] = parent_id

            # Send the PUT request
            resp = await client.put(
                url,
                headers=get_management_headers(),
                content=json.dumps(payload)
            )
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def delete_component_folder(
        folder_id: str
    ) -> Dict[str, Any]:
        """
        Deletes a component folder (component group) by its ID.
        """
        try:
            
            url = build_management_url(f"/component_groups/{folder_id}")

            # Execute deletion
            resp = await client.delete(
                url,
                headers=get_management_headers(),
            )
            _handle_response(resp, url)  # Expecting 200 OK or 204 No Content

            return {"message": f"Component folder {folder_id} deleted successfully."}
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def fetch_component_folders(
        search: Optional[str] = None,
        with_parent: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Retrieves all component folders (non-paginated), with optional filtering.
        """
        try:
            
            url = build_management_url("/component_groups/")
            
            # Query params supported: search, with_parent
            params: Dict[str, Any] = {}
            if search:
                params["search"] = search
            if with_parent is not None:
                params["with_parent"] = with_parent

            resp = await client.get(
                url,
                headers=get_management_headers(),
                params=params
            )
            data = _handle_response(resp, url)
            groups = data.get("component_groups", [])

            return {
                "component_folders": groups,
                "count": len(groups)
            }
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def retrieve_single_component_folder(
        folder_id: str
    ) -> Dict[str, Any]:
        """
        Retrieves a single component folder (component group) by its ID.
        """
        try:
            
            url = build_management_url(f"/component_groups/{folder_id}")

            # Send the GET request
            resp = await client.get(
                url,
                headers=get_management_headers()
            )
            data = _handle_response(resp, url)

            return {"component_group": data.get("component_group") or data}

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
        


