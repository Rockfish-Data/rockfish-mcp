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

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *rockfish-mcp*.

### Using pip

```bash
pip install rockfish-mcp
```

After installation, you can run it as a script using:

```bash
python -m rockfish_mcp.server
```

### From source

```bash
git clone https://github.com/Rockfish-Data/rockfish-mcp.git
cd rockfish-mcp
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
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

<details>
<summary>Using uvx</summary>

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
<summary>Using pip installation</summary>

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

### Usage with VS Code

For manual installation, add the following JSON block to your User Settings (JSON) file in VS Code. You can do this by pressing `Ctrl + Shift + P` and typing `Preferences: Open User Settings (JSON)`.

Optionally, you can add it to a file called `.vscode/mcp.json` in your workspace.

> Note that the `mcp` key is needed when using the `mcp.json` file.

<details>
<summary>Using uvx</summary>

```json
{
  "mcp": {
    "servers": {
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
}
```
</details>

<details>
<summary>Using pip installation</summary>

```json
{
  "mcp": {
    "servers": {
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
}
```
</details>

## Debugging

You can use the MCP inspector to debug the server. For uvx installations:

```bash
npx @modelcontextprotocol/inspector uvx rockfish-mcp
```

Or if you've installed the package in a specific directory or are developing on it:

```bash
cd path/to/rockfish-mcp
npx @modelcontextprotocol/inspector .venv/bin/python -m rockfish_mcp.server
```

## Development

### Setup

Install with dev dependencies:

```bash
pip install -e ".[dev]"
```

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
