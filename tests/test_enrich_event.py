from tests.test_setup import TestServices
from unittest.mock import patch
from src.main import enrich_event

class TestEnrichEvent(TestServices):

    @patch('src.main.get_minimum_price')
    def test_enrich_event_success(self, mock_get_minimum_price):
        event = {
            "id": "34001AGQQHTLTHTMBJQGPRQRMLLBGHNMV",
            "duration": 60
        }

        result = enrich_event(
            event,
            self.mock_venues,
            self.mock_instances,
            self.mock_plans,
            additional_info={}
        )

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        enriched = result[0]

        self.assertIn("locations", enriched)
        self.assertIn("duration", enriched)
        self.assertEqual(enriched["duration"], "PT60M")
