"""
Unit tests for input-schema validation in the mcp 2.x call_tool callback.

mcp 2.x no longer validates arguments against a tool's inputSchema, so
server._on_call_tool does it before dispatching. No API access is needed:
invalid calls are rejected before any client is touched.
"""

import mcp.types as types
import pytest

import rockfish_mcp.server as server_module


def _params(name: str, arguments: dict) -> types.CallToolRequestParams:
    return types.CallToolRequestParams(name=name, arguments=arguments)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "tool, missing",
    [("get_database", "id"), ("create_database", "name")],
)
async def test_missing_required_argument_is_rejected(tool, missing):
    result = await server_module._on_call_tool(None, _params(tool, {}))

    assert result.is_error is True
    text = result.content[0].text
    assert f"Invalid arguments for {tool}" in text
    assert f"'{missing}' is a required property" in text


@pytest.mark.asyncio
async def test_wrong_argument_type_is_rejected():
    result = await server_module._on_call_tool(
        None, _params("get_database", {"id": 123})
    )

    assert result.is_error is True
    assert "Invalid arguments for get_database" in result.content[0].text
