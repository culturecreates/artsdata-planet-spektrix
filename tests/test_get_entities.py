from tests.test_setup import TestServices
from unittest.mock import MagicMock, patch
from src.main import get_entities

class TestGetEntities(TestServices):
    
    @patch('src.main.requests.get')
    def test_get_entities_success(self, mock_requests):
        # Fake HTTP response object
        mock_response = MagicMock()
        mock_response.json.return_value = self.events_data
        mock_response.raise_for_status.return_value = None

        mock_requests.return_value = mock_response

        result = get_entities("events")

        self.assertEqual(result, self.events_data)
        mock_requests.assert_called_once()


    @patch("src.main.requests.get")
    def test_get_entities_failure(self, mock_get):
        mock_get.side_effect = Exception("API Down")

        with self.assertRaises(Exception):
            get_entities("events")
