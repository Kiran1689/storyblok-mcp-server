import json
from typing import Any, Optional, Dict, List, Union
from mcp.server.fastmcp import FastMCP
from httpx import AsyncClient
from utils.api import (
    build_management_url,
    get_management_headers,
    _handle_response,
    APIError,
)
from tools.components import get_component_schema_by_name

def register_stories(mcp: FastMCP, client: AsyncClient) -> None:
    
    @mcp.tool()
    async def fetch_stories(
        page: Optional[int] = 1,
        per_page: Optional[int] = 25,
        contain_component: Optional[str] = None,
        text_search: Optional[str] = None,
        sort_by: Optional[str] = None,
        pinned: Optional[bool] = None,
        excluding_ids: Optional[str] = None,
        by_ids: Optional[str] = None,
        by_uuids: Optional[str] = None,
        with_tag: Optional[str] = None,
        folder_only: Optional[bool] = None,
        story_only: Optional[bool] = None,
        with_parent: Optional[int] = None,
        starts_with: Optional[str] = None,
        in_trash: Optional[bool] = None,
        search: Optional[str] = None,
        filter_query: Optional[Union[str, Dict[str, Any]]] = None,
        in_release: Optional[int] = None,
        is_published: Optional[bool] = None,
        by_slugs: Optional[str] = None,
        mine: Optional[bool] = None,
        excluding_slugs: Optional[str] = None,
        in_workflow_stages: Optional[str] = None,
        by_uuids_ordered: Optional[str] = None,
        with_slug: Optional[str] = None,
        with_summary: Optional[bool] = None,
        scheduled_at_gt: Optional[str] = None,
        scheduled_at_lt: Optional[str] = None,
        favourite: Optional[bool] = None,
        reference_search: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Fetch multiple stories from Storyblok with advanced filtering and pagination.
        """
        try:
            url = build_management_url("/stories")
            # Build query parameters
            raw_params = locals()
            params = {"page": page, "per_page": per_page}
            for key, val in raw_params.items():
                if key in ["mcp", "client"] or val is None:
                    continue
                if isinstance(val, bool):
                    params[key] = 1 if val else 0
                elif isinstance(val, dict):
                    params[key] = json.dumps(val)
                else:
                    params[key] = val

            resp = await client.get(url, headers=get_management_headers(), params=params)
            data = _handle_response(resp, url)
            return {
                "stories": data.get("stories", []),
                "total": len(data.get("stories", [])),
                "page": page,
                "per_page": per_page
            }
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def get_story(
        story_id: int
    ) -> Any:
        """
        Retrieves a specific story by its ID.
        """
        try:
            url = build_management_url(f"/stories/{story_id}")
            resp = await client.get(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def create_story(
        name: str,
        slug: str,
        content: Dict[str, Any],
        parent_id: Optional[int] = None,
        group_id: Optional[str] = None,
        sort_by_date: Optional[str] = None,
        is_folder: bool = False,
        default_root: Optional[str] = None,
        disable_fe_editor: Optional[bool] = None,
        is_startpage: bool = False,
        meta_data: Optional[Dict[str, Any]] = None,
        pinned: Optional[bool] = None,
        translated_slugs_attributes: Optional[List[Dict[str, Any]]] = None,
        position: Optional[int] = None,
        publish: Optional[bool] = False,
        release_id: Optional[int] = None,
    ) -> Any:
        """
        Creates a new Storyblok story.
        Supports all documented fields including publishing.
        """
        try:
            # Construct story object with optional fields
            story_payload: Dict[str, Any] = {
                "name": name,
                "slug": slug,
                "content": content,
            }
            # Only include optional properties if provided
            for key, val in {
                "parent_id": parent_id,
                "group_id": group_id,
                "sort_by_date": sort_by_date,
                "is_folder": is_folder,
                "default_root": default_root,
                "disable_fe_editor": disable_fe_editor,
                "is_startpage": is_startpage,
                "meta_data": meta_data,
                "pinned": pinned,
                "translated_slugs_attributes": translated_slugs_attributes,
                "position": position,
                "release_id": release_id
            }.items():
                if val is not None:
                    story_payload[key] = val

            # Prepare request payload
            payload = {"story": story_payload}
            if publish:
                payload["publish"] = 1

            url = build_management_url("/stories")
            resp = await client.post(
                url,
                headers=get_management_headers(),
                json=payload
            )
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def update_story(
        story_id: int,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        content: Optional[Dict[str, Any]] = None,
        parent_id: Optional[int] = None,
        group_id: Optional[str] = None,
        sort_by_date: Optional[str] = None,
        tag_list: Optional[List[str]] = None,
        is_folder: Optional[bool] = None,
        path: Optional[str] = None,
        default_root: Optional[str] = None,
        disable_fe_editor: Optional[bool] = None,
        is_startpage: Optional[bool] = None,
        meta_data: Optional[Dict[str, Any]] = None,
        pinned: Optional[bool] = None,
        first_published_at: Optional[str] = None,
        translated_slugs_attributes: Optional[List[Dict[str, Any]]] = None,
        position: Optional[int] = None,
        force_update: Optional[Union[bool, int]] = None,
        release_id: Optional[int] = None,
        publish: Optional[bool] = False,
        lang: Optional[str] = None
    ) -> Any:
        """
        Updates an existing Storyblok story by ID.
        Supports all documented fields including publishing.
        """
        try:
            if not name and not slug and not content and not publish:
                return {"isError": True, "content": [{"type": "text", "text": "No update fields or publish flag provided."}]}

            payload_story: Dict[str, Any] = {}
            for key, val in {
                "name": name,
                "slug": slug,
                "content": content,
                "parent_id": parent_id,
                "group_id": group_id,
                "sort_by_date": sort_by_date,
                "tag_list": tag_list,
                "is_folder": is_folder,
                "path": path,
                "default_root": default_root,
                "disable_fe_editor": disable_fe_editor,
                "is_startpage": is_startpage,
                "meta_data": meta_data,
                "pinned": pinned,
                "first_published_at": first_published_at,
                "translated_slugs_attributes": translated_slugs_attributes,
                "position": position,
                "release_id": release_id,
                "lang": lang,
            }.items():
                if val is not None:
                    payload_story[key] = val

            if force_update:
                payload_story["force_update"] = "1"

            payload: Dict[str, Any] = {"story": payload_story}
            if publish:
                payload["publish"] = 1

            url = build_management_url(f"/stories/{story_id}")
            resp = await client.put(url, headers=get_management_headers(), json=payload)
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def delete_story(id: str) -> Any:
        """Deletes a story by ID."""
        try:
            url = build_management_url(f"/stories/{id}")
            resp = await client.delete(url, headers=get_management_headers())
            _handle_response(resp, url)
            return {"message": f"Story {id} has been successfully deleted."}
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def publish_story(
        story_id: int,
        lang: Optional[str] = None,
        release_id: Optional[int] = None
    ) -> Any:
        """
        Publishes a Storyblok story by its ID.
        """
        try:
            url = build_management_url(f"/stories/{story_id}/publish")
            params = {}
            if lang:
                params["lang"] = lang
            if release_id is not None:
                params["release_id"] = release_id

            resp = await client.get(url, headers=get_management_headers(), params=params)
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}



    @mcp.tool()
    async def unpublish_story(
        story_id: int,
        lang: Optional[str] = None
    ) -> Any:
        """
        Unpublishes a Storyblok story by its ID.
        """
        try:
            url = build_management_url(f"/stories/{story_id}/unpublish")
            params = {}
            if lang:
                params["lang"] = lang
            
            resp = await client.get(url, headers=get_management_headers(), params=params)
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}


    @mcp.tool()
    async def get_story_versions(
        by_story_id: int,
        version_id: Optional[int] = None,
        by_release_id: Optional[int] = None,
        page: Optional[int] = 1,
        per_page: Optional[int] = 25,
        show_content: Optional[bool] = False
    ) -> Any:
        """
        Retrieves versions (revisions) of stories.
        """
        try:
            url = build_management_url("/story_versions")
            params = {
                "by_story_id": by_story_id,
                "page": page,
                "per_page": min(per_page, 100)
            }
            if version_id is not None:
                params["version_id"] = version_id
            if by_release_id is not None:
                params["by_release_id"] = by_release_id
            if show_content:
                params["show_content"] = 1

            resp = await client.get(url, headers=get_management_headers(), params=params)
            data = _handle_response(resp, url)

            return {
                "versions": data.get("story_versions", []),
                "page": page,
                "per_page": params["per_page"],
                "total": data.get("total", None)
            }

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}


    @mcp.tool()
    async def restore_story(id: str, version_id: str) -> Any:
        """Restores a story to a specific version."""
        try:
            url = build_management_url(f"/stories/{id}/restore/{version_id}")
            resp = await client.post(url, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def validate_story_content(
        component_name: str,
        story_id: Optional[str] = None,
        story_content: Optional[Dict[str, Any]] = None,
        space_id: Optional[str] = None  # currently unused
    ) -> Any:
        """
        Validates a story's content against a component schema.
        Either provide story_id (to fetch) or story_content directly.
        """
        try:
            schema = await get_component_schema_by_name(component_name, space_id)
            if not schema:
                return {"isError": True, "content": [{"type": "text", "text": f"Error: Component schema '{component_name}' not found."}]}

            content = story_content
            if not content and story_id:
                url = build_management_url(f"/stories/{story_id}")
                resp = await client.get(url, headers=get_management_headers())
                story_data = _handle_response(resp, url)
                content = story_data.get("story", {}).get("content")

            if not content:
                return {"isError": True, "content": [{"type": "text", "text": "Error: story_id or story_content must be provided and valid."}]}

            errors, missing, extraneous = [], [], []
            for field, defn in schema.items():
                if defn.get("required") and content.get(field) is None:
                    missing.append(field)
                    errors.append({"field": field, "type": "missing_required", "message": f"Field '{field}' is required."})

            for field in content:
                if field not in schema:
                    extraneous.append(field)
                    errors.append({"field": field, "type": "extraneous_field", "message": f"Field '{field}' not in schema."})

            return {
                "isValid": not errors,
                "errors": errors,
                "missingFields": missing,
                "extraneousFields": extraneous,
                "validatedComponentName": component_name,
                "storyIdProcessed": story_id or "N/A"
            }

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def debug_story_access(story_id: str) -> Any:
        """Debug access to a specific story via various fetch parameters."""
        api_call_attempts = []
        issues = []
        suggestions = []
        draft_details = {"accessible": False, "contentPresent": False, "fromScenario": ""}
        pub_details = {"accessible": False, "contentPresent": False, "fromScenario": ""}

        scenarios = [
            ("Default (likely draft)", {}),
            ("Published", {"version": "published"}),
            ("Draft explicit", {"version": "draft"}),
            ("Draft with content", {"version": "draft", "with_content": "1"}),
            ("Published with content", {"version": "published", "with_content": "1"}),
        ]

        for name, params in scenarios:
            attempt = {"scenarioName": name, "paramsUsed": {**params, "story_id": story_id}}
            try:
                resp = await client.get(
                    build_management_url(f"/stories/{story_id}"),
                    headers=get_management_headers(),
                    params=params
                )
                data = _handle_response(resp, resp.url)
                story = data.get("story", {})
                content_present = bool(story.get("content"))
                attempt.update({
                    "status": resp.status_code,
                    "responseData": {
                        "id": story.get("id"),
                        "name": story.get("name"),
                        "published_at": story.get("published_at"),
                        "full_slug": story.get("full_slug"),
                        "content_present": content_present,
                        "content_component": story.get("content", {}).get("component"),
                        "version": story.get("version"),
                    }
                })

                if params.get("version") == "published":
                    if not pub_details["accessible"] or (content_present and not pub_details["contentPresent"]):
                        pub_details.update({"accessible": True, "contentPresent": content_present, "fromScenario": name})
                    if story.get("published_at") is None:
                        issues.append(f"Scenario '{name}': fetched as published but no published_at.")
                else:
                    if not draft_details["accessible"] or (content_present and not draft_details["contentPresent"]):
                        draft_details.update({"accessible": True, "contentPresent": content_present, "fromScenario": name})

                if params.get("with_content") and not content_present:
                    issues.append(f"Scenario '{name}': with_content=1 used but no content present.")
            except APIError as e:
                parsed = {}
                try:
                    parsed = json.loads(str(e))
                    attempt["status"] = int(parsed.get("error", "").split(" ")[0])
                    attempt["errorDetails"] = parsed
                except:
                    attempt["status"] = "ERROR"
                    attempt["errorDetails"] = str(e)
            api_call_attempts.append(attempt)

        # Analyze and generate suggestions
        if draft_details["accessible"] and not pub_details["accessible"]:
            suggestions.append("Accessible in draft but not published. Might be unpublished.")
        if pub_details["accessible"] and not draft_details["accessible"]:
            issues.append("Accessible in published but not draft.")
        if draft_details["accessible"] and pub_details["accessible"]:
            if draft_details["contentPresent"] and not pub_details["contentPresent"]:
                suggestions.append("Published version doesn't include content; try with_content=1.")
            if pub_details["contentPresent"] and not draft_details["contentPresent"]:
                suggestions.append("Draft version doesn't include content; try with_content=1.")
        if not draft_details["accessible"] and not pub_details["accessible"]:
            issues.append("Story not accessible in any scenario.")
            suggestions.append("Check story ID and token permissions.")
        all_404 = all(att.get("status") == 404 for att in api_call_attempts)
        if all_404:
            issues.append("All attempts returned 404 Not Found.")
            suggestions.append("Verify the story exists and isn't deleted.")
        any_403 = any(att.get("status") == 403 for att in api_call_attempts)
        if any_403:
            issues.append("One or more attempts resulted in 403 Forbidden.")
            suggestions.append("Check that your API token has proper permissions.")

        return {
            "storyId": story_id,
            "accessibleAsDraftDetails": draft_details,
            "accessibleAsPublishedDetails": pub_details,
            "issuesDetected": list(set(issues)),
            "suggestions": list(set(suggestions)),
            "apiCallAttempts": api_call_attempts
        }

    @mcp.tool()
    async def bulk_publish_stories(story_ids: List[str]) -> Any:
        """Publishes multiple stories by ID."""
        results = []
        success = fail = 0
        for sid in story_ids:
            try:
                resp = await client.post(
                    build_management_url(f"/stories/{sid}/publish"),
                    headers=get_management_headers()
                )
                data = _handle_response(resp, resp.url)
                results.append({"id": sid, "status": "success", "data": data})
                success += 1
            except APIError as e:
                results.append({"id": sid, "status": "error", "error": str(e)})
                fail += 1
        return {"total_processed": len(story_ids), "successful_operations": success,
                "failed_operations": fail, "results": results}


    @mcp.tool()
    async def bulk_delete_stories(story_ids: List[str]) -> Any:
        """Deletes multiple stories in Storyblok."""
        results = []
        success = fail = 0
        for sid in story_ids:
            try:
                resp = await client.delete(
                    build_management_url(f"/stories/{sid}"),
                    headers=get_management_headers()
                )
                _handle_response(resp, resp.url)
                results.append({"id": sid, "status": "success"})
                success += 1
            except APIError as e:
                results.append({
                    "id": sid,
                    "status": "error",
                    "error": str(e)
                })
                fail += 1
        return {
            "total_processed": len(story_ids),
            "successful_operations": success,
            "failed_operations": fail,
            "results": results
        }

    @mcp.tool()
    async def bulk_update_stories(
        stories: List[Dict[str, Any]]
    ) -> Any:
        """Updates multiple stories in Storyblok, optionally publishing them."""
        results = []
        success = fail = 0

        for story_update in stories:
            sid = story_update.get("id")
            publish = story_update.pop("publish", False)
            update_fields = {k: v for k, v in story_update.items() if v is not None}
            try:
                resp = await client.put(
                    build_management_url(f"/stories/{sid}"),
                    headers=get_management_headers(),
                    json={"story": update_fields}
                )
                data = _handle_response(resp, resp.url)
                published = False

                if publish:
                    try:
                        publish_resp = await client.post(
                            build_management_url(f"/stories/{sid}/publish"),
                            headers=get_management_headers()
                        )
                        _handle_response(publish_resp, publish_resp.url)
                        published = True
                    except APIError:
                        pass  # Publishing errors don't block update success

                results.append({
                    "id": sid,
                    "status": "success",
                    "data": data,
                    "published": published
                })
                success += 1
            except APIError as e:
                results.append({
                    "id": sid,
                    "status": "error",
                    "error": str(e)
                })
                fail += 1

        return {
            "total_processed": len(stories),
            "successful_operations": success,
            "failed_operations": fail,
            "results": results
        }

    @mcp.tool()
    async def bulk_create_stories(
        stories: List[Dict[str, Any]]
    ) -> Any:
        """Creates multiple stories in Storyblok."""
        results = []
        success = fail = 0

        for story_input in stories:
            try:
                resp = await client.post(
                    build_management_url("/stories"),
                    headers=get_management_headers(),
                    json={"story": story_input}
                )
                data = _handle_response(resp, resp.url)
                results.append({
                    "input": story_input,
                    "id": data.get("story", {}).get("id"),
                    "slug": data.get("story", {}).get("slug"),
                    "status": "success",
                    "data": data
                })
                success += 1
            except APIError as e:
                results.append({
                    "input": story_input,
                    "slug": story_input.get("slug"),
                    "status": "error",
                    "error": str(e)
                })
                fail += 1

        return {
            "total_processed": len(stories),
            "successful_operations": success,
            "failed_operations": fail,
            "results": results
        }

    
    @mcp.tool()
    async def get_unpublished_dependencies(
        story_ids: List[int],
        release_id: Optional[int] = None
    ) -> Any:
        """
        Retrieves unpublished dependencies for one or more stories.
        """
        try:
            url = build_management_url("/stories/unpublished_dependencies")
            payload: Dict[str, Any] = {"story_ids": story_ids}
            if release_id is not None:
                payload["release_id"] = release_id

            resp = await client.post(
                url,
                headers=get_management_headers(),
                json=payload
            )
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    @mcp.tool()
    async def ai_translate_story(
        space_id: int,
        story_id: int,
        lang: str,
        code: str,
        overwrite: bool = False,
        release_id: Optional[int] = None
    ) -> Any:
        """
        Translates a story's content into a specified language using AI.
        """
        try:
            url = build_management_url(f"/spaces/{space_id}/stories/{story_id}/ai_translate")
            payload = {
                "lang": lang,
                "code": code,
                "overwrite": overwrite
            }
            if release_id:
                payload["release_id"] = release_id

            resp = await client.put(
                url,
                headers=get_management_headers(),
                json=payload
            )
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}

    @mcp.tool()
    async def compare_story_versions(
        story_id: int,
        version_v2: int
    ) -> Any:
        """
        Compares two versions of a story to identify changes.
        """
        try:
            url = build_management_url(f"/stories/{story_id}/compare")
            params = {"version_v2": version_v2}
            resp = await client.get(
                url,
                headers=get_management_headers(),
                params=params
            )
            return _handle_response(resp, url)

        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
        
    


