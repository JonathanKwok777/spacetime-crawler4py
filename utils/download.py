import requests
import cbor
import time

from utils.response import Response

def download(url, config, logger=None):
    host, port = config.cache_server
    try:
        resp = requests.get(
            f"http://{host}:{port}/",
            params=[("q", f"{url}"), ("u", f"{config.user_agent}")], timeout=(15, 50)) # connection time and read time

        if resp and resp.content:
            return Response(cbor.loads(resp.content))
    except requests.exceptions.Timeout:
        if logger:
            logger.warning(f"Timeout when downloading {url}")
        return Response({
            "error": "timeout", "status": 0, "url": url})
    except (EOFError, ValueError) as e:
        pass
    logger.error(f"Spacetime Response error {resp} with url {url}.")
    return Response({
        "error": f"Spacetime Response error {resp} with url {url}.",
        "status": resp.status_code,
        "url": url})
