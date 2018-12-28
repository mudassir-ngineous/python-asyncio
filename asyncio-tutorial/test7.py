import asyncio


# future <=> promise(in node)

async def my_task(seconds):
    """
     A task to do for a number of seconds
    """

    print('This task is taking {} seconds to complete'.format(
        seconds))

    await asyncio.sleep(seconds)

    return 'task finished'


loop = asyncio.get_event_loop()
try:
    print('task creation started')

    task_obj = loop.create_task(my_task(seconds=5))
    loop.run_until_complete(task_obj)
finally:
    loop.close()

print("The task's result was: {}".format(task_obj.result()))
