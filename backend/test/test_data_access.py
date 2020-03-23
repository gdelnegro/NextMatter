import json
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from backend.data_access import ping_url


class TestDataAccess(TestCase):

    @patch("backend.models.requests.get")
    def test__ping_url(self, mock_requests):
        mock_requests.return_value = Mock(status_code=200)
        assert ping_url("http://google.com") is True
        assert ping_url("http://invalid_website.com") is True

    @patch("backend.models.requests.get")
    def test__ping_url_fails_with_status_different_than_200(self, mock_requests):
        mock_requests.return_value = Mock(status_code=404)
        assert ping_url("http://google.com") is False
        assert ping_url("http://invalid_website.com") is False

    @patch("backend.models.requests.get")
    def test__ping_url_fails_with_exceptions(self, mock_requests):
        mock_requests.side_effect = ValueError()
        with self.assertRaises(expected_exception=ValueError):
            ping_url("http://google.com")
