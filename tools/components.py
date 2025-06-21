import json
import requests
from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import FastMCP
from httpx import AsyncClient
from config import API_ENDPOINTS
from utils.api import (
    build_management_url,
    get_management_headers,
    _handle_response,
    APIError,
)

def register_components(mcp: FastMCP, client: AsyncClient) -> None:
    """
    @mcp.tool()
    async def fetch_components(
        component_summary: Optional[bool] = False,
        include_schema_details: Optional[bool] = True,
        filter_by_name: Optional[str] = None
    ) -> Dict[str, Any]:
        # Fetches components, optionally filtering and shaping the response.
        try:
            url = build_management_url("/components")
            resp = await client.get(url, headers=get_management_headers())
            data = _handle_response(resp, url)
            comps = data.get("components", [])

            # Name filter
            if filter_by_name:
                fl = filter_by_name.lower()
                comps = [c for c in comps
                         if fl in (c.get("name", "").lower() + c.get("display_name", "").lower())]

            # Summaries or remove schema
            if component_summary:
                comps = [{"id": c["id"], "name": c["name"], "display_name": c["display_name"]} for c in comps]
            elif not include_schema_details:
                comps = [{k: v for k, v in c.items() if k != "schema"} for c in comps]

            return {"components_count": len(comps), "components": comps}
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
    """

    @mcp.tool()
    async def fetch_components(
        component_summary: bool = False,
        include_schema_details: bool = True,
        filter_by_name: Optional[str] = None,
        is_root: Optional[bool] = None,
        in_group: Optional[int] = None,
        sort_by: Optional[str] = None,
        per_page: Optional[int] = None,  # not used since non-paginated
    ) -> Dict[str, Any]:
        """Fetches components with server-side filters, sorting, and option to include groups."""
        try:
            url = build_management_url("/components")
            params = {}
            if filter_by_name:
                params["search"] = filter_by_name
            if is_root is not None:
                params["is_root"] = 1 if is_root else 0
            if in_group is not None:
                params["in_group"] = in_group
            if sort_by:
                params["sort_by"] = sort_by
            if per_page:
                params["per_page"] = per_page

            resp = await client.get(url, headers=get_management_headers(), params=params)
            data = _handle_response(resp, url)
            components = data.get("components", [])
            
            # Summaries or remove schema if requested
            if component_summary:
                components = [
                    {"id": c["id"], "name": c["name"], "display_name": c["display_name"]}
                    for c in components
                ]
            elif not include_schema_details:
                components = [{k: v for k, v in c.items() if k != "schema"} for c in components]

            # Also fetch component groups (folders)
            # API returns component_groups at /component_groups endpoint
            groups_url = build_management_url("/component_groups")
            grp_resp = await client.get(groups_url, headers=get_management_headers(), params={})
            groups_data = _handle_response(grp_resp, groups_url).get("component_groups", [])

            return {
                "components_count": len(components),
                "components": components,
                "component_groups": groups_data
            }

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    
    @mcp.tool()
    async def get_component(id: str) -> Dict[str, Any]:
        """Gets a specific component by ID."""
        try:
            url = build_management_url(f"/components/{id}")
            resp = await client.get(url, headers=get_management_headers())
            data = _handle_response(resp, url)
            return data
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
    """
    @mcp.tool()
    async def create_component(
        name: str,
        display_name: Optional[str] = None,
        schema: Dict[str, Any] = {},
        is_root: Optional[bool] = False,
        is_nestable: Optional[bool] = True
    ) -> Dict[str, Any]:
        #Creates a new component (block).
        try:
            url = build_management_url("/components")
            payload = {"component": {
                "name": name,
                "display_name": display_name or name,
                "schema": schema,
                "is_root": is_root,
                "is_nestable": is_nestable
            }}
            resp = await client.post(url, headers=get_management_headers(), content=json.dumps(payload))
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
    """
    @mcp.tool()
    async def create_component(
        name: str,
        display_name: Optional[str] = None,
        schema: Dict[str, Any] = {},
        is_root: Optional[bool] = False,
        is_nestable: Optional[bool] = True,
        preview_field: Optional[str] = None,
        preview_tmpl: Optional[str] = None,
        component_group_uuid: Optional[str] = None,
        color: Optional[str] = None,
        icon: Optional[str] = None,
        internal_tag_ids: Optional[List[str]] = None,
        content_type_asset_preview: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Creates a new component with all supported fields."""
        try:
            url = build_management_url("/components")
            payload_comp: Dict[str, Any] = {
                "name": name,
                "display_name": display_name or name,
                "schema": schema,
                "is_root": is_root,
                "is_nestable": is_nestable,
            }
            # Optional fields
            for key, val in {
                "preview_field": preview_field,
                "preview_tmpl": preview_tmpl,
                "component_group_uuid": component_group_uuid,
                "color": color,
                "icon": icon,
                "internal_tag_ids": internal_tag_ids,
                "content_type_asset_preview": content_type_asset_preview
            }.items():
                if val is not None:
                    payload_comp[key] = val

            resp = await client.post(
                url,
                headers=get_management_headers(),
                content=json.dumps({"component": payload_comp})
            )
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    """
    @mcp.tool()
    async def update_component(
        id: str,
        name: Optional[str] = None,
        display_name: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None,
        is_root: Optional[bool] = None,
        is_nestable: Optional[bool] = None
    ) -> Dict[str, Any]:
        #Updates an existing component.
        try:
            url = build_management_url(f"/components/{id}")
            comp_data: Dict[str, Any] = {}
            for k, v in (("name", name), ("display_name", display_name),
                         ("schema", schema), ("is_root", is_root),
                         ("is_nestable", is_nestable)):
                if v is not None:
                    comp_data[k] = v
            resp = await client.put(url, headers=get_management_headers(), content=json.dumps({"component": comp_data}))
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
    """

    @mcp.tool()
    async def update_component(
        id: str,
        name: Optional[str] = None,
        display_name: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None,
        image: Optional[str] = None,
        preview_field: Optional[str] = None,
        preview_tmpl: Optional[str] = None,
        is_root: Optional[bool] = None,
        is_nestable: Optional[bool] = None,
        component_group_uuid: Optional[str] = None,
        color: Optional[str] = None,
        icon: Optional[str] = None,
        internal_tag_ids: Optional[List[str]] = None,
        content_type_asset_preview: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Updates an existing component with all supported fields."""
        try:
            url = build_management_url(f"/components/{id}")
            comp_data: Dict[str, Any] = {}

            # Populate only provided fields
            for key, val in {
                "name": name,
                "display_name": display_name,
                "schema": schema,
                "image": image,
                "preview_field": preview_field,
                "preview_tmpl": preview_tmpl,
                "is_root": is_root,
                "is_nestable": is_nestable,
                "component_group_uuid": component_group_uuid,
                "color": color,
                "icon": icon,
                "internal_tag_ids": internal_tag_ids,
                "content_type_asset_preview": content_type_asset_preview
            }.items():
                if val is not None:
                    comp_data[key] = val

            resp = await client.put(
                url,
                headers=get_management_headers(),
                content=json.dumps({"component": comp_data})
            )
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}


    @mcp.tool()
    async def delete_component(id: str) -> Dict[str, Any]:
        """Deletes a component by ID."""
        try:
            url = build_management_url(f"/components/{id}")
            resp = await client.delete(url, headers=get_management_headers())
            _handle_response(resp, url)
            return {"message": f"Component {id} has been successfully deleted."}
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def get_component_usage(component_name: str) -> Dict[str, Any]:
        """Finds stories where a component is used in content (draft & published)."""
        MAX_PAGES = 10
        PER_PAGE = 100
        stories_map: Dict[int, Dict[str, Any]] = {}
        limit_reached = False

        async def fetch_page(version: str, page: int):
            url = (build_management_url("/stories")
                   + f"?page={page}&per_page={PER_PAGE}&with_content=1&version={version}")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)

        for version in ("published", "draft"):
            page = 1
            while page <= MAX_PAGES:
                try:
                    data = await fetch_page(version, page)
                    for st in data.get("stories", []):
                        stories_map[st["id"]] = st
                    if len(data.get("stories", [])) < PER_PAGE:
                        break
                    page += 1
                except APIError:
                    break
            else:
                limit_reached = True

        used = []
        def search(val: Any) -> bool:
            if isinstance(val, list):
                return any(search(v) for v in val)
            if isinstance(val, dict):
                if val.get("component") == component_name:
                    return True
                return any(search(v) for v in val.values())
            return False

        for st in stories_map.values():
            if search(st.get("content", {})):
                used.append({k: st[k] for k in ("id", "name", "slug", "full_slug")})

        return {
            "component_name": component_name,
            "usage_count": len(used),
            "stories_analyzed_count": len(stories_map),
            "search_limit_reached": limit_reached,
            "used_in_stories": used
        }
    
    @mcp.tool()
    async def retrieve_component_versions(
        component_id: str,
        page: Optional[int] = 1,
        per_page: Optional[int] = 25
    ) -> Dict[str, Any]:
        """
        Retrieves paginated versions of a component.
        """
        try:
            url = build_management_url("/versions")
            params = {
                "model": "components",
                "model_id": component_id,
                "page": page,
                "per_page": min(per_page, 100)
            }
            resp = await client.get(
                url,
                headers=get_management_headers(),
                params=params
            )
            data = _handle_response(resp, url)
            versions = data.get("versions", [])

            return {
                "versions": versions,
                "page": page,
                "per_page": params["per_page"],
                "total_versions": len(versions)
            }

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def retrieve_single_component_version(
        component_id: str,
        version_id: str
    ) -> Dict[str, Any]:
        """
        Retrieves the schema details of a specific component version.
        """
        try:
            url = build_management_url(
                f"/components/{component_id}/component_versions/{version_id}"
            )
            resp = await client.get(
                url,
                headers=get_management_headers()
            )
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def restore_component_version(
        version_id: str,
        component_id: str,
    ) -> Dict[str, Any]:
        """
        Restores a component to a previous version.
        """
        try:
            path = f"/versions/{version_id}"
            
            url = build_management_url(path)

            payload = {
                "model": "components",
                "model_id": component_id
            }
            resp = await client.put(
                url,
                headers=get_management_headers(),
                content=json.dumps(payload)
            )
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}



def get_component_schema_by_name(component_name: str, space_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Fetches the schema of a component by its name from the Storyblok Management API.

    Args:
        component_name (str): The name of the component to retrieve.
        space_id (Optional[str]): Placeholder for future use (e.g., handling different spaces or credentials).

    Returns:
        Optional[Dict[str, Any]]: The schema of the component if found, otherwise None.
    """

    # Future support for space-specific logic
    if space_id:
        # Placeholder for handling alternate tokens or clients per space
        pass

    endpoint = build_management_url('/components')
    response = requests.get(endpoint, headers=get_management_headers())
    data = _handle_response(response, endpoint)

    if data and isinstance(data.get("components"), list):
        for component in data["components"]:
            if component.get("name") == component_name:
                return component.get("schema") or None

    return None