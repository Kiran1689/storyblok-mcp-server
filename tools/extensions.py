import json
from typing import Any, List, Optional
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import get_management_headers, _handle_response, APIError

def register_extensions(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def retrieve_all_extensions(context: str) -> Any:
        """
        Retrieves all extensions (plugins) from the specified context.
        
        Args:
            context (str): The context to retrieve extensions from. 
            Options are 'org' for organization-level or 'partner' for partner-level extensions.
        """
        try:
            # Determine the base URL based on the context
            if context == "org":
                url = "https://mapi.storyblok.com/v1/org_apps/"
            elif context == "partner":
                url = "https://mapi.storyblok.com/v1/partner_apps/"
            else:
                return {"isError": True, "content": [{"type": "text", "text": "Invalid context specified."}]}

            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def retrieve_extension(extension_id: int, context: str) -> Any:
        """
        Retrieves the settings of a specific extension by its numeric ID.
        
        Args:
            extension_id (int): The numeric ID of the extension.
            context (str): The context to retrieve the extension from. 
                           Options are 'org' for organization-level or 'partner' for partner-level extensions.
        """
        try:
            # Determine the base URL based on the context
            if context == "org":
                url = f"https://app.storyblok.com/v1/org_apps/{extension_id}"
            elif context == "partner":
                url = f"https://mapi.storyblok.com/v1/partner_apps/{extension_id}"
            else:
                return {"isError": True, "content": [{"type": "text", "text": "Invalid context specified."}]}

            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def create_extension(
        name: str,
        slug: str,
        context: str,
        icon: Optional[str] = None,
        preview_video: Optional[str] = None,
        description: Optional[str] = None,
        intro: Optional[str] = None,
        screenshot: Optional[str] = None,
        website: Optional[str] = None,
        author: Optional[str] = None,
        field_type_ids: Optional[List[int]] = None,
        embedded_app_url: Optional[str] = None,
        dev_embedded_app_url: Optional[str] = None,
        dev_oauth_redirect_uri: Optional[str] = None,
        in_sidebar: Optional[bool] = None,
        in_toolbar: Optional[bool] = None,
        sidebar_icon: Optional[str] = None,
        oauth_redirect_uri: Optional[str] = None,
        enable_space_settings: Optional[bool] = None
    ) -> Any:
        """
        Creates a new extension in the specified context (organization or partner).
        """
        try:
            # Determine the base URL based on the context
            if context == "org":
                url = "https://mapi.storyblok.com/v1/org_apps"
            elif context == "partner":
                url = "https://mapi.storyblok.com/v1/partner_apps"
            else:
                return {"isError": True, "content": [{"type": "text", "text": "Invalid context specified. Mention either 'org' or 'partner'."}]}

            # Construct the payload
            payload = {
                "app": {
                    "name": name,
                    "slug": slug,
                    "icon": icon,
                    "preview_video": preview_video,
                    "description": description,
                    "intro": intro,
                    "screenshot": screenshot,
                    "website": website,
                    "author": author,
                    "field_type_ids": field_type_ids,
                    "embedded_app_url": embedded_app_url,
                    "dev_embedded_app_url": dev_embedded_app_url,
                    "dev_oauth_redirect_uri": dev_oauth_redirect_uri,
                    "in_sidebar": in_sidebar,
                    "in_toolbar": in_toolbar,
                    "sidebar_icon": sidebar_icon,
                    "oauth_redirect_uri": oauth_redirect_uri,
                    "enable_space_settings": enable_space_settings
                }
            }

            # Remove keys with None values
            payload["app"] = {k: v for k, v in payload["app"].items() if v is not None}

            # Make the POST request to the appropriate endpoint
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def update_extension(
        extension_id: int,
        context: str = "org",
        name: Optional[str] = None,
        slug: Optional[str] = None,
        icon: Optional[str] = None,
        preview_video: Optional[str] = None,
        description: Optional[str] = None,
        intro: Optional[str] = None,
        screenshot: Optional[str] = None,
        website: Optional[str] = None,
        author: Optional[str] = None,
        field_type_ids: Optional[List[int]] = None,
        embedded_app_url: Optional[str] = None,
        dev_embedded_app_url: Optional[str] = None,
        dev_oauth_redirect_uri: Optional[str] = None,
        in_sidebar: Optional[bool] = None,
        in_toolbar: Optional[bool] = None,
        sidebar_icon: Optional[str] = None,
        oauth_redirect_uri: Optional[str] = None,
        enable_space_settings: Optional[bool] = None
    ) -> Any:
        """
        Updates an existing extension in the specified context (organization or partner).
        """
        try:
            # Determine the base URL based on the context
            if context == "org":
                url = f"https://mapi.storyblok.com/v1/org_apps/{extension_id}"
            elif context == "partner":
                url = f"https://mapi.storyblok.com/v1/partner_apps/{extension_id}"
            else:
                return {"isError": True, "content": [{"type": "text", "text": "Invalid context specified. Mention either 'org' or 'partner'"}]}

            # Construct the payload
            payload = {"app": {}}
            if name is not None:
                payload["app"]["name"] = name
            if slug is not None:
                payload["app"]["slug"] = slug
            if icon is not None:
                payload["app"]["icon"] = icon
            if preview_video is not None:
                payload["app"]["preview_video"] = preview_video
            if description is not None:
                payload["app"]["description"] = description
            if intro is not None:
                payload["app"]["intro"] = intro
            if screenshot is not None:
                payload["app"]["screenshot"] = screenshot
            if website is not None:
                payload["app"]["website"] = website
            if author is not None:
                payload["app"]["author"] = author
            if field_type_ids is not None:
                payload["app"]["field_type_ids"] = field_type_ids
            if embedded_app_url is not None:
                payload["app"]["embedded_app_url"] = embedded_app_url
            if dev_embedded_app_url is not None:
                payload["app"]["dev_embedded_app_url"] = dev_embedded_app_url
            if dev_oauth_redirect_uri is not None:
                payload["app"]["dev_oauth_redirect_uri"] = dev_oauth_redirect_uri
            if in_sidebar is not None:
                payload["app"]["in_sidebar"] = in_sidebar
            if in_toolbar is not None:
                payload["app"]["in_toolbar"] = in_toolbar
            if sidebar_icon is not None:
                payload["app"]["sidebar_icon"] = sidebar_icon
            if oauth_redirect_uri is not None:
                payload["app"]["oauth_redirect_uri"] = oauth_redirect_uri
            if enable_space_settings is not None:
                payload["app"]["enable_space_settings"] = enable_space_settings

            # Make the PUT request to the appropriate endpoint
            resp = await client.put(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def delete_extension(extension_id: int, context: str = "org") -> dict:
        """
        Deletes an existing extension in the specified context (organization or partner).
        """
        try:
            # Determine the base URL based on the context
            if context == "org":
                url = f"https://mapi.storyblok.com/v1/org_apps/{extension_id}"
            elif context == "partner":
                url = f"https://mapi.storyblok.com/v1/partner_apps/{extension_id}"
            else:
                return {"isError": True, "content": [{"type": "text", "text": "Invalid context specified. Mention either 'org' or 'partner'"}]}

            # Make the DELETE request to the appropriate endpoint
            resp = await client.delete(url, headers=get_management_headers())
            if resp.status_code == 204:
                return {"isError": False, "content": [{"type": "text", "text": "Extension deleted successfully."}]}
            else:
                return {"isError": True, "content": [{"type": "text", "text": f"Failed to delete extension. Status code: {resp.status_code}"}]}
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def retrieve_extension_settings(space_id: int, extension_id: int) -> Any:
        """
        Retrieve settings for a specific extension in a space.
        """
        try:
            url = f"https://mapi.storyblok.com/v1/spaces/{space_id}/app_provisions/{extension_id}"
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def retrieve_all_extension_settings(space_id: int) -> Any:
        """
        Retrieve settings for all extensions installed in a space.
        """
        try:
            url = f"https://mapi.storyblok.com/v1/spaces/{space_id}/app_provisions/"
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    