from typing import Any, Dict, Optional
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import get_management_headers, _handle_response, APIError

def register_field_plugin_retrieval(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_field_plugins(
        context: str = "space",
        only_mine: Optional[int] = 1,
        page: Optional[int] = 1,
        per_page: Optional[int] = 25,
        search: Optional[str] = None
    ) -> Any:
        """
        Retrieves multiple field plugins (field types) across different contexts.

        Args:
            context (str): 'space', 'org', or 'partner'
            only_mine (int): 1 = only plugins created by authenticated user
            page (int): pagination page number
            per_page (int): plugins per page (max 100)
            search (str): search filter for plugin name or slug
        """
        try:
            url_map = {
                "space": "https://mapi.storyblok.com/v1/field_types/",
                "org":   "https://mapi.storyblok.com/v1/org_field_types/",
                "partner": "https://mapi.storyblok.com/v1/partner_field_types/"
            }
            if context not in url_map:
                return {"isError": True, "content": [{"type": "text", "text": f"Context must be one of {list(url_map.keys())}"}]}
            
            params: dict[str, Any] = {}
            if only_mine is not None:
                params["only_mine"] = only_mine
            if page is not None:
                params["page"] = page
            if per_page is not None:
                params["per_page"] = per_page
            if search is not None:
                params["search"] = search

            resp = await client.get(url_map[context], headers=get_management_headers(), params=params)
            return _handle_response(resp, url_map[context])
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}


    @mcp.tool()
    async def retrieve_field_plugin(
        field_type_id: int,
        context: str = "space"
    ) -> Any:
        """
        Retrieves a single field plugin by its ID in the specified context.

        Args:
            field_type_id (int): Numeric ID of the field plugin.
            context (str): 'space', 'org', or 'partner'.
        """
        url_map = {
            "space": f"https://mapi.storyblok.com/v1/field_types/{field_type_id}",
            "org": f"https://mapi.storyblok.com/v1/org_field_types/{field_type_id}",
            "partner": f"https://mapi.storyblok.com/v1/partner_field_types/{field_type_id}",
        }

        if context not in url_map:
            return {"isError": True, "content": [{"type": "text", "text": "Context must be 'space', 'org', or 'partner'."}]}

        url = url_map[context]

        try:
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def create_field_plugin(
        name: str,
        body: str,
        compiled_body: str = "",
        context: str = "space"
    ) -> Any:
        """
        Creates a new field plugin (field type) in the specified context.

        Args:
            name (str): Unique name for your plugin (e.g., 'my-geo-selector').
            body (str): The uncompiled JavaScript source for the plugin.
            compiled_body (str): Required; empty string if developing locally.
            context (str): 'space', 'org', or 'partner'.
        """
        try:
            url_map = {
                "space": "https://mapi.storyblok.com/v1/field_types/",
                "org": "https://mapi.storyblok.com/v1/org_field_types/",
                "partner": "https://mapi.storyblok.com/v1/partner_field_types/"
            }

            if context not in url_map:
                return {"isError": True, "content": [{"type": "text", "text": "Invalid context: choose 'space', 'org', or 'partner'."}]}

            payload = {
                "field_type": {
                    "name": name,
                    "body": body,
                    "compiled_body": compiled_body
                }
            }

            resp = await client.post(url_map[context], json=payload, headers=get_management_headers())
            return _handle_response(resp, url_map[context])
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def update_field_plugin(
        field_type_id: int,
        body: Optional[str] = None,
        compiled_body: Optional[str] = None,
        name: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        space_ids: Optional[list[int]] = None,
        context: str = "space"
    ) -> Any:
        """
        Updates an existing field plugin in the specified context.

        Args:
          field_type_id: Numeric ID of the field plugin.
          body: Updated uncompiled JS source.
          compiled_body: Updated compiled JS source.
          name: Optional new name (must still be unique).
          options: Optional config options for the plugin.
          space_ids: Optional space assignment list.
          context: 'space', 'org', or 'partner'.
        """
        url_map = {
            "space": f"https://mapi.storyblok.com/v1/field_types/{field_type_id}",
            "org": f"https://mapi.storyblok.com/v1/org_field_types/{field_type_id}",
            "partner": f"https://mapi.storyblok.com/v1/partner_field_types/{field_type_id}"
        }
        if context not in url_map:
            return {"isError": True, "content":[{"type":"text","text":"Invalid context: use 'space', 'org' or 'partner'."}]}

        payload: Dict[str, Any] = {"field_type": {}}
        if name is not None:
            payload["field_type"]["name"] = name
        if body is not None:
            payload["field_type"]["body"] = body
        if compiled_body is not None:
            payload["field_type"]["compiled_body"] = compiled_body
        if options is not None:
            payload["field_type"]["options"] = options
        if space_ids is not None:
            payload["field_type"]["space_ids"] = space_ids

        try:
            resp = await client.put(
                url_map[context],
                headers=get_management_headers(),
                json=payload
            )
            return _handle_response(resp, url_map[context])
        except APIError as e:
            return {"isError": True, "content": [{"type":"text","text":str(e)}]}
        
    @mcp.tool()
    async def delete_field_plugin(field_type_id: int) -> Any:
        """
        Deletes a field plugin by its ID.

        Args:
            field_type_id (int): Numeric ID of the field plugin to delete.
        """
        url = f"https://mapi.storyblok.com/v1/field_types/{field_type_id}"
        try:
            resp = await client.delete(url, headers=get_management_headers())
            if resp.status_code == 204:
                return {"isError": False, "content": [{"type": "text", "text": "Field plugin deleted successfully."}]}
            else:
                return {"isError": True, "content": [{"type": "text", "text": f"Failed to delete field plugin. Status code: {resp.status_code}"}]}
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}