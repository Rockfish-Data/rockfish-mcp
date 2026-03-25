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


class TestDatasetQueryBookmarks:
    @pytest_asyncio.fixture(scope="class", autouse=True, loop_scope="session")
    async def seed_bookmark(self, dataset_id: str):
        """Store a query bookmark on the dataset via REST API before running tests."""
        client = server_module.rockfish_client
        assert client is not None, "rockfish_client not initialized"
        await client._request(
            "PUT",
            f"/dataset/{dataset_id}/query-bookmarks",
            json={"queries": [TEST_BOOKMARK]},
        )
        yield
        # Clean up
        await client._request(
            "PUT",
            f"/dataset/{dataset_id}/query-bookmarks",
            json={"queries": []},
        )

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

        assert isinstance(bookmarks, dict), "Response should be a dict"
        assert "queries" in bookmarks, "Response should contain 'queries' key"
        assert isinstance(bookmarks["queries"], list), "'queries' should be a list"
        assert len(bookmarks["queries"]) > 0, "Should have at least one bookmark"

        first = bookmarks["queries"][0]
        assert isinstance(first, dict), "Each bookmark should be a dict with 'query' and 'metadata'"
        assert first.get("query") == TEST_BOOKMARK["query"], (
            f"Expected query '{TEST_BOOKMARK['query']}', got: {first}"
        )
