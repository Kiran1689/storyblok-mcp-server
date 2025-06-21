import json
from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import FastMCP
from httpx import AsyncClient
from utils.api import (
    build_management_url,
    get_management_headers,
    _handle_response,
    APIError,
)

def register_space(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def fetch_spaces() -> Any:
        """
        Retrieve all accessible spaces.
        """
        try:
            url = "https://mapi.storyblok.com/v1/spaces/"
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def get_space(space_id: str) -> Any:
        """
        Fetch a specific space by ID.
        """
        try:
            url = f"https://mapi.storyblok.com/v1/spaces/{space_id}"
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        

    @mcp.tool()
    async def create_space(
        name: str,
        domain: Optional[str] = None,
        story_published_hook: Optional[str] = None,
        environments: Optional[List[Dict[str, str]]] = None
    ) -> Any:
        """
        Creates a new Storyblok space via the Management API.
        """
        try:
            payload: Dict[str, Any] = {
                "space": {"name": name}
            }
            if domain:
                payload["space"]["domain"] = domain
            if story_published_hook:
                payload["space"]["story_published_hook"] = story_published_hook
            if environments:
                payload["space"]["environments"] = environments

            url = "https://mapi.storyblok.com/v1/spaces/"
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}


    @mcp.tool()
    async def update_space(
        space_id: int,
        name: Optional[str] = None,
        domain: Optional[str] = None,
        uniq_domain: Optional[str] = None,
        owner_id: Optional[int] = None,
        story_published_hook: Optional[str] = None,
        environments: Optional[List[Dict[str, str]]] = None,
        parent_id: Optional[int] = None,
        searchblok_id: Optional[int] = None,
        duplicatable: Optional[bool] = None,
        billing_address: Optional[Dict[str, Any]] = None,
        routes: Optional[List[str]] = None,
        default_root: Optional[str] = None,
        has_pending_tasks: Optional[bool] = None,
        ai_translation_disabled: Optional[bool] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Updates an existing Storyblok space via the Management API.
        """
        try:
            payload = {"space": {}}
            if name:
                payload["space"]["name"] = name
            if domain:
                payload["space"]["domain"] = domain
            if uniq_domain:
                payload["space"]["uniq_domain"] = uniq_domain
            if owner_id:
                payload["space"]["owner_id"] = owner_id
            if story_published_hook:
                payload["space"]["story_published_hook"] = story_published_hook
            if environments:
                payload["space"]["environments"] = environments
            if parent_id:
                payload["space"]["parent_id"] = parent_id
            if searchblok_id:
                payload["space"]["searchblok_id"] = searchblok_id
            if duplicatable is not None:
                payload["space"]["duplicatable"] = duplicatable
            if billing_address:
                payload["space"]["billing_address"] = billing_address
            if routes:
                payload["space"]["routes"] = routes
            if default_root:
                payload["space"]["default_root"] = default_root
            if has_pending_tasks is not None:
                payload["space"]["has_pending_tasks"] = has_pending_tasks
            if ai_translation_disabled is not None:
                payload["space"]["ai_translation_disabled"] = ai_translation_disabled
            if options:
                payload["space"]["options"] = options

            url = f"https://mapi.storyblok.com/v1/spaces/{space_id}"
            resp = await client.put(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}


    @mcp.tool()
    async def duplicate_space(
        original_space_id: int,
        new_space_name: str,
        domain: Optional[str] = None,
        story_published_hook: Optional[str] = None,
        environments: Optional[List[Dict[str, str]]] = None,
        searchblok_id: Optional[int] = None,
        has_pending_tasks: Optional[bool] = None
    ) -> Any:
        """
        Duplicates an existing Storyblok space via the Management API.
        """
        try:
            payload = {
                "dup_id": original_space_id,
                "space": {
                    "name": new_space_name,
                    "domain": domain,
                    "story_published_hook": story_published_hook,
                    "environments": environments,
                    "searchblok_id": searchblok_id,
                    "has_pending_tasks": has_pending_tasks
                }
            }

            url = "https://mapi.storyblok.com/v1/spaces/"
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def backup_space(
        space_id: int
    ) -> Any:
        """
        Triggers a backup task for a Storyblok space using Management API.
        """
        try:
            url = f"https://mapi.storyblok.com/v1/spaces/{space_id}/backups"
            resp = await client.post(url, json={}, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
            
    @mcp.tool()
    async def delete_space(
        space_id: int
    ) -> Any:
        """
        Permanently deletes a Storyblok space using the Management API.
        """
        try:
            url = f"https://mapi.storyblok.com/v1/spaces/{space_id}"
            resp = await client.delete(url, headers=get_management_headers())
            if resp.status_code == 204:
                return {"isError": False, "content": [{"type": "text", "text": f"Space deleted successfully."}]}
            else:
                return {"isError": True, "content": [{"type": "text", "text": f"Failed to delter space. Status code: {resp.status_code}"}]}
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

