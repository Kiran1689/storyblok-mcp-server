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

def register_collaborators(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_multiple_collaborators(
        page: Optional[int] = 1,
        per_page: Optional[int] = 25
    ) -> Any:
        """
        Retrieves a paginated list of collaborators (users) in a specified Storyblok space.
        """
        try:
            params = {
                "page": page,
                "per_page": per_page
            }
            url = build_management_url("/collaborators/")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @ mcp.tool()
    async def add_collaborator(
        email: str,
        role: Optional[str] = None,
        space_role_id: Optional[int] = None,
        space_role_ids: Optional[List[int]] = None,
        permissions: Optional[List[str]] = None,
        allow_multiple_roles_creation: Optional[bool] = None
    ) -> Any:
        """
        Adds a collaborator to a space in Storyblok.

        Use either `role` (string) OR `space_role_id` (int) OR `space_role_ids` (list[int]).
        """
        try:
            collaborator: dict[str, Any] = {"email": email}

            if role:
                collaborator["role"] = role
            if space_role_id:
                collaborator["space_role_id"] = space_role_id
            if space_role_ids:
                collaborator["space_role_ids"] = space_role_ids
            if permissions:
                collaborator["permissions"] = permissions
            if allow_multiple_roles_creation is not None:
                collaborator["allow_multiple_roles_creation"] = allow_multiple_roles_creation

            payload = {"collaborator": collaborator}
            url = build_management_url("/collaborators/")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def update_collaborator(
        collaborator_id: int,
        role: Optional[str] = None,
        user_id: Optional[int] = None,
        permissions: Optional[List[str]] = None,
        space_role_id: Optional[int] = None,
        space_role_ids: Optional[List[int]] = None,
        allowed_paths: Optional[List[int]] = None,
        field_permissions: Optional[List[str]] = None
    ) -> Any:
        """
        Updates roles, permissions, or access paths for an existing collaborator.

        """
        try:
            payload: dict[str, Any] = {"collaborator": {}}
            if role is not None:
                payload["collaborator"]["role"] = role
            if user_id is not None:
                payload["collaborator"]["user_id"] = user_id
            if permissions is not None:
                payload["collaborator"]["permissions"] = permissions
            if space_role_id is not None:
                payload["collaborator"]["space_role_id"] = space_role_id
            if space_role_ids is not None:
                payload["collaborator"]["space_role_ids"] = space_role_ids
            if allowed_paths is not None:
                payload["collaborator"]["allowed_paths"] = allowed_paths
            if field_permissions is not None:
                payload["collaborator"]["field_permissions"] = field_permissions

            url = build_management_url(
                f"/collaborators/{collaborator_id}"
            )
            resp = await client.put(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def delete_collaborator(
        collaborator_id: int,
        sso_id: Optional[str] = None
    ) -> Any:
        """
        Deletes a collaborator from a specified Storyblok space.
        You can delete by numeric collaborator_id or by sso_id for SSO users.
        """
        try:
            identifier = sso_id if sso_id is not None else collaborator_id
            url = build_management_url(
                f"/collaborators/{identifier}"
            )
            resp = await client.delete(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}