from typing import Any, Dict, List, Optional
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import build_management_url, get_management_headers, _handle_response, APIError

def register_discussions(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_multiple_discussions(
        story_id: int,
        per_page: Optional[int] = 25,
        page: Optional[int] = 1,
        by_status: Optional[str] = None
    ) -> Any:
        """
        Retrieves multiple discussions for a specific story in a Storyblok space.

        - story_id: Numeric ID of the story.
        - per_page: Number of discussions per page (default: 25, max: 100).
        - page: Page number to retrieve (default: 1).
        - by_status: Filter discussions by status (e.g., 'unsolved', 'solved').
        """
        try:
            params = {
                "per_page": per_page,
                "page": page,
                "by_status": by_status
            }
            url = build_management_url(f"/stories/{story_id}/discussions")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def retrieve_specific_discussion(
        discussion_id: int
    ) -> Any:
        """
        Retrieves a specific discussion by its ID in a Storyblok space.

        - discussion_id: Numeric ID of the discussion.
        """
        try:
            url = build_management_url(f"/discussions/{discussion_id}")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def retrieve_idea_discussions_comments(
        discussion_uuid: str
    ) -> Any:
        """
        Retrieves comments for a specific idea discussion in a Storyblok space.

        - discussion_uuid: UUID of the discussion in the idea.
        """
        try:
            url = build_management_url(f"/discussions/{discussion_uuid}/comments")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def create_discussion(
        story_id: int,
        title: str,
        fieldname: str,
        block_uid: str,
        component: str,
        lang: str,
        message_json: List[Dict[str, Any]]
    ) -> Any:
        """
        Creates a new discussion for a story via the Storyblok Management API.

        Required:
        - story_id: ID of the story
        - title: Title of the discussion field
        - fieldname: Technical name of the discussion field
        - block_uid: ID of the discussion block
        - component: Component/block name this discussion belongs to
        - lang: Language code (e.g., "default", "en")
        - message_json: Array of message objects [{"type": "text", "text": "...", "attrs": {...}}, ...]
        """
        try:
            payload = {
                "discussion": {
                    "title": title,
                    "fieldname": fieldname,
                    "block_uid": block_uid,
                    "component": component,
                    "lang": lang,
                    "comment": {
                        "message_json": message_json
                    }
                }
            }

            url = build_management_url(f"/stories/{story_id}/discussions")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def retrieve_my_discussions(
        page: Optional[int] = 1,
        per_page: Optional[int] = 25,
        by_status: Optional[str] = None
    ) -> Any:
        """
        Retrieves discussions you're involved in within a Storyblok space.

        - space_id: Numeric ID of the space.
        - page: Page number (default 1).
        - per_page: Items per page (default 25, max 100).
        - by_status: Filter discussions by status ('unsolved' or 'solved').
        """
        try:
            params = {
                "page": page,
                "per_page": per_page
            }
            if by_status is not None:
                params["by_status"] = by_status

            url = build_management_url(f"/mentioned_discussions/me")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def resolve_discussion(
        discussion_id: int,
        solved_at: str
    ) -> Any:
        """
        Marks a discussion as resolved via the Storyblok Management API.

        - discussion_id: Numeric ID of the discussion.
        - solved_at: Timestamp when the discussion is resolved (ISO 8601 format).
        """
        try:
            payload = {
                "discussion": {
                    "solved_at": solved_at
                }
            }

            url = build_management_url(f"/discussions/{discussion_id}")
            resp = await client.put(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def retrieve_multiple_comments(
        discussion_id: int
    ) -> Any:
        """
        Retrieves all comments from a specific discussion via the Storyblok Management API.

        - discussion_id: Numeric ID of the discussion.
        """
        try:
            url = build_management_url(f"/discussions/{discussion_id}/comments")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True,
                    "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def create_comment(
        discussion_id: int,
        message_json: List[Dict[str, Any]],
        message: Optional[str] = None
    ) -> Any:
        """
        Adds a comment to a discussion via the Storyblok Management API.

        - discussion_id: Numeric ID of the discussion.
        - message_json: Required array of message objects. Each must include "type", "text", and "attrs".
        - message: Optional plain-text field (can be null or string).
        """
        try:
            payload = {
                "comment": {
                    "message_json": message_json
                }
            }
            # Include optional `message` field
            if message is not None:
                payload["comment"]["message"] = message

            url = build_management_url(f"/discussions/{discussion_id}/comments")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def update_comment(
        discussion_id: int,
        comment_id: int,
        message_json: List[Dict[str, Any]],
        message: Optional[str] = None
    ) -> Any:
        """
        Updates a comment in a discussion via the Storyblok Management API.

        Required:
        - discussion_id: Numeric ID of the discussion.
        - comment_id: Numeric ID of the comment.

        Payload:
        - message_json: Required. Array of message objects, each with keys "type", "text", "attrs".
        - message: Optional string or null.
        """
        try:
            payload = {
                "comment": {
                    "message_json": message_json
                }
            }
            # Include optional message field when provided
            if message is not None:
                payload["comment"]["message"] = message

            url = build_management_url(
                f"/discussions/{discussion_id}/comments/{comment_id}"
            )
            resp = await client.put(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def delete_comment(
        discussion_id: int,
        comment_id: int
    ) -> Any:
        """
        Deletes a comment from a discussion via the Storyblok Management API.

        - discussion_id: Numeric ID of the discussion.
        - comment_id: Numeric ID of the comment.
        """
        try:
            url = build_management_url(
                f"/discussions/{discussion_id}/comments/{comment_id}"
            )
            resp = await client.delete(url, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True,
                    "content": [{"type": "text", "text": str(e)}]}