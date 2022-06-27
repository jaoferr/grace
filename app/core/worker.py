from typing import Callable

async def add_task(
    *,
    task: Callable,
    **kwargs
) -> bool:
    this_is_a_task = False

    return this_is_a_task
