from typing import Any, Optional
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import build_management_url, get_management_headers, _handle_response, APIError

def register_branches(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_multiple_branches(
        by_ids: Optional[str] = None,
        search: Optional[str] = None
    ) -> Any:
        """
        Retrieves multiple branches (pipelines) in a Storyblok space via the Management API.

        - by_ids: Optional comma-separated list of branch IDs to filter.
        - search: Optional filter term for branch names.
        """
        try:
            params: dict[str, Any] = {}
            if by_ids is not None:
                params["by_ids"] = by_ids
            if search is not None:
                params["search"] = search

            url = build_management_url(f"/branches/")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def retrieve_single_branch(
        branch_id: int
    ) -> Any:
        """
        Retrieves a single branch (pipeline) by its ID via the Storyblok Management API.
        - branch_id: Numeric ID of the branch to retrieve.
        """
        try:
            url = build_management_url(f"/branches/{branch_id}")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def create_branch(
        name: str,
        source_id: Optional[int] = None,
        url: Optional[str] = None,
        position: Optional[int] = None
    ) -> Any:
        """
        Creates a new branch (pipeline) in a Storyblok space via the Management API.

        - name: Required name for the new branch.
        - source_id: Optional ID of an existing branch to clone.
        - url: Optional preview URL for the branch.
        - position: Optional numeric position for ordering.
        """
        try:
            branch_data: dict[str, Any] = {"name": name}
            if source_id is not None:
                branch_data["source_id"] = source_id
            if url is not None:
                branch_data["url"] = url
            if position is not None:
                branch_data["position"] = position

            payload = {"branch": branch_data}
            url_path = build_management_url(f"/branches/")
            resp = await client.post(url_path, json=payload, headers=get_management_headers())
            return _handle_response(resp, url_path)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def update_branch(
        branch_id: int,
        name: Optional[str] = None,
        source_id: Optional[int] = None,
        url: Optional[str] = None,
        position: Optional[int] = None
    ) -> Any:
        """
        Updates an existing branch (pipeline) in a Storyblok space via the Management API.

        - branch_id: Numeric ID of the branch to update.
        Optional fields:
          - name: New branch name
          - source_id: Set/clear source branch (clone origin)
          - url: Preview URL
          - position: Position ordering number
        """
        try:
            branch_data: dict[str, Any] = {}
            if name is not None:
                branch_data["name"] = name
            if source_id is not None:
                branch_data["source_id"] = source_id
            if url is not None:
                branch_data["url"] = url
            if position is not None:
                branch_data["position"] = position

            payload = {"branch": branch_data}
            url_path = build_management_url(f"/branches/{branch_id}")
            resp = await client.put(url_path, json=payload, headers=get_management_headers())
            return _handle_response(resp, url_path)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def delete_branch(
        branch_id: int
    ) -> Any:
        """
        Deletes a branch (pipeline) by its ID in a Storyblok space.
        - branch_id: Numeric ID of the branch to delete.
        """
        try:
            url = build_management_url(f"/branches/{branch_id}")
            resp = await client.delete(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}