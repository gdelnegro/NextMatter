import re

import validators
import requests
from bs4 import BeautifulSoup

from validators import ValidationFailure

from backend.exceptions import InvalidURLException


class WebSiteInformation:
    url = ''
    information = None
    title = None
    headers = None
    links = {
        "internal": None,
        "external": None,
        "unreachable": None
    }
    has_login = None

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
            possible_urls = [{"url": url, "valid": False}]
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

    @staticmethod
    def _has_login_form(soup):
        # check if it has a password field in the web
        # or if there's a login/sign in button
        _soup = str(soup)

        sign_in_group = True if re.search(r'([sS]ign).([iI]n)', _soup) is not None else False
        login_group = True if re.search(r'([lL]og).([iI]n)', _soup) else False
        password_group = True if re.search(r'([pP]assword)', _soup) else False
        return any([sign_in_group, login_group, password_group])

    def _get_website_information(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            self.headers = soup.find_all(re.compile(r'^h[1-6]$'))
            self.title = soup.title.string
            self.has_login = WebSiteInformation._has_login_form(soup)

    def to_json(self):
        pass

    def from_json(self):
        pass