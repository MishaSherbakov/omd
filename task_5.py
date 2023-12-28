import asyncio
from typing import Coroutine

async def limit_execution_time(coro: Coroutine, max_execution_time: float) -> None:
    try:
        await asyncio.wait_for(coro, timeout=max_execution_time)
    except asyncio.TimeoutError:
        pass

async def limit_execution_time_many(*coros: Coroutine, max_execution_time: float) -> None:
    tasks = [asyncio.create_task(coro) for coro in coros]

    try:
        await asyncio.wait(tasks, timeout=max_execution_time)
    except asyncio.TimeoutError:
        pass
    finally:
        for task in tasks:
            task.cancel()

        # Ожидаем завершения отмененных задач
        await asyncio.gather(*tasks, return_exceptions=True)
