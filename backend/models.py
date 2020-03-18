import validators
import requests
from validators import ValidationFailure

from backend.exceptions import InvalidURLException


class WebSiteInformation:
    url = ''

    def __init__(self, url):
        # Adding http and https to the url before validating since this is something that users tend to forget
        # instead of forcing the user to fix this simple mistake and re-executing the request, it is best to just
        # try with http and https
        if 'http' not in url:
            possible_urls = [
                {"url": "http://{}".format(url), "valid": False},
                {"url": "http://{}".format(url), "valid": False}
            ]
        else:
            possible_urls = [{"url": "http://{}".format(url), "valid": False}]
        for _index, _url in enumerate(possible_urls):
            _url["valid"] = WebSiteInformation.is_valid_url(_url["url"])
            possible_urls[_index] = _url

        valid_urls = [_url["url"] for _url in possible_urls if _url["valid"] is True]
        if len(valid_urls):
            self.url = valid_urls[0]
        else:
            raise InvalidURLException

    @staticmethod
    def is_valid_url(url):
        validation_result = validators.url(url)
        if validation_result is True:
            return True
        else:
            return False

    @staticmethod
    def ping_url(url):
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False

    def _get_website_information(self, url):
        pass