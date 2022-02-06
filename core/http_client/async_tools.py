import asyncio


async def gather_with_concurrency(max_tasks, tasks):
    semaphore = asyncio.Semaphore(max_tasks)

    async def sem_task(task):
        async with semaphore:
            return await task

    return await asyncio.gather(*(sem_task(task) for task in tasks))
