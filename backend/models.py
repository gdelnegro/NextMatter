import json
import re

import validators
import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

from backend.data_access import get_website_html, ping_url
from backend.exceptions import InvalidURLException


class WebSiteInformation:
    url = ''
    information = None
    title = None
    headers = {}
    links = {
        "internal": list(),
        "external": list(),
        "unreachable": list()
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

    @staticmethod
    def is_valid_url(url):
        validation_result = validators.url(url)
        if validation_result is True:
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
            "internal": list(),
            "external": list(),
            "unreachable": list()
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
            if ping_url(formatted_href):
                if domain_name not in formatted_href:
                    links["external"].append(formatted_href)
                else:
                    links["internal"].append(formatted_href)
            else:
                links["unreachable"].append(formatted_href)
        return links

    def get_website_information(self):
        website_html = get_website_html(self.url)
        soup = BeautifulSoup(website_html, "html.parser")
        self.title = soup.title.string
        self.headers = WebSiteInformation._get_all_headers(soup)
        self.has_login = WebSiteInformation._has_login_form(soup)
        self.links = WebSiteInformation._get_all_links(self.url, soup)

    def to_dict(self):
        return {
            "url": self.url,
            "title": self.title,
            "headers": self.headers,
            "links": self.links,
            "has_login": self.has_login
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_string):
        json_representation = json.loads(json_string)
        website = cls(json_representation["url"])
        website.has_login = json_representation["has_login"]
        website.title = json_representation["title"]
        website.headers = json_representation["headers"]
        website.links = json_representation["links"]
        return website
