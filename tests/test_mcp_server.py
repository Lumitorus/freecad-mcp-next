from __future__ import annotations

import asyncio

import pytest

from freecad_mcp.server import _validate_host, mcp


def test_server_registers_expected_tools() -> None:
    tools = asyncio.run(mcp.list_tools())

    assert len(tools) == 14
    assert {tool.name for tool in tools} >= {
        "create_document",
        "create_object",
        "execute_code",
        "get_view",
        "list_documents",
    }


def test_host_validation() -> None:
    assert _validate_host("localhost") == "localhost"
    assert _validate_host("127.0.0.1") == "127.0.0.1"

    with pytest.raises(Exception, match="Invalid host"):
        _validate_host("bad host!")
