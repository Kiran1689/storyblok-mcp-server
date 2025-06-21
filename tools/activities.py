import json
from typing import Any, Optional, List
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import (
    build_management_url,
    get_management_headers,
    _handle_response,
    APIError,
)

def register_activities(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_multiple_activities(
        created_at_gte: Optional[str] = None,
        created_at_lte: Optional[str] = None,
        by_owner_ids: Optional[List[int]] = None,
        types: Optional[List[str]] = None
    ) -> Any:
        """
        Retrieves activity logs for a specified Storyblok space.

        Optional filters:
        - created_at_gte / created_at_lte: 'YYYY-MM-DD' date strings
        - by_owner_ids: list of user IDs
        - types: list of activity types (e.g. 'Story', 'Component', 'Asset')
        """
        try:
            params: dict[str, Any] = {}
            if created_at_gte:
                params["created_at_gte"] = created_at_gte
            if created_at_lte:
                params["created_at_lte"] = created_at_lte
            if by_owner_ids:
                params["by_owner_ids"] = ",".join(map(str, by_owner_ids))
            if types:
                params["types"] = ",".join(types)

            url = build_management_url("/activities/")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def retrieve_single_activity(
        activity_id: int
    ) -> Any:
        """
        Retrieves a single activity log by its ID from a specified Storyblok space.
        """
        try:
            url = build_management_url(f"/activities/{activity_id}")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    