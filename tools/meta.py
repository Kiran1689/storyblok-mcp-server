from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP


def register_meta(mcp: FastMCP, all_tools_info: List[Dict[str, str]]) -> None:
    """
    Registers meta-tools with the MCP server.

    :param mcp: The MCP server instance.
    :param all_tools_info: A list of dictionaries with 'name' and 'description' keys for each tool.
    """

    @mcp.tool()
    async def list_tools() -> Any:
        """Lists all available tools with their names, descriptions, and total count."""
        try:
            if not all_tools_info:
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": "Available tools: No tool information was provided to list_tools."
                        }
                    ]
                }

            formatted = [
                f"{tool['name']}: {tool.get('description', '')}".strip()
                for tool in all_tools_info
            ]

            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Available tools (total: {len(all_tools_info)}):\n" + "\n".join(formatted)
                    }
                ],
                "total_tools": len(all_tools_info)
            }

        except Exception as e:
            return {
                "isError": True,
                "content": [
                    {
                        "type": "text",
                        "text": f"Error listing tools: {str(e)}"
                    }
                ]
            }

