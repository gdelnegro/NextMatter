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

    def test_get_all_links(self):
        pass


    def test_to_json(self):
        pass

    def test_from_json(self):
        pass