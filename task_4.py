async def task_1(i: int, order: list[int]) -> None:
    if i == 0:
        return

    if i > 5:
        order.append(1)
        await task_2(i // 2, order)
    else:
        order.append(2)
        await task_2(i - 1, order)


async def task_2(i: int, order: list[int]) -> None:
    if i == 0:
        return

    if i % 2 == 0:
        order.append(3)
        await task_1(i // 2, order)
    else:
        order.append(4)
        await task_2(i - 1, order)


async def coroutines_execution_order(i: int = 42) -> int:
    order = []
    await task_1(i, order)
    return int(''.join(map(str, order)))
