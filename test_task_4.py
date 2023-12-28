import pytest

from task_4 import coroutines_execution_order


@pytest.mark.asyncio
async def test_coroutines_execution_order():
    assert await coroutines_execution_order() == 14314324