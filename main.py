import asyncio

from bypass.modules import linkvertise


async def main(input_url):
    coroutines = []

    # Create coroutines and tasks
    for cr in range(1):
        print("[%d]:Bypassing link" % cr)
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

            return result  # Exit after the first result is found


if __name__ == "__main__":
    input_url = input("Input the link you want to bypass: ")
    asyncio.run(main(input_url))
