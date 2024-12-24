import asyncio

from bypass.modules import linkvertise


async def main():
    input_url = "https://direct-link.net/382645/content8987"
    coroutines = []

    # Create coroutines and tasks
    for cr in range(100):
        print("[%d]: Bypassing link" % cr)
        task = asyncio.create_task(linkvertise.bypass(cr, input_url))
        coroutines.append(task)

    # Process results as soon as any coroutine finishes
    for task in asyncio.as_completed(coroutines):
        result = await task
        if result != None:
            print(result)

            # Cancel remaining tasks once one result is obtained
            for remaining_task in coroutines:
                if not remaining_task.done():
                    remaining_task.cancel()

            break  # Exit after the first result is found


if __name__ == "__main__":
    asyncio.run(main())
