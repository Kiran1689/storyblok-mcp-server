import json
from typing import Optional, Any, List
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP

from utils.api import (
    build_management_url,
    get_management_headers,
    _handle_response,
    APIError
)

def register_releases(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_multiple_releases(
        space_id: int,
        branch_id: Optional[int] = None
    ) -> Any:
        """
        Retrieves multiple releases from a specified Storyblok space.
        """
        try:
            params = {}
            if branch_id is not None:
                params["branch_id"] = branch_id

            url = build_management_url(f"/releases")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}


    @mcp.tool()
    async def retrieve_single_release(
        release_id: int
    ) -> Any:
        """
        Retrieves a single release from a specified Storyblok space.
        """
        try:
            url = build_management_url(f"/releases/{release_id}")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}


    @mcp.tool()
    async def create_release(
        name: str,
        release_at: Optional[str] = None,
        timezone: Optional[str] = None,
        branches_to_deploy: Optional[List[int]] = None,
        users_to_notify_ids: Optional[List[int]] = None
    ) -> Any:
        """
        Creates a new release in a specified Storyblok space.
        """
        try:
            payload = {
                "release": {
                    "name": name,
                    "release_at": release_at,
                    "timezone": timezone,
                    "branches_to_deploy": branches_to_deploy,
                    "users_to_notify_ids": users_to_notify_ids
                }
            }

            url = build_management_url(f"/releases")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def update_release(
        release_id: int,
        name: Optional[str] = None,
        release_at: Optional[str] = None,
        timezone: Optional[str] = None,
        branches_to_deploy: Optional[List[int]] = None,
        users_to_notify_ids: Optional[List[int]] = None,
        do_release: Optional[bool] = None
    ) -> Any:
        """
        Updates an existing release in a specified Storyblok space.
        """
        try:
            payload = {
                "release": {
                    "name": name,
                    "release_at": release_at,
                    "timezone": timezone,
                    "branches_to_deploy": branches_to_deploy,
                    "users_to_notify_ids": users_to_notify_ids
                },
                "do_release": do_release
            }

            # Remove any keys with None values
            payload = {k: v for k, v in payload.items() if v is not None}

            url = build_management_url(f"/releases/{release_id}")
            resp = await client.put(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}


    @mcp.tool()
    async def delete_release(release_id: str) -> Any:
        """Deletes a release."""
        try:
            url = build_management_url(f"/releases/{release_id}")
            resp = await client.delete(url, headers=get_management_headers())
            # No need to return full payload on delete
            return {
                "content": [
                    {"type": "text", "text": f"Release {release_id} has been successfully deleted."}
                ]
            }
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
