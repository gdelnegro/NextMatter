import json
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from bs4 import BeautifulSoup

from backend.models import WebSiteInformation
from backend.exceptions import InvalidURLException


class TestWebSiteInformation(TestCase):

    def test__is_valid_url(self):
        assert WebSiteInformation.is_valid_url("google.com") is False
        assert WebSiteInformation.is_valid_url("http://google.com") is True
        assert WebSiteInformation.is_valid_url("invalid_website.com") is False
        assert WebSiteInformation.is_valid_url("http://invalid_website.com") is False

    def test_WebSiteInformation(self):
        WebSiteInformation("http://google.com")
        WebSiteInformation("google.com")

    @patch("backend.models.requests.get")
    def test_website_html(self, mock_requests):
        test_html = "<html><a href='./test'></a><a href='http://google.com'></a></html>"
        mock_requests.return_value = Mock(status_code=200, text=test_html)
        website = WebSiteInformation("http://google.com")
        assert test_html == website.website_html

    def test__get_website_information_fails_for_invalid_urls(self):
        with self.assertRaises(expected_exception=InvalidURLException):
            WebSiteInformation(url='invalid_url')

    @patch("backend.models.requests.get")
    def test__ping_url(self, mock_requests):
        mock_requests.return_value = Mock(status_code=200)
        assert WebSiteInformation.ping_url("http://google.com") is True
        assert WebSiteInformation.ping_url("http://invalid_website.com") is True

    @patch("backend.models.requests.get")
    def test__ping_url_fails_with_status_different_than_200(self, mock_requests):
        mock_requests.return_value = Mock(status_code=404)
        assert WebSiteInformation.ping_url("http://google.com") is False
        assert WebSiteInformation.ping_url("http://invalid_website.com") is False

    @patch("backend.models.requests.get")
    def test__ping_url_fails_with_exceptions(self, mock_requests):
        mock_requests.side_effect = ValueError()
        with self.assertRaises(expected_exception=ValueError):
            WebSiteInformation.ping_url("http://google.com")

    def test__has_login_form(self):
        assert WebSiteInformation._has_login_form('blablablasign inlololakdkljas') is True
        assert WebSiteInformation._has_login_form('blablablaSign inlololakdkljas') is True
        assert WebSiteInformation._has_login_form('blablablaLog inlololakdkljas') is True

    def test__get_all_headers(self):
        html = "<html><h1>test</h1><h2>test2</h2></html>"
        soup = BeautifulSoup(html, "html.parser")
        headers = WebSiteInformation._get_all_headers(soup)
        assert 1 == headers["h1"]
        assert 1 == headers["h2"]

    def test__format_href(self):
        assert "http://google.com.br/test" == WebSiteInformation._format_href("http://google.com.br", "../../../../../test")
        assert "http://rte.ie" == WebSiteInformation._format_href("http://google.com.br", "http://rte.ie")

    @patch("backend.models.requests.get")
    def test__get_all_links(self, mock_requests):
        mock_requests.return_value = Mock(status_code=200)
        html = "<html><a href='./test'></a><a href='http://google.com'></a><a></a></html>"
        soup = BeautifulSoup(html, "html.parser")
        links = WebSiteInformation._get_all_links('http://test.com', soup)
        assert dict is type(links)
        assert "http://google.com" in links["external"]
        assert "http://test.com/test" in links["internal"]

    @patch("backend.models.requests.get")
    def test__get_all_links_unreachable_links(self, mock_requests):
        mock_requests.return_value = Mock(status_code=400)
        html = "<html><a href='./test'></a><a href='http://google.com'></a></html>"
        soup = BeautifulSoup(html, "html.parser")
        links = WebSiteInformation._get_all_links('http://test.com', soup)
        assert dict is type(links)
        assert "http://google.com" not in links["external"]
        assert "http://test.com/test" not in links["internal"]
        assert "http://test.com/test" in links["unreachable"]

    @patch("backend.models.requests.get")
    def test_get_website_information(self, mock_requests):
        test_html = '<!DOCTYPE html><html><head><title>Test</title></head><body><h2>HTML Links</h2><p><a href="https://www.google.com/html/">This will go to google</a></p></body></html>'
        mock_requests.return_value = Mock(status_code=200, text=test_html)
        website = WebSiteInformation("http://google.com")
        website.get_website_information()
        assert "Test" == website.title
        assert isinstance(website.links, dict)
        assert "https://www.google.com/html/" in website.links["internal"]
        assert isinstance(website.headers, dict)
        assert "h2" in website.headers
        assert 1 == website.headers["h2"]

    @patch("backend.models.requests.get")
    def test_to_json(self, mock_requests):
        test_html = '<!DOCTYPE html><html><head><title>Test</title></head><body><h2>HTML Links</h2><p><a href="https://www.google.com/html/">This will go to google</a></p></body></html>'
        mock_requests.return_value = Mock(status_code=200, text=test_html)
        website = WebSiteInformation("http://google.com")
        _json = website.to_json()
        json_object = json.loads(_json)
        assert json_object["url"] == website.url
        assert json_object["title"] == website.title
        assert json_object["headers"] == website.headers
        assert json_object["links"] == website.links
        assert json_object["has_login"] == website.has_login

    @patch("backend.models.requests.get")
    def test_from_json(self, mock_requests):
        test_html = '<!DOCTYPE html><html><head><title>Test</title></head><body><h2>HTML Links</h2><p><a href="https://www.google.com/html/">This will go to google</a></p></body></html>'
        mock_requests.return_value = Mock(status_code=200, text=test_html)
        website_from_json = WebSiteInformation.from_json('{"url": "http://google.com", "title": null, "headers": {}, "links": {"internal": [], "external": [], "unreachable": []}, "has_login": null}')
        website = WebSiteInformation("http://google.com")
        assert website_from_json.url == website.url
        assert website_from_json.title == website.title
        assert website_from_json.has_login == website.has_login
        assert website_from_json.headers == website.headers
        assert website_from_json.links == website.links
