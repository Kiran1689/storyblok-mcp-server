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

def register_space_roles(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def fetch_space_roles(
        search: Optional[str] = None,
        by_ids: Optional[List[int]] = None
    ) -> Any:
        """
        Retrieves multiple space roles for a given space.
        """
        try:
            params: dict[str, Any] = {}
            if search:
                params["search"] = search
            if by_ids:
                params["by_ids"] = ",".join(str(i) for i in by_ids)

            url = build_management_url(f"/space_roles/")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}


    @mcp.tool()
    async def get_space_role(
        space_role_id: int
    ) -> Any:
        """
        Retrieve a single space role by ID via the Storyblok Management API.
        """
        try:
            url = build_management_url(f"/space_roles/{space_role_id}")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {
                "isError": True,
                "content": [{"type": "text", "text": str(e)}]
            }


    @mcp.tool()
    async def create_space_role(
        role_name: str,
        allowed_paths: Optional[List[int]] = None,
        field_permissions: Optional[List[str]] = None,
        readonly_field_permissions: Optional[List[str]] = None,
        permissions: List[str] = None,
        subtitle: Optional[str] = None,
        datasource_ids: Optional[List[int]] = None,
        component_ids: Optional[List[int]] = None,
        branch_ids: Optional[List[int]] = None,
        allowed_languages: Optional[List[str]] = None,
        asset_folder_ids: Optional[List[int]] = None
    ) -> Any:
        """
        Creates a new custom space role with specific permissions.
        """
        try:
            payload: Dict[str, Any] = {
                "space_role": {
                    "role": role_name,
                    "permissions": permissions
                }
            }

            sr = payload["space_role"]

            if allowed_paths is not None:
                sr["allowed_paths"] = allowed_paths
            if field_permissions is not None:
                sr["field_permissions"] = field_permissions
            if readonly_field_permissions is not None:
                sr["readonly_field_permissions"] = readonly_field_permissions
            if subtitle is not None:
                sr["subtitle"] = subtitle
            if datasource_ids is not None:
                sr["datasource_ids"] = datasource_ids
            if component_ids is not None:
                sr["component_ids"] = component_ids
            if branch_ids is not None:
                sr["branch_ids"] = branch_ids
            if allowed_languages is not None:
                sr["allowed_languages"] = allowed_languages
            if asset_folder_ids is not None:
                sr["asset_folder_ids"] = asset_folder_ids

            url = build_management_url(f"/space_roles/")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def update_space_role(
        space_role_id: int,
        *,
        allowed_paths: Optional[List[int]] = None,
        field_permissions: Optional[List[str]] = None,
        readonly_field_permissions: Optional[List[str]] = None,
        permissions: Optional[List[str]] = None,
        role_name: Optional[str] = None,
        subtitle: Optional[str] = None,
        datasource_ids: Optional[List[int]] = None,
        component_ids: Optional[List[int]] = None,
        branch_ids: Optional[List[int]] = None,
        allowed_languages: Optional[List[str]] = None,
        asset_folder_ids: Optional[List[int]] = None
    ) -> Any:
        """
        Updates a space role's configuration via the Storyblok Management API.
        """
        try:
            payload: Dict[str, Any] = {"space_role": {}}
            sr = payload["space_role"]

            if allowed_paths is not None:
                sr["allowed_paths"] = allowed_paths
            if field_permissions is not None:
                sr["field_permissions"] = field_permissions
            if readonly_field_permissions is not None:
                sr["readonly_field_permissions"] = readonly_field_permissions
            if permissions is not None:
                sr["permissions"] = permissions
            if role_name is not None:
                sr["role"] = role_name
            if subtitle is not None:
                sr["subtitle"] = subtitle
            if datasource_ids is not None:
                sr["datasource_ids"] = datasource_ids
            if component_ids is not None:
                sr["component_ids"] = component_ids
            if branch_ids is not None:
                sr["branch_ids"] = branch_ids
            if allowed_languages is not None:
                sr["allowed_languages"] = allowed_languages
            if asset_folder_ids is not None:
                sr["asset_folder_ids"] = asset_folder_ids

            url = build_management_url(f"/space_roles/{space_role_id}")
            resp = await client.put(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def delete_space_role(
        space_role_id: int
    ) -> Any:
        """
        Deletes a space role using the Storyblok Management API.
        """
        try:
            url = build_management_url(f"/space_roles/{space_role_id}")
            resp = await client.delete(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

