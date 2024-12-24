import os
import random


def rand():
    path = os.getcwd()
    with open(path + "/bypass/proxies.txt") as proxy_file:
        proxies = proxy_file.read()

    proxies = proxies.split("\n")
    proxies.remove("")

    raw_proxy = proxies[random.randint(0, len(proxies) - 1)]
    if len(raw_proxy.split(":")) == 2:
        if raw_proxy.startswith("http://"):
            return raw_proxy
        return "http://" + raw_proxy
    else:
        raise Exception("unsupported proxy type")
