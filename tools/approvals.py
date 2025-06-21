import json
from typing import Any, Optional
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import (
    build_management_url,
    get_management_headers,
    _handle_response,
    APIError,
)

def register_approvals(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_multiple_approvals(
        approver: int,
        page: Optional[int] = None,
        per_page: Optional[int] = None
    ) -> Any:
        """
        Retrieves multiple approvals from a specified Storyblok space.
        
        :param approver: Optional approver user ID to filter approvals.
        """
        try:
            params: dict[str, Any] = {}
            if not approver:
                return {"isError": True, "content": [{"type": "text", "text": f"Error: approver id is required"}]}
            if approver is not None:
                params["approver"] = approver
            # Despite pagination not being explicitly documented, support page/per_page
            if page is not None:
                params["page"] = page
            if per_page is not None:
                params["per_page"] = per_page

            url = build_management_url("/approvals/")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
    
    @mcp.tool()
    async def retrieve_single_approval(
        approval_id: int
    ) -> Any:
        """
        Retrieves a single approval by its ID from a specified Storyblok space.
        """
        try:
            url = build_management_url(f"/approvals/{approval_id}")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def create_approval(
        story_id: int,
        approver_id: int
    ) -> Any:
        """
        Creates an approval request for a story (and optional release) in a Storyblok space.
        
        :param story_id: Numeric ID of the content entry to be approved.
        :param approver_id: Numeric ID of the user who will approve it.
        """
        try:
            payload: dict[str, Any] = {
                "approval": {
                    "story_id": story_id,
                    "approver_id": approver_id
                }
            }
        
            url = build_management_url("/approvals/")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def create_release_approval(
        story_id: int,
        approver_id: int,
        release_id: Optional[int] = None
    ) -> Any:
        """
        Creates a release approval for a given story and release.

        :param story_id:       ID of the story/content entry to approve.
        :param approver_id:    ID of the user who will approve the release.
        :param release_id:     ID of the release to include in the approval (optional).
        """
        try:
            payload: dict[str, Any] = {
                "approval": {
                    "story_id": story_id,
                    "approver_id": approver_id
                }
            }
            if release_id is not None:
                payload["release_id"] = release_id

            url = build_management_url("/approvals/")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def delete_approval(
        approval_id: int
    ) -> Any:
        """
        Deletes an approval from a specified Storyblok space.

        :param approval_id: Numeric ID of the approval to delete.
        """
        try:
            url = build_management_url(
                f"/approvals/{approval_id}"
            )
            resp = await client.delete(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}