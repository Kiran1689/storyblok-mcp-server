from typing import Any, Optional, Dict
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import build_management_url, get_management_headers, _handle_response, APIError

def register_presets(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_multiple_presets(
        component_id: Optional[int] = None
    ) -> Any:
        """
        Retrieves multiple presets from a Storyblok space using the Management API.
        Optionally filters by component_id.
        """
        try:
            params: Dict[str, Any] = {}
            if component_id is not None:
                params["component_id"] = component_id

            url = build_management_url("/presets/")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def retrieve_single_preset(
        preset_id: int
    ) -> Any:
        """
        Retrieves a single preset from a Storyblok space using the Management API.
        """
        try:
            url = build_management_url(f"/presets/{preset_id}")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def create_preset(
        name: str,
        component_id: int,
        preset: Dict[str, Any],
        image: Optional[str] = None,
        color: Optional[str] = None,
        icon: Optional[str] = None,
        description: Optional[str] = None
    ) -> Any:
        """
        Creates a new preset in a Storyblok space via the Management API.
        """
        try:
            payload: Dict[str, Any] = {
                "preset": {
                    "name": name,
                    "component_id": component_id,
                    "preset": preset,
                }
            }
            # Attach optional fields if provided
            if image is not None:
                payload["preset"]["image"] = image
            if color is not None:
                payload["preset"]["color"] = color
            if icon is not None:
                payload["preset"]["icon"] = icon
            if description is not None:
                payload["preset"]["description"] = description

            url = build_management_url("/presets/")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def update_preset(
        preset_id: int,
        name: Optional[str] = None,
        component_id: Optional[int] = None,
        preset: Optional[Dict[str, Any]] = None,
        image: Optional[str] = None,
        color: Optional[str] = None,
        icon: Optional[str] = None,
        description: Optional[str] = None
    ) -> Any:
        """
        Updates an existing preset in a Storyblok space via the Management API.
        """
        try:
            payload: Dict[str, Any] = {"preset": {}}
            
            if name is not None:
                payload["preset"]["name"] = name
            if component_id is not None:
                payload["preset"]["component_id"] = component_id
            if preset is not None:
                payload["preset"]["preset"] = preset
            if image is not None:
                payload["preset"]["image"] = image
            if color is not None:
                payload["preset"]["color"] = color
            if icon is not None:
                payload["preset"]["icon"] = icon
            if description is not None:
                payload["preset"]["description"] = description

            url = build_management_url(f"/presets/{preset_id}")
            resp = await client.put(url, json=payload, headers=get_management_headers())
            return {"isError": False, "content": [{"type": "text", "text": "Preset updated successfully"}]}

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def delete_preset(
        preset_id: int
    ) -> Any:
        """
        Deletes a preset from a Storyblok space using the Management API.

        - preset_id: Numeric ID of the preset to delete.
        """
        try:
            url = build_management_url(f"/presets/{preset_id}")
            resp = await client.delete(url, headers=get_management_headers())
            return {"isError": False, "content": [{"type": "text", "text": "Preset deleted successfully"}]}
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}