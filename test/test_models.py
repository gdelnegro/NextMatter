from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock
from backend.models import WebSiteInformation
from backend.exceptions import InvalidURLException


class TestWebSiteInformation(TestCase):

    def test__is_valid_url(self):
        assert WebSiteInformation.is_valid_url("google.com") is False
        assert WebSiteInformation.is_valid_url("http://google.com") is True
        assert WebSiteInformation.is_valid_url("invalid_website.com") is False
        assert WebSiteInformation.is_valid_url("http://invalid_website.com") is False

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


