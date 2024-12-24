import aiohttp


async def free_session(requestPayload):
    headers = {"x-api-key": "my-auth-key-1", "Content-Type": "application/json"}
    payload = {"sessionId": requestPayload["sessionId"]}
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url="http://127.0.0.1:8090/api/free-session",
            headers=headers,
            json=payload,
        ) as res:
            await res.json()
    # if res.json()["success"]:
    #     print("Session %s freed successfully" % (requestPayload["sessionId"]))


async def free_all_sessions():
    headers = {"x-api-key": "my-auth-key-1", "Content-Type": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url="http://127.0.0.1:8090/api/free-all",
            headers=headers,
        ) as res:
            await res.json()
    # if res.json()["success"]:
    #     print("All sessions freed successfully")
