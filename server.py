import sys
import signal
from mcp.server.fastmcp import FastMCP
from config import Config
from tools.components import register_components
from tools.components_folder import register_components_folder
from tools.stories import register_stories
from tools.assets import register_assets
from tools.assets_folder import register_assets_folder
from tools.tags import register_tags
from tools.meta import register_meta
from tools.releases import register_releases
from tools.data_sources import register_datasources
from tools.datasource_entries import register_datasource_entries
from tools.space import register_space
from tools.space_roles import register_space_roles
from tools.ping import register_ping
from tools.presets import register_presets
from tools.access_tokens import register_access_tokens
from tools.workflows import register_workflows
from tools.workflow_stage import register_workflow_stages
from tools.workflow_stage_changes import register_workflow_stage_changes
from tools.scheduling_stories import register_story_schedules
from tools.pipelines import register_branches
from tools.branch_deployments import register_branch_deployments
from tools.discussions import register_discussions
from tools.tasks import register_tasks
from tools.webhooks import register_webhooks
from tools.collaborators import register_collaborators
from tools.internal_tags import register_internal_tags
from tools.approvals import register_approvals
from tools.activities import register_activities
from tools.extensions import register_extensions
from tools.field_plugins import register_field_plugin_retrieval
from httpx import AsyncClient

# Load and validate config (space ID, tokens)
cfg = Config()
client = AsyncClient() 

# Create MCP server instance with name/version
mcp = FastMCP(name="storyblok-mcp-server", version="1.0.0")

all_tools_info = [
    # access_tokens.py
    {"name": "retrieve_multiple_access_tokens", "description": "Retrieve multiple access tokens."},
    {"name": "create_access_token", "description": "Create a new access token."},
    {"name": "update_access_token", "description": "Update an existing access token."},
    {"name": "delete_access_token", "description": "Delete an access token."},

    # activities.py
    {"name": "retrieve_multiple_activities", "description": "Retrieve multiple activities."},
    {"name": "retrieve_single_activity", "description": "Retrieve a single activity."},

    # approvals.py
    {"name": "retrieve_multiple_approvals", "description": "Retrieve multiple approvals."},
    {"name": "retrieve_single_approval", "description": "Retrieve a single approval."},
    {"name": "create_approval", "description": "Create a new approval."},
    {"name": "create_release_approval", "description": "Create a release approval."},
    {"name": "delete_approval", "description": "Delete an approval."},

    # assets.py
    {"name": "fetch_assets", "description": "Fetch assets."},
    {"name": "get_asset", "description": "Get an asset by ID."},
    {"name": "delete_asset", "description": "Delete an asset by ID."},
    {"name": "update_asset", "description": "Update an asset."},
    {"name": "delete_multiple_assets", "description": "Delete multiple assets."},
    {"name": "bulk_move_assets", "description": "Bulk move assets."},
    {"name": "bulk_restore_assets", "description": "Bulk restore assets."},
    {"name": "init_asset_upload", "description": "Initialize asset upload."},
    {"name": "complete_asset_upload", "description": "Complete asset upload."},

    # assets_folder.py
    {"name": "retrieve_asset_folders", "description": "Retrieve asset folders."},
    {"name": "fetch_asset_folder", "description": "Fetch an asset folder."},
    {"name": "create_asset_folder", "description": "Create an asset folder."},
    {"name": "update_asset_folder", "description": "Update an asset folder."},
    {"name": "delete_asset_folder", "description": "Delete an asset folder."},

    # branch_deployments.py
    {"name": "create_branch_deployment", "description": "Create a branch deployment."},

    # collaborators.py
    {"name": "retrieve_multiple_collaborators", "description": "Retrieve multiple collaborators."},
    {"name": "update_collaborator", "description": "Update a collaborator."},
    {"name": "delete_collaborator", "description": "Delete a collaborator."},

    # components.py
    {"name": "fetch_components", "description": "Fetch components."},
    {"name": "get_component", "description": "Get a component by ID."},
    {"name": "create_component", "description": "Create a component."},
    {"name": "update_component", "description": "Update a component."},
    {"name": "delete_component", "description": "Delete a component."},
    {"name": "get_component_usage", "description": "Get component usage."},
    {"name": "retrieve_component_versions", "description": "Retrieve component versions."},
    {"name": "retrieve_single_component_version", "description": "Retrieve a single component version."},
    {"name": "restore_component_version", "description": "Restore a component version."},

    # components_folder.py
    {"name": "create_component_folder", "description": "Create a component folder."},
    {"name": "update_component_folder", "description": "Update a component folder."},
    {"name": "delete_component_folder", "description": "Delete a component folder."},
    {"name": "fetch_component_folders", "description": "Fetch component folders."},
    {"name": "retrieve_single_component_folder", "description": "Retrieve a single component folder."},

    # datasource_entries.py
    {"name": "retrieve_multiple_datasource_entries", "description": "Retrieve multiple datasource entries."},
    {"name": "retrieve_single_datasource_entry", "description": "Retrieve a single datasource entry."},
    {"name": "create_datasource_entry", "description": "Create a datasource entry."},
    {"name": "update_datasource_entry", "description": "Update a datasource entry."},
    {"name": "delete_datasource_entry", "description": "Delete a datasource entry."},

    # data_sources.py
    {"name": "retrieve_multiple_datasources", "description": "Retrieve multiple datasources."},
    {"name": "retrieve_single_datasource", "description": "Retrieve a single datasource."},
    {"name": "create_datasource", "description": "Create a datasource."},
    {"name": "update_datasource", "description": "Update a datasource."},
    {"name": "delete_datasource", "description": "Delete a datasource."},

    # discussions.py
    {"name": "retrieve_multiple_discussions", "description": "Retrieve multiple discussions."},
    {"name": "retrieve_specific_discussion", "description": "Retrieve a specific discussion."},
    {"name": "retrieve_idea_discussions_comments", "description": "Retrieve idea discussions comments."},
    {"name": "create_discussion", "description": "Create a discussion."},
    {"name": "retrieve_my_discussions", "description": "Retrieve my discussions."},
    {"name": "resolve_discussion", "description": "Resolve a discussion."},
    {"name": "retrieve_multiple_comments", "description": "Retrieve multiple comments."},
    {"name": "create_comment", "description": "Create a comment."},
    {"name": "update_comment", "description": "Update a comment."},
    {"name": "delete_comment", "description": "Delete a comment."},

    # extensions.py
    {"name": "retrieve_all_extensions", "description": "Retrieve all extensions."},
    {"name": "retrieve_extension", "description": "Retrieve an extension."},
    {"name": "create_extension", "description": "Create an extension."},
    {"name": "update_extension", "description": "Update an extension."},
    {"name": "delete_extension", "description": "Delete an extension."},
    {"name": "retrieve_extension_settings", "description": "Retrieve extension settings."},
    {"name": "retrieve_all_extension_settings", "description": "Retrieve all extension settings."},

    # field_plugins.py
    {"name": "retrieve_field_plugins", "description": "Retrieve field plugins."},
    {"name": "retrieve_field_plugin", "description": "Retrieve a field plugin."},
    {"name": "create_field_plugin", "description": "Create a field plugin."},
    {"name": "update_field_plugin", "description": "Update a field plugin."},
    {"name": "delete_field_plugin", "description": "Delete a field plugin."},

    # internal_tags.py
    {"name": "retrieve_multiple_internal_tags", "description": "Retrieve multiple internal tags."},
    {"name": "create_internal_tag", "description": "Create an internal tag."},
    {"name": "update_internal_tag", "description": "Update an internal tag."},
    {"name": "delete_internal_tag", "description": "Delete an internal tag."},

    # meta.py
    {"name": "list_tools", "description": "List all available tools."},

    # ping.py
    {"name": "ping", "description": "Ping the server."},

    # pipelines.py
    {"name": "retrieve_multiple_branches", "description": "Retrieve multiple branches."},
    {"name": "retrieve_single_branch", "description": "Retrieve a single branch."},
    {"name": "create_branch", "description": "Create a branch."},
    {"name": "update_branch", "description": "Update a branch."},
    {"name": "delete_branch", "description": "Delete a branch."},

    # presets.py
    {"name": "retrieve_multiple_presets", "description": "Retrieve multiple presets."},
    {"name": "retrieve_single_preset", "description": "Retrieve a single preset."},
    {"name": "create_preset", "description": "Create a preset."},
    {"name": "update_preset", "description": "Update a preset."},
    {"name": "delete_preset", "description": "Delete a preset."},

    # releases.py
    {"name": "retrieve_multiple_releases", "description": "Retrieve multiple releases."},
    {"name": "retrieve_single_release", "description": "Retrieve a single release."},
    {"name": "create_release", "description": "Create a release."},
    {"name": "update_release", "description": "Update a release."},
    {"name": "delete_release", "description": "Delete a release."},

    # scheduling_stories.py
    {"name": "retrieve_multiple_story_schedules", "description": "Retrieve multiple story schedules."},
    {"name": "retrieve_one_story_schedule", "description": "Retrieve one story schedule."},
    {"name": "create_story_schedule", "description": "Create a story schedule."},
    {"name": "update_story_schedule", "description": "Update a story schedule."},
    {"name": "delete_story_schedule", "description": "Delete a story schedule."},

    # space.py
    {"name": "fetch_spaces", "description": "Fetch spaces."},
    {"name": "get_space", "description": "Get a space."},
    {"name": "create_space", "description": "Create a space."},
    {"name": "update_space", "description": "Update a space."},
    {"name": "duplicate_space", "description": "Duplicate a space."},
    {"name": "backup_space", "description": "Backup a space."},
    {"name": "delete_space", "description": "Delete a space."},

    # space_roles.py
    {"name": "fetch_space_roles", "description": "Fetch space roles."},
    {"name": "get_space_role", "description": "Get a space role."},
    {"name": "create_space_role", "description": "Create a space role."},
    {"name": "update_space_role", "description": "Update a space role."},
    {"name": "delete_space_role", "description": "Delete a space role."},

    # stories.py
    {"name": "fetch_stories", "description": "Fetch stories."},
    {"name": "get_story", "description": "Get a story."},
    {"name": "create_story", "description": "Create a story."},
    {"name": "update_story", "description": "Update a story."},
    {"name": "delete_story", "description": "Delete a story."},
    {"name": "publish_story", "description": "Publish a story."},
    {"name": "unpublish_story", "description": "Unpublish a story."},
    {"name": "get_story_versions", "description": "Get story versions."},
    {"name": "restore_story", "description": "Restore a story."},
    {"name": "validate_story_content", "description": "Validate story content."},
    {"name": "debug_story_access", "description": "Debug story access."},
    {"name": "bulk_publish_stories", "description": "Bulk publish stories."},
    {"name": "bulk_delete_stories", "description": "Bulk delete stories."},
    {"name": "bulk_update_stories", "description": "Bulk update stories."},
    {"name": "bulk_create_stories", "description": "Bulk create stories."},
    {"name": "get_unpublished_dependencies", "description": "Get unpublished dependencies."},
    {"name": "ai_translate_story", "description": "AI translate story."},
    {"name": "compare_story_versions", "description": "Compare story versions."},

    # tags.py
    {"name": "retrieve_multiple_tags", "description": "Retrieve multiple tags."},
    {"name": "create_tag", "description": "Create a tag."},
    {"name": "update_tag", "description": "Update a tag."},
    {"name": "delete_tag", "description": "Delete a tag."},
    {"name": "tag_bulk_association", "description": "Bulk tag association."},

    # tasks.py
    {"name": "retrieve_multiple_tasks", "description": "Retrieve multiple tasks."},
    {"name": "retrieve_single_task", "description": "Retrieve a single task."},
    {"name": "create_task", "description": "Create a task."},
    {"name": "update_task", "description": "Update a task."},
    {"name": "delete_task", "description": "Delete a task."},

    # webhooks.py
    {"name": "retrieve_multiple_webhooks", "description": "Retrieve multiple webhooks."},
    {"name": "retrieve_single_webhook", "description": "Retrieve a single webhook."},
    {"name": "add_webhook", "description": "Add a webhook."},
    {"name": "update_webhook", "description": "Update a webhook."},
    {"name": "delete_webhook", "description": "Delete a webhook."},

    # workflows.py
    {"name": "retrieve_multiple_workflows", "description": "Retrieve multiple workflows."},
    {"name": "retrieve_single_workflow", "description": "Retrieve a single workflow."},
    {"name": "create_workflow", "description": "Create a workflow."},
    {"name": "update_workflow", "description": "Update a workflow."},
    {"name": "duplicate_workflow", "description": "Duplicate a workflow."},
    {"name": "delete_workflow", "description": "Delete a workflow."},

    # workflow_stage.py
    {"name": "retrieve_multiple_workflow_stages", "description": "Retrieve multiple workflow stages."},
    {"name": "retrieve_single_workflow_stage", "description": "Retrieve a single workflow stage."},
    {"name": "create_workflow_stage", "description": "Create a workflow stage."},
    {"name": "update_workflow_stage", "description": "Update a workflow stage."},
    {"name": "delete_workflow_stage", "description": "Delete a workflow stage."},

    # workflow_stage_changes.py
    {"name": "retrieve_multiple_workflow_stage_changes", "description": "Retrieve multiple workflow stage changes."},
    {"name": "create_workflow_stage_change", "description": "Create a workflow stage change."},
]

# Register all modular tool implementations for Storyblok MCP
register_components(mcp, client)
register_components_folder(mcp, client)
register_stories(mcp, client)
register_assets(mcp, client)
register_tags(mcp, client)
register_meta(mcp, all_tools_info)
register_releases(mcp, client)
register_ping(mcp, client)
register_assets_folder(mcp, client)
register_datasources(mcp, client)
register_datasource_entries(mcp, client)
register_space(mcp, client)
register_space_roles(mcp, client)
register_presets(mcp, client)
register_access_tokens(mcp, client)
register_workflows(mcp, client)
register_workflow_stages(mcp, client)
register_workflow_stage_changes(mcp, client)
register_story_schedules(mcp, client)
register_branches(mcp, client)
register_branch_deployments(mcp, client)
register_discussions(mcp, client)
register_tasks(mcp, client)
register_webhooks(mcp, client)
register_internal_tags(mcp, client)
register_collaborators(mcp, client)
register_approvals(mcp, client)
register_activities(mcp, client)
register_extensions(mcp, client)
register_field_plugin_retrieval(mcp, client)

# Graceful exit on unexpected errors
def _exit(*args):
    """Exit the application gracefully on SIGINT or SIGTERM signals."""
    sys.exit(1)

signal.signal(signal.SIGINT, _exit)
signal.signal(signal.SIGTERM, _exit)

# Entry point: Run the MCP server using stdio transport
if __name__ == "__main__":
    mcp.run(transport='stdio')
