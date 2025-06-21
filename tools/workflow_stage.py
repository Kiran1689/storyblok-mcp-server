from typing import Any, List, Optional
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import build_management_url, get_management_headers, _handle_response, APIError

def register_workflow_stages(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_multiple_workflow_stages(
        exclude_id: Optional[int] = None,
        by_ids: Optional[str] = None,
        search: Optional[str] = None,
        in_workflow: Optional[int] = None
    ) -> Any:
        """
        Retrieves multiple workflow stages in a Storyblok space via the Management API.

        - space_id: Numeric ID of the space.
        - exclude_id: ID of a workflow stage to exclude.
        - by_ids: Comma-separated list of workflow stage IDs to retrieve.
        - search: Filter by workflow stage name.
        - in_workflow: Filter by a specific workflow ID.
        """
        try:
            params = {
                "exclude_id": exclude_id,
                "by_ids": by_ids,
                "search": search,
                "in_workflow": in_workflow
            }
            # Filter out any parameters that are None
            params = {key: value for key, value in params.items() if value is not None}

            url = build_management_url(f"/workflow_stages/")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def retrieve_single_workflow_stage(
        workflow_stage_id: int
    ) -> Any:
        """
        Retrieves a single workflow stage by its ID in a Storyblok space via the Management API.
        """
        try:
            url = build_management_url(f"/workflow_stages/{workflow_stage_id}")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def create_workflow_stage(
        name: str,
        color: str,
        is_default: Optional[bool] = False,
        user_ids: Optional[List[int]] = None,
        space_role_ids: Optional[List[int]] = None,
        workflow_stage_ids: Optional[List[int]] = None,
        allow_publish: Optional[bool] = False,
        allow_all_stages: Optional[bool] = False,
        allow_admin_publish: Optional[bool] = False,
        allow_all_users: Optional[bool] = False,
        allow_admin_change: Optional[bool] = False,
        allow_editor_change: Optional[bool] = False,
        position: Optional[int] = None,
        after_publish_id: Optional[int] = None,
        workflow_id: Optional[int] = None
    ) -> Any:
        """
        Creates a new workflow stage in a Storyblok space via the Management API.
        """
        try:
            payload = {
                "workflow_stage": {
                    "name": name,
                    "color": color,
                    "is_default": is_default,
                    "user_ids": user_ids or [],
                    "space_role_ids": space_role_ids or [],
                    "workflow_stage_ids": workflow_stage_ids or [],
                    "allow_publish": allow_publish,
                    "allow_all_stages": allow_all_stages,
                    "allow_admin_publish": allow_admin_publish,
                    "allow_all_users": allow_all_users,
                    "allow_admin_change": allow_admin_change,
                    "allow_editor_change": allow_editor_change,
                    "position": position,
                    "after_publish_id": after_publish_id,
                    "workflow_id": workflow_id
                }
            }

            url = build_management_url(f"/workflow_stages")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    
    @mcp.tool()
    async def update_workflow_stage(
        workflow_id: int,
        name: str,
        color: str,
        is_default: Optional[bool] = False,
        user_ids: Optional[List[int]] = None,
        space_role_ids: Optional[List[int]] = None,
        workflow_stage_ids: Optional[List[int]] = None,
        allow_publish: Optional[bool] = False,
        allow_all_stages: Optional[bool] = False,
        allow_admin_publish: Optional[bool] = False,
        allow_all_users: Optional[bool] = False,
        allow_admin_change: Optional[bool] = False,
        allow_editor_change: Optional[bool] = False,
        position: Optional[int] = None,
        after_publish_id: Optional[int] = None
    ) -> Any:
        """
        Updates an existing workflow stage in a Storyblok space via the Management API.
        """
        try:
            payload = {
                "workflow_stage": {
                    "name": name,
                    "color": color,
                    "is_default": is_default,
                    "user_ids": user_ids or [],
                    "space_role_ids": space_role_ids or [],
                    "workflow_stage_ids": workflow_stage_ids or [],
                    "allow_publish": allow_publish,
                    "allow_all_stages": allow_all_stages,
                    "allow_admin_publish": allow_admin_publish,
                    "allow_all_users": allow_all_users,
                    "allow_admin_change": allow_admin_change,
                    "allow_editor_change": allow_editor_change,
                    "position": position,
                    "after_publish_id": after_publish_id
                }
            }

            url = build_management_url(f"/workflow_stages/{workflow_id}")
            resp = await client.put(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def delete_workflow_stage(
        workflow_id: int
    ) -> Any:
        """
        Deletes a workflow stage in a Storyblok space via the Management API.
        """
        try:
            url = build_management_url(f"/workflow_stages/{workflow_id}")
            resp = await client.delete(url, headers=get_management_headers())
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}