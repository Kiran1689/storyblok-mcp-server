import json
from typing import Any, Optional, Dict
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import (
    build_management_url,
    get_management_headers,
    _handle_response,
    APIError,
)

def register_tasks(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_multiple_tasks(
        space_id: int,
        page: Optional[int] = 1,
        per_page: Optional[int] = 25
    ) -> Any:
        """
        Retrieves multiple tasks from a specified Storyblok space using the Management API.
        """
        try:
            params: Dict[str, Any] = {
                "page": page,
                "per_page": per_page
            }

            url = build_management_url("/tasks/")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
    
    @mcp.tool()
    async def retrieve_single_task(
        task_id: int
    ) -> Any:
        """
        Retrieves a single task from a specified Storyblok space using the Management API.
        """
        try:
            url = build_management_url(f"/tasks/{task_id}")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def create_task(
        name: str,
        task_type: str = "webhook",
        webhook_url: Optional[str] = None,
        description: Optional[str] = None,
        lambda_code: Optional[str] = None,
        user_dialog: Optional[dict] = None
    ) -> Any:
        """
        Creates a new task in a specified Storyblok space using the Management API.
        """
        try:
            payload = {
                "task": {
                    "name": name,
                    "task_type": task_type,
                    "webhook_url": webhook_url,
                    "description": description,
                    "lambda_code": lambda_code,
                    "user_dialog": user_dialog
                }
            }

            url = build_management_url("/tasks/")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def update_task(
        task_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        task_type: Optional[str] = "webhook",
        webhook_url: Optional[str] = None,
        lambda_code: Optional[str] = None,
        user_dialog: Optional[dict] = None
    ) -> Any:
        """
        Updates an existing task in a specified Storyblok space using the Management API.
        """
        try:
            payload = {
                "task": {
                    "name": name,
                    "description": description,
                    "task_type": task_type,
                    "webhook_url": webhook_url,
                    "lambda_code": lambda_code,
                    "user_dialog": user_dialog
                }
            }

            url = build_management_url(f"/tasks/{task_id}")
            resp = await client.put(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def delete_task(
        task_id: int
    ) -> Any:
        """
        Deletes an existing task in a specified Storyblok space using the Management API.
        """
        try:
            url = build_management_url(f"/tasks/{task_id}")
            resp = await client.delete(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    