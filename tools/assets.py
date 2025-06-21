import json
from typing import Optional, Dict, Any, Literal, List
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import (
    build_management_url,
    get_management_headers,
    _handle_response,
    create_pagination_params,
    add_optional_params,
    APIError,
)
from datetime import datetime


def register_assets(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def fetch_assets(
        page: Optional[int] = 1,
        per_page: Optional[int] = 25,
        search: Optional[str] = None,
        folder_id: Optional[int] = None,
        sort_by: Optional[Literal[
            "created_at:asc", "created_at:desc",
            "updated_at:asc", "updated_at:desc",
            "short_filename:asc", "short_filename:desc"
        ]] = None,
        is_private: Optional[bool] = None,
        by_alt: Optional[str] = None,
        by_title: Optional[str] = None,
        by_copyright: Optional[str] = None,
        with_tags: Optional[str] = None
    ) -> Any:
        """
        Retrieve multiple assets from Storyblok Management API.
        """
        try:
            params = create_pagination_params(page, per_page)
            add_optional_params(params, {
                "search": search,
                "in_folder": folder_id,
                "sort_by": sort_by,
                "is_private": "1" if is_private else None,
                "by_alt": by_alt,
                "by_title": by_title,
                "by_copyright": by_copyright,
                "with_tags": with_tags,
            })
            url = build_management_url("/assets")
            resp = await client.get(url, params=params, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def get_asset(id: str) -> Any:
        """Gets a specific asset by ID."""
        try:
            url = build_management_url(f"/assets/{id}")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def delete_asset(id: str) -> Any:
        """Deletes an asset from Storyblok."""
        try:
            url = build_management_url(f"/assets/{id}")
            resp = await client.delete(url, headers=get_management_headers())
            _handle_response(resp, url)
            return {"content": [{"type": "text", "text": f"Asset {id} has been successfully deleted."}]}
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def update_asset(
        asset_id: int,
        asset_folder_id: Optional[int] = None,
        internal_tag_ids: Optional[List[int]] = None,
        locked: Optional[bool] = None,
        is_private: Optional[bool] = None,
        publish_at: Optional[datetime] = None,
        expire_at: Optional[datetime] = None,
        focus: Optional[str] = None,
        alt: Optional[str] = None,
        title: Optional[str] = None,
        source: Optional[str] = None,
        copyright: Optional[str] = None,
        meta_data: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Update an existing asset’s metadata or settings.
        """
        try:
            payload: Dict[str, Any] = {}
            # Core fields
            for field, value in [
                ("asset_folder_id", asset_folder_id),
                ("internal_tag_ids", internal_tag_ids),
                ("locked", locked),
                ("is_private", is_private),
                ("publish_at", publish_at.isoformat() if publish_at else None),
                ("expire_at", expire_at.isoformat() if expire_at else None),
                ("focus", focus),
            ]:
                if value is not None:
                    payload[field] = value

            # Metadata fields
            md: Dict[str, Any] = meta_data or {}
            for field, value in [
                ("alt", alt),
                ("title", title),
                ("source", source),
                ("copyright", copyright),
            ]:
                if value is not None and field not in md:
                    md[field] = value
            if md:
                payload["meta_data"] = md

            url = build_management_url(f"/assets/{asset_id}")
            resp = await client.put(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def delete_multiple_assets(
        ids: List[int]
    ) -> Any:
        """
        Deletes multiple assets by numeric IDs using the Storyblok Management API.
        """
        if not ids:
            return {"isError": True, "content": [{"type": "text", "text": "ids list cannot be empty"}]}

        try:
            payload = {"ids": ids}
            url = build_management_url("/assets/bulk_destroy")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
    

    @mcp.tool()
    async def bulk_move_assets(
        ids: List[int],
        asset_folder_id: int
    ) -> Any:
        """
        Move multiple assets to a specified folder.
        """
        if not ids:
            return {"isError": True, "content": [{"type": "text", "text": "ids list cannot be empty"}]}
        if not isinstance(asset_folder_id, int):
            return {"isError": True, "content": [{"type": "text", "text": "asset_folder_id must be an integer"}]}

        try:
            payload = {
                "ids": ids,
                "asset_folder_id": asset_folder_id
            }
            url = build_management_url("/assets/bulk_update")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        

    @mcp.tool()
    async def bulk_restore_assets(
        ids: List[int]
    ) -> Any:
        """
        Restores multiple previously deleted assets
        """
        if not ids:
            return {"isError": True, "content": [{"type": "text", "text": "ids list cannot be empty"}]}

        try:
            payload = {"ids": ids}
            url = build_management_url("/assets/bulk_restore")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}



    @mcp.tool()
    async def init_asset_upload(filename: str, size: int, content_type: str) -> Any:
        """Initializes asset upload and returns signed S3 upload URL."""
        try:
            url = build_management_url("/assets")
            payload = {"filename": filename, "size": size, "content_type": content_type}
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def complete_asset_upload(asset_id: str) -> Any:
        """Completes the asset upload process after S3 upload."""
        try:
            url = build_management_url(f"/assets/{asset_id}/finish_upload")
            resp = await client.post(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

