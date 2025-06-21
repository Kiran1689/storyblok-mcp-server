from typing import Any, Optional, List, Dict
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import build_management_url, get_management_headers, _handle_response, APIError

def register_access_tokens(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_multiple_access_tokens() -> Any:
        """
        Retrieve all access tokens for the current Storyblok space using the Management API.
        
        Returns:
            Any: The API response containing a list of access tokens or an error message.
        """
        try:
            url = build_management_url("/api_keys/")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def create_access_token(
        access: str,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        story_ids: Optional[List[int]] = None,
        min_cache: Optional[int] = None
    ) -> Any:
        """
        Create a new access token in the current Storyblok space via the Management API.
        
        Request Body:
            access (str): The access level for the token (e.g., 'draft', 'published').
            name (Optional[str]): Optional name for the token.
            branch_id (Optional[int]): Optional branch ID to associate with the token.
            story_ids (Optional[List[int]]): Optional list of story IDs to restrict access.
            min_cache (Optional[int]): Optional minimum cache time in seconds.
        
        Returns:
            Any: The API response containing the created access token or an error message.
        """
        try:
            api_key: dict[str, Any] = {"access": access}
            if name is not None:
                api_key["name"] = name
            if branch_id is not None:
                api_key["branch_id"] = branch_id
            if story_ids is not None:
                api_key["story_ids"] = story_ids
            if min_cache is not None:
                api_key["min_cache"] = min_cache

            payload = {"api_key": api_key}
            url = build_management_url("/api_keys/")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def update_access_token(
        token_id: int,
        access: Optional[str] = None,
        name: Optional[str] = None,
        branch_id: Optional[int] = None,
        story_ids: Optional[List[int]] = None,
        min_cache: Optional[int] = None
    ) -> Any:
        """
        Update an existing access token in the current Storyblok space via the Management API.
        
        Params:
            token_id (int): The ID of the access token to update.
        
        Request Body:
            access (Optional[str]): New access level for the token.
            name (Optional[str]): New name for the token.
            branch_id (Optional[int]): New branch ID to associate with the token.
            story_ids (Optional[List[int]]): New list of story IDs to restrict access.
            min_cache (Optional[int]): New minimum cache time in seconds.
        
        Returns:
            Any: A success message or an error message.
        """
        try:
            api_key: dict[str, Any] = {}
            if access is not None:
                api_key["access"] = access
            if name is not None:
                api_key["name"] = name
            if branch_id is not None:
                api_key["branch_id"] = branch_id
            if story_ids is not None:
                api_key["story_ids"] = story_ids
            if min_cache is not None:
                api_key["min_cache"] = min_cache

            payload = {"api_key": api_key}
            url = build_management_url(f"/api_keys/{token_id}")
            resp = await client.put(url, json=payload, headers=get_management_headers())
            if resp.status_code == 204:
                return {"isError": False, "content": [{"type": "text", "text": f"Access Token updated successfully."}]}
            else:
                return {"isError": True, "content": [{"type": "text", "text": f"Failed to update access token. Status code: {resp.status_code}"}]}

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def delete_access_token(
        token_id: int
    ) -> Any:
        """
        Delete an access token from the current Storyblok space using the Management API.
        
        Params:
            token_id (int): The ID of the access token to delete.
        
        Returns:
            Any: A success message or an error message.
        """
        try:
            url = build_management_url(f"/api_keys/{token_id}")
            resp = await client.delete(url, headers=get_management_headers())
            if resp.status_code == 204:
                return {"isError": False, "content": [{"type": "text", "text": f"Access Token deleted successfully."}]}
            else:
                return {"isError": True, "content": [{"type": "text", "text": f"Failed to delete Access token. Status code: {resp.status_code}"}]}
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
