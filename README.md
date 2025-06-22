<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/banner_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="./assets/banner_white.png">
  <img align="center" alt="banner" src="./assets/banner_white.png">
</picture>

<div align="center">
   
# Storyblok MCP Server 🚀

The Storyblok MCP ([Model Context Protocol](https://modelcontextprotocol.io/introduction)) server enables your AI assistants to directly access and manage your Storyblok spaces, stories, components, assets, workflows, and more.

<a href="https://www.storyblok.com/docs/api/management/getting-started" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/documentation-storyblok-blue" alt="documentation" /></a>
<a href="https://reactjs.org/"><img alt="Made With React" src="https://img.shields.io/badge/made%20with-python-yellow?style=flat" /></a>
<a href="https://github.com/Kiran1689" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/built_with-love-red" alt="built with love badge" /></a>
<img src="https://img.shields.io/badge/built_for-developers-dcd4fc" alt="built for developers badge" /></a>
<img src="https://img.shields.io/badge/built_for-marketers-bce4fb" alt="built for marketers badge" /></a>


</div>

## What Does It Do?

With the Storyblok MCP Server, your AI assistant can:
- **Create** - Create new stories, components, assets, datasources, tags, releases, workflows, and more.
- **Read** - Read all your stories, components, assets, datasources, tags, releases, workflows, and more.
- **Update** - Update existing/new stories, components, assets, datasources, tags, releases, workflows, and more.
- **Delete** - Delete specific/all your stories, components, assets, datasources, tags, releases, workflows, and more.

---

## 🚀 Features
- **Full Storyblok Management**: CRUD for stories, components, assets, datasources, tags, releases, workflows, and more.(Covered everything)
- **Modular Tooling**: Each Storyblok resource is managed by its own tool module for easy extension and maintenance.
- **Meta Tool**: Discover all available tools and their descriptions at runtime.
- **Async & Fast**: Built on `httpx` and `FastMCP` for high performance.
- **Environment-based Config**: Securely manage tokens and space IDs via `.env`.
- **Bulk Operations**: Efficiently update, delete, or publish multiple resources at once.

---

## 📦 Project Structure

```
├── config.py              # Loads and validates environment config
├── server.py              # Main entrypoint, registers all tools
├── tools/                 # All modular tool implementations
│   ├── components.py      # Component CRUD and usage
│   ├── stories.py         # Story CRUD, bulk ops, validation
│   ├── ...                # (assets, tags, releases, workflows, etc.)
│   └── meta.py            # Meta tool for tool discovery
├── utils/
│   └── api.py             # API helpers, error handling, URL builders
├── .env                   # Your Storyblok tokens and space ID
├── pyproject.toml         # Python dependencies
└── README.md              # This file
```

---

## 🚀 API Coverage

| Resource                   | Description                                      |
|----------------------------|--------------------------------------------------|
| Access Tokens              | Manage access tokens for Storyblok API           |
| Activities                 | Manage or retrieve activity logs                 |
| Approvals                  | Manage approval workflows                        |
| Assets                     | Manage assets (upload, update, delete, list)     |
| Assets Folder              | Manage asset folders                             |
| Branch Deployments         | Manage branch deployments                        |
| Collaborators              | Manage collaborators in a space                  |
| Components                 | Manage Storyblok components (CRUD, schema, etc.) |
| Components Folder          | Manage folders for components                    |
| Datasource Entries         | Manage entries in data sources                   |
| Data Sources               | Manage data sources (CRUD, entries)              |
| Discussions                | Manage discussions and comments                  |
| Extensions                 | Manage Storyblok extensions                      |
| Field Plugins              | Manage custom field plugins                      |
| Internal Tags              | Manage internal tags for assets/stories          |
| Meta                       | Meta tool: discover all available tools          |
| Ping                       | Health check and server status                   |
| Pipelines                  | Manage pipelines for content delivery            |
| Presets                    | Manage field presets for components              |
| Releases                   | Manage releases (create, update, publish)        |
| Scheduling Stories         | Schedule stories for publishing                  |
| Space                      | Manage Storyblok space settings and info         |
| Space Roles                | Manage roles and permissions in a space          |
| Stories                    | Manage stories (CRUD, bulk ops, validation)      |
| Tags                       | Manage tags (CRUD, bulk association)             |
| Tasks                      | Manage tasks (CRUD, webhooks, automation)        |
| Webhooks                   | Manage webhooks (CRUD, trigger)                  |
| Workflows                  | Manage workflows and workflow stages             |
| Workflow Stage             | Manage individual workflow stages                |
| Workflow Stage Changes     | Track and manage workflow stage changes          |

---

## 🪄 Available Tools

### Access Tokens
<details>
<summary>Manage access tokens for Storyblok API</summary>
   
- `retrieve_multiple_access_tokens`: List all access tokens
- `create_access_token`: Create a new access token
- `update_access_token`: Update an existing access token
- `delete_access_token`: Delete an access token
</details>

### Activities
<details>
<summary>Manage or retrieve activity logs</summary>
   
- `retrieve_multiple_activities`: List activity logs
</details>

### Approvals
<details>
<summary>Manage approval workflows</summary>
   
- `retrieve_multiple_approvals`: List approvals
- `create_approval`: Create a new approval
- `update_approval`: Update an approval
- `delete_approval`: Delete an approval
</details>

### Assets
<details>
<summary>Manage assets (upload, update, delete, list)</summary>
   
- `fetch_assets`: List assets with filtering
- `get_asset`: Get a specific asset by ID
- `delete_asset`: Delete an asset
- `update_asset`: Update an asset
- `delete_multiple_assets`: Delete multiple assets
- `bulk_move_assets`: Move multiple assets
- `bulk_restore_assets`: Restore multiple assets
- `init_asset_upload`: Initialize asset upload
- `complete_asset_upload`: Complete asset upload
</details>

### Assets Folder
<details>
<summary>Manage asset folders</summary>
   
- `retrieve_multiple_asset_folders`: List asset folders
- `create_asset_folder`: Create a new asset folder
- `update_asset_folder`: Update an asset folder
- `delete_asset_folder`: Delete an asset folder
</details>

### Branch Deployments
<details>
<summary>Manage branch deployments</summary>
   
- `retrieve_multiple_branch_deployments`: List branch deployments
- `create_branch_deployment`: Create a new branch deployment
- `update_branch_deployment`: Update a branch deployment
- `delete_branch_deployment`: Delete a branch deployment
</details>

### Collaborators
<details>
<summary>Manage collaborators in a space</summary>
   
- `retrieve_multiple_collaborators`: List collaborators
- `add_collaborator`: Add a collaborator
- `update_collaborator`: Update a collaborator
- `remove_collaborator`: Remove a collaborator
</details>

### Components
<details>
<summary>Manage Storyblok components (CRUD, schema, etc.)</summary>
   
- `fetch_components`: List components with filtering
- `get_component`: Get a specific component by ID
- `create_component`: Create a new component
- `update_component`: Update an existing component
- `delete_component`: Delete a component
- `get_component_usage`: Find stories using a component
- `retrieve_component_versions`: List versions of a component
- `retrieve_single_component_version`: Get a specific component version
- `restore_component_version`: Restore a component to a previous version
</details>

### Components Folder
<details>
<summary>Manage folders for components</summary>
  
- `retrieve_multiple_component_folders`: List component folders
- `create_component_folder`: Create a new component folder
- `update_component_folder`: Update a component folder
- `delete_component_folder`: Delete a component folder
</details>

### Datasource Entries
<details>
<summary>Manage entries in data sources</summary>
   
- `retrieve_multiple_datasource_entries`: List datasource entries
- `create_datasource_entry`: Create a new datasource entry
- `update_datasource_entry`: Update a datasource entry
- `delete_datasource_entry`: Delete a datasource entry
</details>

### Data Sources
<details>
<summary>Manage data sources (CRUD, entries)</summary>
   
- `retrieve_multiple_data_sources`: List data sources
- `create_data_source`: Create a new data source
- `update_data_source`: Update a data source
- `delete_data_source`: Delete a data source
</details>

### Discussions
<details>
<summary>Manage discussions and comments</summary>
   
- `retrieve_multiple_discussions`: List discussions
- `retrieve_specific_discussion`: Get a specific discussion
- `retrieve_idea_discussions_comments`: List idea discussion comments
- `create_discussion`: Create a new discussion
- `retrieve_my_discussions`: List my discussions
</details>

### Extensions
<details>
<summary>Manage Storyblok extensions</summary>
   
- `retrieve_all_extensions`: List all extensions
- `retrieve_extension`: Get a specific extension
- `create_extension`: Create a new extension
- `update_extension`: Update an extension
- `delete_extension`: Delete an extension
- `retrieve_extension_settings`: Get extension settings
- `retrieve_all_extension_settings`: List all extension settings
</details>

### Field Plugins
<details>
<summary>Manage custom field plugins</summary>
   
- `retrieve_field_plugins`: List field plugins
- `retrieve_field_plugin`: Get a specific field plugin
- `create_field_plugin`: Create a new field plugin
- `update_field_plugin`: Update a field plugin
- `delete_field_plugin`: Delete a field plugin
</details>

### Internal Tags
<details>
<summary>Manage internal tags for assets/stories</summary>
   
- `retrieve_multiple_internal_tags`: List internal tags
- `create_internal_tag`: Create a new internal tag
- `update_internal_tag`: Update an internal tag
- `delete_internal_tag`: Delete an internal tag
</details>

### Meta
<details>
<summary>Meta tool: discover all available tools</summary>
   
- `list_tools`: List all available tools
</details>

### Ping
<details>
<summary>Health check and server status</summary>
   
- `ping`: Check server health
</details>

### Pipelines
<details>
<summary>Manage pipelines for content delivery</summary>
   
- `retrieve_multiple_branches`: List branches
- `retrieve_single_branch`: Get a specific branch
- `create_branch`: Create a new branch
- `update_branch`: Update a branch
- `delete_branch`: Delete a branch
</details>

### Presets
<details>
<summary>Manage field presets for components</summary>
   
- `retrieve_multiple_presets`: List field presets
- `retrieve_single_preset`: Get a specific preset
- `create_preset`: Create a new preset
- `update_preset`: Update a preset
- `delete_preset`: Delete a preset
</details>

### Releases
<details>
<summary>Manage releases (create, update, publish)</summary>
   
- `retrieve_multiple_releases`: List releases
- `retrieve_single_release`: Get a specific release
- `create_release`: Create a new release
- `update_release`: Update a release
- `delete_release`: Delete a release
</details>

### Scheduling Stories
<details>
<summary>Schedule stories for publishing</summary>
   
- `retrieve_multiple_story_schedules`: List story schedules
- `retrieve_one_story_schedule`: Get a specific story schedule
- `create_story_schedule`: Create a new story schedule
- `update_story_schedule`: Update a story schedule
- `delete_story_schedule`: Delete a story schedule
</details>

### Space
<details>
<summary>Manage Storyblok space settings and info</summary>
   
- `fetch_spaces`: List spaces
- `get_space`: Get a specific space
- `create_space`: Create a new space
- `update_space`: Update a space
- `duplicate_space`: Duplicate a space
- `backup_space`: Backup a space
- `delete_space`: Delete a space
</details>

### Space Roles
<details>
<summary>Manage roles and permissions in a space</summary>
   
- `fetch_space_roles`: List space roles
- `get_space_role`: Get a specific space role
- `create_space_role`: Create a new space role
- `update_space_role`: Update a space role
- `delete_space_role`: Delete a space role
</details>

### Stories
<details>
<summary>Manage stories (CRUD, bulk ops, validation)</summary>
   
- `fetch_stories`: List stories with filtering
- `get_story`: Get a specific story by ID
- `create_story`: Create a new story
- `update_story`: Update an existing story
- `delete_story`: Delete a story
- `publish_story`: Publish a story
- `unpublish_story`: Unpublish a story
- `get_story_versions`: List versions of a story
- `restore_story`: Restore a story to a previous version
- `validate_story_content`: Validate story content
- `debug_story_access`: Debug access for a story
- `bulk_publish_stories`: Publish multiple stories
- `bulk_delete_stories`: Delete multiple stories
- `bulk_update_stories`: Update multiple stories
- `bulk_create_stories`: Create multiple stories
- `get_unpublished_dependencies`: List unpublished dependencies
- `ai_translate_story`: AI-powered translation for a story
- `compare_story_versions`: Compare two versions of a story
</details>

### Tags
<details>
<summary>Manage tags (CRUD, bulk association)</summary>
   
- `retrieve_multiple_tags`: List tags
- `create_tag`: Create a new tag
- `update_tag`: Update a tag
- `delete_tag`: Delete a tag
- `tag_bulk_association`: Add tags to multiple stories
</details>

### Tasks
<details>
<summary>Manage tasks (CRUD, webhooks, automation)</summary>
   
- `retrieve_multiple_tasks`: List tasks
- `retrieve_single_task`: Get a specific task
- `create_task`: Create a new task
- `update_task`: Update a task
- `delete_task`: Delete a task
</details>

### Webhooks
<details>
<summary>Manage webhooks (CRUD, trigger)</summary>
  
- `retrieve_multiple_webhooks`: List webhooks
- `retrieve_single_webhook`: Get a specific webhook
- `add_webhook`: Add a new webhook
- `update_webhook`: Update a webhook
- `delete_webhook`: Delete a webhook
</details>

### Workflows
<details>
<summary>Manage workflows and workflow stages</summary>
   
- `retrieve_multiple_workflows`: List workflows
- `retrieve_single_workflow`: Get a specific workflow
- `create_workflow`: Create a new workflow
- `update_workflow`: Update a workflow
- `duplicate_workflow`: Duplicate a workflow
- `delete_workflow`: Delete a workflow
</details>

### Workflow Stage
<details>
<summary>Manage individual workflow stages</summary>
   
- `retrieve_multiple_workflow_stages`: List workflow stages
- `retrieve_single_workflow_stage`: Get a specific workflow stage
- `create_workflow_stage`: Create a new workflow stage
- `update_workflow_stage`: Update a workflow stage
- `delete_workflow_stage`: Delete a workflow stage
</details>

### Workflow Stage Changes
<details>
<summary>Track and manage workflow stage changes</summary>
   
- `retrieve_multiple_workflow_stage_changes`: List workflow stage changes
- `create_workflow_stage_change`: Create a workflow stage change
</details>


## ⚡️ Quickstart

1. **Clone the repo**
   ```sh
   git clone <your-repo-url>
   cd storyblok-mcp-server
   ```
2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure your environment**
   - Copy `.env.example` to `.env` and fill in your Storyblok credentials:
     ```
     STORYBLOK_SPACE_ID=your_space_id
     STORYBLOK_MANAGEMENT_TOKEN=your_management_token
     STORYBLOK_DEFAULT_PUBLIC_TOKEN=your_public_token
     ```

4. **MCP Client Configuration**
   - To use this server with Claude or any MCP client, copy the following into your `claude_desktop_config.json`:

```json
{
    "mcpServers": {
        "storyblok": {
            "command": "uv",
            "args": [
                "run",
                "--with",
                "mcp",
                "mcp",
                "run",
                "C:\\path\\to\\storyblok-mcp-server\\server.py"
            ],
            "env": {
                "STORYBLOK_SPACE_ID": "your_space_id",
                "STORYBLOK_MANAGEMENT_TOKEN": "your_management_token",
                "STORYBLOK_DEFAULT_PUBLIC_TOKEN": "your_public_token"
            }
        }
    }
}
```

- Paste this config into your Claude or MCP client to connect instantly.

> [!NOTE]
> Make sure you have installed `uv` on your system

Restart your Claude Desktop and chek the tools. It will show total number tools available if you connected successfully.

![Claude Desktop](./assets/claude.png)

5. **Run and Test Locally**
   - You can also run and test the server locally using MCP Inspector:
   ```sh
   mcp run server.py
   ```

  ![mcp inspector](./assets/inspector.png)

## Example Questions

> [!TIP]
> Here are some natural language queries you can try with your MCP Client.

* "Show me all stories from storyblok"
* "Give me details about Home story"
* "Create a new story with any content"
* "Publish Home story"

---

## 🧑‍💻 Contributing

We welcome contributions! To get started:

1. **Fork the repo** and create your branch from `master`.
2. **Add or improve a tool** in the `tools/` directory.
3. **Write clear docstrings** and keep code modular.
4. **Use MCP Inspector** for debugging
5. **Open a pull request** with a clear description of your changes.

### Coding Guidelines
- Use type hints and docstrings for all functions and classes.
- Keep each tool focused on a single Storyblok resource.
- Handle API errors gracefully and return informative messages.
- Keep the `.env` file out of version control.

---

## 🤝 Credits
Built with [Storyblok](https://www.storyblok.com/) and [FastMCP](https://gofastmcp.com/getting-started/welcome).

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 💬 Questions & Support

- For issues, open a GitHub issue.
- For feature requests, open a discussion or PR.
- For Storyblok API docs, see [Storyblok API Reference](https://www.storyblok.com/docs/api/management).

---

_Built with 💙 by [Kiran](https://github.com/Kiran1689)_

