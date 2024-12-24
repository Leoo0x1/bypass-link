import aiohttp
import asyncio
import json
import uuid

from ..utils import proxy
from ..utils import tls


async def session(input_url):
    session_id = str(uuid.uuid4())
    proxyUrl = proxy.rand()

    requestPayload = {
        "catchPanics": False,
        "certificatePinningHosts": None,
        "customTlsClient": None,
        "transportOptions": None,
        "followRedirects": False,
        "forceHttp1": False,
        "headerOrder": None,
        "headers": None,
        "insecureSkipVerify": False,
        "isByteRequest": False,
        "isByteResponse": False,
        "isRotatingProxy": False,
        "proxyUrl": proxyUrl,
        "requestBody": None,
        "requestCookies": None,
        "requestHostOverride": None,
        "defaultHeaders": None,
        "connectHeaders": None,
        "requestMethod": "",
        "requestUrl": "",
        "disableIPV6": False,
        "disableIPV4": False,
        "localAddress": None,
        "sessionId": session_id,
        "serverNameOverwrite": "",
        "streamOutputBlockSize": None,
        "streamOutputEOFSymbol": None,
        "streamOutputPath": None,
        "timeoutMilliseconds": 0,
        "timeoutSeconds": 0,
        "tlsClientIdentifier": "chrome_124",
        "withDebug": False,
        "withDefaultCookieJar": False,
        "withoutCookieJar": False,
        "withRandomTLSExtensionOrder": False,
    }

    user_token = await get_user_token(requestPayload)

    access_token = await get_access_token(requestPayload, input_url, user_token)

    target_token = await get_target_token(
        requestPayload, input_url, user_token, access_token
    )

    await asyncio.sleep(10)

    result_url = await get_result_url(
        requestPayload, input_url, user_token, target_token
    )

    await tls.free_session(requestPayload)
    return result_url


async def bypass(cr, input_url):
    while True:
        try:
            result_url = await session(input_url)
            return result_url
        except Exception as e:
            print("[%d]:%s" % (cr, e))


async def get_user_token(requestPayload):
    requestPayload["headers"] = {
        "Host": "publisher.linkvertise.com",
        "sec-ch-ua": '"Not;A=Brand";v="24", "Chromium";v="124"',
        "accept": "application/json",
        "sec-ch-ua-platform": '"Windows"',
        "dnt": "1",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "content-type": "application/json",
        "origin": "https://linkvertise.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://linkvertise.com/",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=1, i",
    }
    requestPayload["headerOrder"] = None
    requestPayload["requestBody"] = ""
    requestPayload["requestMethod"] = "GET"
    requestPayload["requestUrl"] = "https://publisher.linkvertise.com/api/v1/account"
    requestPayload["timeoutSeconds"] = 30

    headers = {"x-api-key": "my-auth-key-1", "Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url="http://127.0.0.1:8090/api/forward",
            headers=headers,
            json=requestPayload,
        ) as res:
            tls_res = await res.json()

    if tls_res["status"] == 200:
        user_token = json.loads(tls_res["body"])["user_token"]
    else:
        await tls.free_session(requestPayload)
        raise ValueError("request error getting user_token [%d]" % tls_res["status"])

    return user_token


async def get_access_token(requestPayload, input_url, user_token):
    requestPayload["headers"] = {
        "Host": "publisher.linkvertise.com",
        "sec-ch-ua": '"Not;A=Brand";v="24", "Chromium";v="124"',
        "accept": "application/json",
        "sec-ch-ua-platform": '"Windows"',
        "dnt": "1",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "content-type": "application/json",
        "origin": "https://linkvertise.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://linkvertise.com/",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=1, i",
    }
    requestPayload["headerOrder"] = None
    user_id = input_url.split("/")[3]
    url_id = input_url.split("/")[4]
    req_body = {
        "operationName": "getDetailPageContent",
        "variables": {
            "linkIdentificationInput": {
                "userIdAndUrl": {"user_id": user_id, "url": url_id}
            },
            "origin": "sharing",
            "additional_data": {
                "taboola": {
                    "external_referrer": "",
                    "user_id": "fallbackUserId",
                    "url": input_url + "?o=sharing",
                    "test_group": "old",
                    "session_id": None,
                }
            },
        },
        "query": "mutation getDetailPageContent($linkIdentificationInput: PublicLinkIdentificationInput!, $origin: String, $additional_data: CustomAdOfferProviderAdditionalData!) {\n  getDetailPageContent(\n    linkIdentificationInput: $linkIdentificationInput\n    origin: $origin\n    additional_data: $additional_data\n  ) {\n    access_token\n    payload_bag {\n      taboola {\n        session_id\n        __typename\n      }\n      __typename\n    }\n    premium_subscription_active\n    link {\n      id\n      video_url\n      short_link_title\n      recently_edited\n      short_link_title\n      description\n      url\n      seo_faqs {\n        body\n        title\n        __typename\n      }\n      target_host\n      last_edit_at\n      link_images {\n        url\n        __typename\n      }\n      title\n      thumbnail_url\n      view_count\n      is_trending\n      recently_edited\n      seo_faqs {\n        title\n        body\n        __typename\n      }\n      percentage_rating\n      is_premium_only_link\n      publisher {\n        id\n        name\n        subscriber_count\n        __typename\n      }\n      positive_rating\n      negative_rating\n      already_rated_by_user\n      user_rating\n      __typename\n    }\n    linkCustomAdOffers {\n      title\n      call_to_action\n      description\n      countdown\n      completion_token\n      provider\n      provider_additional_payload {\n        taboola {\n          available_event_url\n          visible_event_url\n          __typename\n        }\n        __typename\n      }\n      media {\n        type\n        ... on UrlMediaResource {\n          content_type\n          resource_url\n          __typename\n        }\n        __typename\n      }\n      clickout_action {\n        type\n        ... on CustomAdOfferClickoutUrlAction {\n          type\n          clickout_url\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    link_recommendations {\n      short_link_title\n      target_host\n      id\n      url\n      publisher {\n        id\n        name\n        __typename\n      }\n      last_edit_at\n      link_images {\n        url\n        __typename\n      }\n      title\n      thumbnail_url\n      view_count\n      is_trending\n      recently_edited\n      percentage_rating\n      publisher {\n        name\n        __typename\n      }\n      __typename\n    }\n    target_access_information {\n      remaining_waiting_time\n      __typename\n    }\n    __typename\n  }\n}",
    }
    requestPayload["requestBody"] = json.dumps(req_body)
    requestPayload["requestMethod"] = "POST"
    requestPayload["requestUrl"] = (
        "https://publisher.linkvertise.com/graphql?X-Linkvertise-UT=" + user_token
    )
    requestPayload["timeoutSeconds"] = 30

    headers = {"x-api-key": "my-auth-key-1", "Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url="http://127.0.0.1:8090/api/forward",
            headers=headers,
            json=requestPayload,
        ) as res:
            tls_res = await res.json()

    if tls_res["status"] == 200:
        access_token = json.loads(tls_res["body"])["data"]["getDetailPageContent"][
            "access_token"
        ]
    else:
        await tls.free_session(requestPayload)
        raise ValueError("request error getting access_token [%d]" % tls_res["status"])

    return access_token


async def get_target_token(requestPayload, input_url, user_token, access_token):
    requestPayload["headers"] = {
        "Host": "publisher.linkvertise.com",
        "sec-ch-ua": '"Not;A=Brand";v="24", "Chromium";v="124"',
        "accept": "application/json",
        "sec-ch-ua-platform": '"Windows"',
        "dnt": "1",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "content-type": "application/json",
        "origin": "https://linkvertise.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://linkvertise.com/",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=1, i",
    }
    requestPayload["headerOrder"] = None
    user_id = input_url.split("/")[3]
    url_id = input_url.split("/")[4]
    req_body = {
        "operationName": "completeDetailPageContent",
        "variables": {
            "linkIdentificationInput": {
                "userIdAndUrl": {"user_id": user_id, "url": url_id}
            },
            "completeDetailPageContentInput": {"access_token": access_token},
        },
        "query": "mutation completeDetailPageContent($linkIdentificationInput: PublicLinkIdentificationInput!, $completeDetailPageContentInput: CompleteDetailPageContentInput!) {\n  completeDetailPageContent(\n    linkIdentificationInput: $linkIdentificationInput\n    completeDetailPageContentInput: $completeDetailPageContentInput\n  ) {\n    CUSTOM_AD_STEP\n    TARGET\n    additional_target_access_information {\n      remaining_waiting_time\n      can_not_access\n      should_show_ads\n      has_long_paywall_duration\n      __typename\n    }\n    __typename\n  }\n}",
    }
    requestPayload["requestBody"] = json.dumps(req_body)
    requestPayload["requestMethod"] = "POST"
    requestPayload["requestUrl"] = (
        "https://publisher.linkvertise.com/graphql?X-Linkvertise-UT=" + user_token
    )
    requestPayload["timeoutSeconds"] = 30

    headers = {"x-api-key": "my-auth-key-1", "Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url="http://127.0.0.1:8090/api/forward",
            headers=headers,
            json=requestPayload,
        ) as res:
            tls_res = await res.json()

    if tls_res["status"] == 200:
        target_token = json.loads(tls_res["body"])["data"]["completeDetailPageContent"][
            "TARGET"
        ]
        waiting_time = json.loads(tls_res["body"])["data"]["completeDetailPageContent"][
            "additional_target_access_information"
        ]["remaining_waiting_time"]

        if waiting_time > 10:
            await tls.free_session(requestPayload)
            raise ValueError("restart session [bad proxy]")

    else:
        await tls.free_session(requestPayload)
        raise ValueError("request error getting target_token [%d]" % tls_res["status"])

    return target_token


async def get_result_url(requestPayload, input_url, user_token, target_token):
    requestPayload["headers"] = {
        "Host": "publisher.linkvertise.com",
        "sec-ch-ua": '"Not;A=Brand";v="24", "Chromium";v="124"',
        "accept": "application/json",
        "sec-ch-ua-platform": '"Windows"',
        "dnt": "1",
        "sec-ch-ua-mobile": "?0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "content-type": "application/json",
        "origin": "https://linkvertise.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://linkvertise.com/",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=1, i",
    }
    requestPayload["headerOrder"] = None
    user_id = input_url.split("/")[3]
    url_id = input_url.split("/")[4]
    req_body = {
        "operationName": "getDetailPageTarget",
        "variables": {
            "linkIdentificationInput": {
                "userIdAndUrl": {"user_id": user_id, "url": url_id}
            },
            "token": target_token,
            "action_id": str(uuid.uuid4()) + str(uuid.uuid4()) + str(uuid.uuid4()),
        },
        "query": "mutation getDetailPageTarget($linkIdentificationInput: PublicLinkIdentificationInput!, $token: String!, $action_id: String) {\n  getDetailPageTarget(\n    linkIdentificationInput: $linkIdentificationInput\n    token: $token\n    action_id: $action_id\n  ) {\n    type\n    url\n    paste\n    short_link_title\n    __typename\n  }\n}",
    }
    requestPayload["requestBody"] = json.dumps(req_body)

    requestPayload["requestMethod"] = "POST"
    requestPayload["requestUrl"] = (
        "https://publisher.linkvertise.com/graphql?X-Linkvertise-UT=" + user_token
    )
    requestPayload["timeoutSeconds"] = 30

    headers = {"x-api-key": "my-auth-key-1", "Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url="http://127.0.0.1:8090/api/forward",
            headers=headers,
            json=requestPayload,
        ) as res:
            tls_res = await res.json()

    if tls_res["status"] == 200:
        result_url = json.loads(tls_res["body"])["data"]["getDetailPageTarget"]["url"]
    else:
        await tls.free_session(requestPayload)
        raise ValueError("request error getting result_url [%d]" % tls_res["status"])

    return result_url
