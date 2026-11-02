"""Tests that agent cell replacements request JupyterLab's diff review UI."""

from unittest.mock import AsyncMock, patch

import pytest

from jupyter_ai_tools.toolkits.notebook import edit_cell


@pytest.mark.asyncio
async def test_rtc_free_edit_cell_requests_diff_review():
    command_result = {"success": True, "result": {"success": True}}
    with (
        patch(
            "jupyter_ai_tools.toolkits.notebook.rtc_available",
            return_value=False,
        ),
        patch(
            "jupyter_ai_tools.toolkits.notebook.run_lab_command",
            new_callable=AsyncMock,
            return_value=command_result,
        ) as run_lab_command,
    ):
        result = await edit_cell(
            "notebooks/example.ipynb",
            "cell-1",
            content="new_value = 42",
        )

    assert result == command_result
    run_lab_command.assert_awaited_once_with(
        "jupyterlab-ai-commands:set-cell-content",
        {
            "notebookPath": "notebooks/example.ipynb",
            "cellId": "cell-1",
            "content": "new_value = 42",
            "showDiff": True,
        },
    )
