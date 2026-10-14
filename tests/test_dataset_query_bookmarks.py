"""
Integration test for get_dataset_query_bookmarks tool.

Seeds a query bookmark on the test dataset via the REST API, then verifies
the tool retrieves it. Confirms whether the SDK correctly handles the
API's SingleQueryBookmark structure (query + metadata).
"""

import pytest
import pytest_asyncio
import rockfish_mcp.server as server_module
from mcp import types

from rockfish_mcp.server import handle_call_tool

from .test_list_resources import parse_response_text

TEST_BOOKMARK = {
    "query": "SELECT * FROM dataset LIMIT 10",
    "metadata": {
        "name": "test bookmark",
        "labels": {},
    },
}


@pytest_asyncio.fixture(scope="class", loop_scope="session")
async def seed_bookmark(dataset_id: str):
    """Store a query bookmark on the dataset via REST API before running tests."""
    client = server_module.rockfish_client
    assert client is not None, "rockfish_client not initialized"
    endpoint = f"/dataset/{dataset_id}/query-bookmarks"
    original = (await client._request("GET", endpoint)).get("queries", [])
    await client._request(
        "PUT",
        endpoint,
        json={"queries": [TEST_BOOKMARK]},
    )
    yield
    # Restore whatever bookmarks the dataset had before the test
    await client._request("PUT", endpoint, json={"queries": original})


@pytest.mark.usefixtures("seed_bookmark")
class TestDatasetQueryBookmarks:
    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_dataset_query_bookmarks(self, dataset_id: str):
        """Retrieve query bookmarks for a dataset."""
        result = await handle_call_tool(
            "get_dataset_query_bookmarks", {"dataset_id": dataset_id}
        )

        assert result is not None, "Result should not be None"
        assert len(result) > 0, "Result should contain content"

        first_content = result[0]
        assert isinstance(first_content, types.TextContent), "Result should be TextContent"

        bookmarks = parse_response_text(first_content.text, "get_dataset_query_bookmarks")

        assert isinstance(bookmarks, list), "Response should be a list of query strings"
        assert len(bookmarks) > 0, "Should have at least one bookmark"

        assert isinstance(bookmarks[0], str), "Each bookmark should be a query string"
        assert bookmarks[0] == TEST_BOOKMARK["query"], (
            f"Expected query '{TEST_BOOKMARK['query']}', got: {bookmarks[0]}"
        )
