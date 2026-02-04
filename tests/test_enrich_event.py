from tests.test_setup import TestServices
from unittest.mock import patch
from src.main import enrich_event

class TestEnrichEvent(TestServices):

    @patch('src.main.get_minimum_price')
    def test_enrich_event_success(self, mock_get_minimum_price):
        # Mock the get_minimum_price function to avoid actual API calls
        mock_get_minimum_price.return_value = 25.00
        
        event = {
            "id": "34001AGQQHTLTHTMBJQGPRQRMLLBGHNMV",
            "duration": 60,
            "name": "Sample Test Event 1"
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
        
    @patch('src.main.get_minimum_price')
    def test_enrich_event_with_exclusion(self, mock_get_minimum_price):
        """Test that excluded events return empty list"""
        mock_get_minimum_price.return_value = 25.00
        
        event = {
            "id": "34001AGQQHTLTHTMBJQGPRQRMLLBGHNMV",
            "duration": 60,
            "name": "Gift Voucher"
        }
        
        additional_info = {
            "exclusion_patterns": ["Gift Voucher", "Volunteer Shift"]
        }

        result = enrich_event(
            event,
            self.mock_venues,
            self.mock_instances,
            self.mock_plans,
            additional_info=additional_info
        )

        # Should return empty list for excluded events
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
        
    @patch('src.main.get_minimum_price')
    def test_enrich_event_not_excluded(self, mock_get_minimum_price):
        """Test that non-excluded events are processed normally"""
        mock_get_minimum_price.return_value = 25.00
        
        event = {
            "id": "34001AGQQHTLTHTMBJQGPRQRMLLBGHNMV",
            "duration": 60,
            "name": "Regular Show"
        }
        
        additional_info = {
            "exclusion_patterns": ["Gift Voucher", "Volunteer Shift"]
        }

        result = enrich_event(
            event,
            self.mock_venues,
            self.mock_instances,
            self.mock_plans,
            additional_info=additional_info
        )

        # Should process normally
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        
    @patch('src.main.get_minimum_price')
    def test_enrich_event_case_insensitive_exclusion(self, mock_get_minimum_price):
        """Test that exclusions are case-insensitive"""
        mock_get_minimum_price.return_value = 25.00
        
        event = {
            "id": "34001AGQQHTLTHTMBJQGPRQRMLLBGHNMV",
            "duration": 60,
            "name": "GIFT VOUCHER"  # All caps
        }
        
        additional_info = {
            "exclusion_patterns": ["Gift Voucher"]  # Mixed case
        }

        result = enrich_event(
            event,
            self.mock_venues,
            self.mock_instances,
            self.mock_plans,
            additional_info=additional_info
        )

        # Should exclude regardless of case
        self.assertEqual(len(result), 0)