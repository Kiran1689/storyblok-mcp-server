# Storyblok MCP Server

A modular, extensible Python server for managing Storyblok spaces, stories, components, assets, workflows, and more via the Model Context Protocol (MCP).

---

## 🚀 Features
- **Full Storyblok Management**: CRUD for stories, components, assets, datasources, tags, releases, workflows, and more.
- **Modular Tooling**: Each Storyblok resource is managed by its own tool module for easy extension and maintenance.
- **Meta Tool**: Discover all available tools and their descriptions at runtime.
- **Async & Fast**: Built on `httpx` and `FastMCP` for high performance.
- **Environment-based Config**: Securely manage tokens and space IDs via `.env`.
- **Bulk Operations**: Efficiently update, delete, or publish multiple resources at once.
- **Self-Documenting**: The meta tool lists all available endpoints and their purposes.

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

## ⚡️ Quickstart

1. **Clone the repo**
   ```sh
   git clone <your-repo-url>
   cd storyblok_mcp_server
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
        "storyblok-mcp-server": {
            "command": "uv",
            "args": [
                "run",
                "--with",
                "mcp",
                "mcp",
                "run",
                "C:\\path\\to\\storyblok_mcp_server\\server.py"
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

5. **Run and Test Locally**
   - You can also run and test the server locally using MCP Inspector:
   ```sh
   mcp run server.py
   ```

---

## 🛠️ Tooling & Usage

- Each tool (e.g., `stories`, `components`, `assets`) exposes a set of async functions for CRUD and bulk operations.
- The meta tool (`list_tools`) lets you discover all available tools and their descriptions, including the total count.
- All API errors are handled gracefully and return helpful messages.

### Example: Listing All Tools

You can call the meta tool to get a list of all available tools and their descriptions:
```json
{
  "content": [
    {
      "type": "text",
      "text": "Available tools (total: 99):\nfetch_stories: Fetch stories.\ncreate_story: Create a story.\n..."
    }
  ],
  "total_tools": 99
}
```

---

## 🧑‍💻 Contributing

We welcome contributions! To get started:

1. **Fork the repo** and create your branch from `main`.
2. **Add or improve a tool** in the `tools/` directory.
3. **Write clear docstrings** and keep code modular.
4. **Add or update tests** if possible.
5. **Open a pull request** with a clear description of your changes.

### Coding Guidelines
- Use type hints and docstrings for all functions and classes.
- Keep each tool focused on a single Storyblok resource.
- Handle API errors gracefully and return informative messages.
- Keep the `.env` file out of version control.

---

## 🤝 Credits
- Built with [Storyblok](https://www.storyblok.com/) and [FastMCP](https://github.com/modelcontext/fastmcp).
- Async HTTP by [httpx](https://www.python-httpx.org/).
- Environment management by [python-dotenv](https://github.com/theskumar/python-dotenv).

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 💬 Questions & Support

- For issues, open a GitHub issue.
- For feature requests, open a discussion or PR.
- For Storyblok API docs, see [Storyblok API Reference](https://www.storyblok.com/docs/api/management).

---

> _Happy building with Storyblok MCP!_
