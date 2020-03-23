import logging
import requests
from backend.common import cache, CACHE_CONFIG


@cache.cached(timeout=CACHE_CONFIG["CACHE_DEFAULT_TIMEOUT"], key_prefix="website_html")
def get_website_html(url):
    logging.info("Getting website html for url {}".format(url))
    response = requests.get(url)
    if response.status_code == 200:
        logging.info("Returning html")
        return response.text
    else:
        raise ValueError("Response code different than 200. Received {}".format(response.status_code))


@cache.cached(timeout=120, key_prefix="urls_ping")
def ping_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False
