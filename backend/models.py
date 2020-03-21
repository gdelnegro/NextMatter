import re
from urllib.parse import urlparse, urljoin

import validators
import requests
from bs4 import BeautifulSoup
from backend.exceptions import InvalidURLException


class WebSiteInformation:
    url = ''
    information = None
    title = None
    headers = {}
    links = {
        "internal": set(),
        "external": set(),
        "unreachable": set()
    }
    has_login = None
    _html = None

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

    @property
    def website_html(self):
        if not self._html:
            self._html = requests.get(self.url).text
        return self._html

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
    def _format_href(url, href):
        parsed_href = urlparse(urljoin(url, href))
        formatted_href = "%(scheme)s://%(netloc)s%(path)s" % {"scheme": parsed_href.scheme,
                                                              "netloc": parsed_href.netloc,
                                                              "path": parsed_href.path
                                                              }
        return formatted_href

    @staticmethod
    def _has_login_form(soup):
        # check if it has a password field in the web
        # or if there's a login/sign in button
        _soup = str(soup)

        sign_in_group = True if re.search(r'([sS]ign).([iI]n)', _soup) is not None else False
        login_group = True if re.search(r'([lL]og).([iI]n)', _soup) else False
        password_group = True if re.search(r'([pP]assword)', _soup) else False
        return any([sign_in_group, login_group, password_group])

    @staticmethod
    def _get_all_headers(soup):
        headers = dict()
        for header in soup.find_all(re.compile(r'^h[1-6]$')):
            header_tag = str(header)[1:3].lower()
            if header_tag not in headers:
                headers.update({header_tag: 1})
            else:
                headers[header_tag] += 1
        return headers

    @staticmethod
    def _get_all_links(url, soup):
        links = {
            "internal": set(),
            "external": set(),
            "unreachable": set()
        }

        domain_name = urlparse(url).netloc
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if not href:
                continue
            formatted_href = WebSiteInformation._format_href(url, href)
            if not WebSiteInformation.is_valid_url(formatted_href):
                continue
            if formatted_href in links["internal"]:
                pass
            if formatted_href in links["external"]:
                pass
            if WebSiteInformation.ping_url(formatted_href):
                if domain_name not in formatted_href:
                    links["external"].add(formatted_href)
                else:
                    links["internal"].add(formatted_href)
            else:
                links["unreachable"].add(formatted_href)
        return links

    def get_website_information(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(self.website_html, "html.parser")
            self.title = soup.title.string
            self.headers = WebSiteInformation._get_all_headers(soup)
            self.has_login = WebSiteInformation._has_login_form(soup)
            self.links = WebSiteInformation._get_all_links(self.url, soup)

    def to_json(self):
        pass

    @classmethod
    def from_json(cls, json):
        pass
