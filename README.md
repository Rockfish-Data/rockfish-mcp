# Rockfish MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/Rockfish-Data/rockfish-mcp/blob/main/LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Model Context Protocol server that provides tools to interact with the [Rockfish AI](https://rockfish.ai) platform for synthetic data generation, dataset management, and ML workflow orchestration.

### Available Tools

**Rockfish API** — databases, worker sets, workflows, models, projects, datasets, organizations (22+ tools)

**SDK (Synthetic Data Generation)**
- `obtain_train_config` — generate training configuration with automatic column type detection
- `update_train_config` — modify training hyperparameters or field classifications
- `start_training_workflow` — start TabGAN training workflow
- `get_workflow_logs` — stream workflow logs with configurable level and timeout
- `get_trained_model_id` — extract trained model ID from completed workflow
- `start_generation_workflow` — start generation workflow from trained model
- `obtain_synthetic_dataset_id` — extract generated dataset ID from completed workflow
- `plot_distribution` — generate distribution plots comparing real and synthetic data
- `get_marginal_distribution_score` — calculate similarity score between real and synthetic data

**Manta (Analytics & Scenarios)** — requires `MANTA_API_URL`
- `discover_schema` — discover dataset schema
- `generate_test_suite` — generate test suites
- `execute_query` / `execute_nl_query` — run SQL or natural language queries
- `inject_scenario` — inject test scenarios into datasets

## Installation

`rockfish-mcp` is not currently published to PyPI, so install it from source (below) and run it
with `uv run --directory /path/to/rockfish-mcp rockfish-mcp`. The `uvx rockfish-mcp` and
`pip install rockfish-mcp` forms only work once the package is published to an index.

### From source (recommended)

```bash
git clone https://github.com/Rockfish-Data/rockfish-mcp.git
cd rockfish-mcp
```

2. Install dependencies (exact versions from `uv.lock`, including dev tools):

```bash
uv sync
source .venv/bin/activate  # optional; or prefix commands with `uv run`
```

For a runtime-only install (no dev tools), use `uv sync --no-dev`.

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Rockfish API key
```

## Configuration

Create a `.env` file with your Rockfish API credentials:

```env
ROCKFISH_API_KEY=your_api_key_here
ROCKFISH_API_URL=https://api.rockfish.ai
```

Optional settings:

```env
ROCKFISH_ORGANIZATION_ID=your_organization_id_here
ROCKFISH_PROJECT_ID=your_project_id_here
MANTA_API_URL=https://manta.rockfish.ai
```

### Usage with Claude Desktop

Add to your `claude_desktop_config.json`:

<details open>
<summary>From a source checkout (uv run)</summary>

`rockfish-mcp` is not published to PyPI, so `uvx rockfish-mcp` fails with
`rockfish-mcp was not found in the package registry`. Run it from a clone instead. Use
`uv run --directory` rather than `uvx --from`, so the locked dependencies and the Rockfish SDK
`find-links` index from `pyproject.toml` are honored. Use the absolute path to `uv`
(`which uv`), since Claude Desktop does not inherit your shell `PATH`.

```json
{
  "mcpServers": {
    "rockfish": {
      "command": "/opt/homebrew/bin/uv",
      "args": ["run", "--directory", "/path/to/rockfish-mcp", "rockfish-mcp"],
      "env": {
        "ROCKFISH_API_KEY": "your_api_key_here",
        "ROCKFISH_API_URL": "https://api.rockfish.ai"
      }
    }
  }
}
```

The first launch builds the environment and can take ~30 seconds; later launches are fast.
</details>

<details>
<summary>Using uvx (requires a published package)</summary>

```json
{
  "mcpServers": {
    "rockfish": {
      "command": "uvx",
      "args": ["rockfish-mcp"],
      "env": {
        "ROCKFISH_API_KEY": "your_api_key_here",
        "ROCKFISH_API_URL": "https://api.rockfish.ai"
      }
    }
  }
}
```
</details>

<details>
<summary>Using pip installation (requires a published package)</summary>

```json
{
  "mcpServers": {
    "rockfish": {
      "command": "python",
      "args": ["-m", "rockfish_mcp.server"],
      "env": {
        "ROCKFISH_API_KEY": "your_api_key_here",
        "ROCKFISH_API_URL": "https://api.rockfish.ai"
      }
    }
  }
}
```
</details>

<details>
<summary>Using docker</summary>

```json
{
  "mcpServers": {
    "rockfish": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "ROCKFISH_API_KEY", "-e", "ROCKFISH_API_URL", "rockfish-mcp"],
      "env": {
        "ROCKFISH_API_KEY": "your_api_key_here",
        "ROCKFISH_API_URL": "https://api.rockfish.ai"
      }
    }
  }
}
```
</details>

## Debugging

You can use the MCP inspector to debug the server from a source checkout:

```bash
npx @modelcontextprotocol/inspector uv run --directory path/to/rockfish-mcp rockfish-mcp
```

Or run the venv's Python directly (after `uv sync`):

```bash
cd path/to/rockfish-mcp
npx @modelcontextprotocol/inspector .venv/bin/python -m rockfish_mcp.server
```

If the server fails to start in Claude Desktop, check `~/Library/Logs/Claude/mcp-server-rockfish.log`.

## Development

### Setup

Install with dev dependencies (the default for `uv sync`):

```bash
uv sync
```

Run tools with `uv run` (for example `uv run pytest`) or activate `.venv` first.

### Code Formatting

```bash
isort src/rockfish_mcp/ && black src/rockfish_mcp/
```

### Running Tests

**Unit tests** (no credentials required):

```bash
pytest tests/test_manta_client.py tests/test_manta_tools.py
```

**Integration tests** (requires `.env` with real credentials):

```bash
pytest tests/
pytest --env=.env.prod.local --html=report.html --self-contained-html
```

## Contributing

We encourage contributions to help expand and improve rockfish-mcp. Whether you want to add new tools, enhance existing functionality, or improve documentation, your input is valuable.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Format your code with `isort` and `black`
5. Add tests if applicable
6. Submit a pull request

For examples of other MCP servers and implementation patterns, see:
https://github.com/modelcontextprotocol/servers

## License

rockfish-mcp is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the [LICENSE](LICENSE) file in the project repository.
