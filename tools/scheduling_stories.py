from typing import Any, Optional
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import build_management_url, get_management_headers, _handle_response, APIError

def register_story_schedules(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_multiple_story_schedules(
        space_id: int,
        by_status: Optional[str] = None
    ) -> Any:
        """
        Retrieves multiple story scheduling entries in a Storyblok space via the Management API.

        - by_status: Optional status filter ("published_before_schedule" or "scheduled").
        """
        try:
            params: dict[str, Any] = {}
            if by_status is not None:
                params["by_status"] = by_status

            url = build_management_url(f"/story_schedulings/")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def retrieve_one_story_schedule(
        story_scheduling_id: int
    ) -> Any:
        """
        Retrieves a single story schedule entry by its ID in a Storyblok space via the Management API.

        - story_scheduling_id: Numeric ID of the schedule to retrieve.
        """
        try:
            url = build_management_url(
                f"/story_schedulings/{story_scheduling_id}"
            )
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def create_story_schedule(
        story_id: int,
        publish_at: str,
        language: Optional[str] = None
    ) -> Any:
        """
        Creates a new story schedule via the Storyblok Management API.

        - story_id: Numeric ID of the story to be scheduled.
        - publish_at: ISO‑8601 date/time string in UTC (e.g., "2025‑06‑20T15:30:00Z").
        - language: Optional language code (e.g., "en", "pt‑br").
        """
        try:
            payload: dict[str, Any] = {
                "story_scheduling": {
                    "story_id": story_id,
                    "publish_at": publish_at
                }
            }
            if language:
                payload["story_scheduling"]["language"] = language

            url = build_management_url(f"/story_schedulings")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def update_story_schedule(
        space_id: int,
        story_scheduling_id: int,
        publish_at: Optional[str] = None,
        language: Optional[str] = None
    ) -> Any:
        """
        Updates an existing story schedule via the Storyblok Management API.

        - space_id: Numeric ID of the Storyblok space.
        - story_scheduling_id: Numeric ID of the schedule to update.
        - publish_at: New ISO‑8601 UTC date/time string.
        - language: Optional new language code.
        """
        try:
            payload: dict[str, Any] = {"story_scheduling": {}}
            if publish_at is not None:
                payload["story_scheduling"]["publish_at"] = publish_at
            if language is not None:
                payload["story_scheduling"]["language"] = language

            url = build_management_url(
                f"/story_schedulings/{story_scheduling_id}"
            )
            resp = await client.put(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def delete_story_schedule(
        story_scheduling_id: int
    ) -> Any:
        """
        Deletes a story schedule entry via the Storyblok Management API.
        """
        try:
            url = build_management_url(
                f"/story_schedulings/{story_scheduling_id}"
            )
            resp = await client.delete(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}