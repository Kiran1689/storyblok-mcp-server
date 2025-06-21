from typing import Any, Optional
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import build_management_url, get_management_headers, _handle_response, APIError

def register_workflow_stage_changes(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_multiple_workflow_stage_changes(
        space_id: int,
        with_story: Optional[int] = None
    ) -> Any:
        """
        Retrieves multiple workflow stage changes in a Storyblok space via the Management API.
        """
        try:
            params = {"with_story": with_story} if with_story else {}
            url = build_management_url(f"/workflow_stage_changes", params=params)
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def create_workflow_stage_change(
        story_id: int,
        workflow_stage_id: int
    ) -> Any:
        """
        Creates a new workflow stage change for a story in a Storyblok space via the Management API.
        """
        try:
            payload = {
                "workflow_stage_change": {
                    "story_id": story_id,
                    "workflow_stage_id": workflow_stage_id
                }
            }

            url = build_management_url(f"/workflow_stage_changes")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
