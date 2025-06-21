from typing import Any
from httpx import AsyncClient
from mcp.server.fastmcp import FastMCP
from utils.api import build_management_url, get_management_headers, _handle_response, APIError

def register_branch_deployments(mcp: FastMCP, client: AsyncClient) -> None:

    @mcp.tool()
    async def create_branch_deployment(
        branch_id: int,
        release_uuids: list[str]
    ) -> Any:
        """
        Triggers a deployment of specified releases to a given branch (pipeline stage).

        - branch_id: Numeric ID of the branch to deploy to.
        - release_uuids: List of release UUIDs to deploy.
        """
        try:
            payload = {
                "branch_id": branch_id,
                "release_uuids": release_uuids
            }
            url = build_management_url("/deployments/")
            resp = await client.post(url, json=payload, headers=get_management_headers())
            return _handle_response(resp, url)
        except APIError as e:
            return {"isError": True, "content": [{"type": "text", "text": str(e)}]}
