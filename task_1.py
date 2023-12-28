from asyncio import Task
from typing import Callable, Coroutine, Any


async def await_my_func(f: Callable[..., Coroutine] | Task | Coroutine) -> Any:
    # На вход приходит одна из стадий жизненного цикла корутины, необходимо вернуть результат
    # её выполнения.

    if isinstance(f, Callable):
        # Если передана обычная функция (Callable), вызываем её.
        return await f()

    elif isinstance(f, Task):
        # Если передан объект Task, ожидаем его выполнение.
        return await f

    elif isinstance(f, Coroutine):
        # Если передана уже запущенная корутина, ожидаем её завершение.
        return await f

    else:
        raise ValueError('invalid argument')
