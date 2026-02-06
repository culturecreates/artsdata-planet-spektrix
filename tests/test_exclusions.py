import unittest
from src.util import should_exclude_event


class TestExclusions(unittest.TestCase):
    """Test cases for event exclusion functionality"""
    
    def test_exact_match_case_insensitive(self):
        """Test that exact matches work case-insensitively"""
        patterns = ["Volunteer Shift"]
        
        self.assertTrue(should_exclude_event("Volunteer Shift", patterns))
        self.assertTrue(should_exclude_event("volunteer shift", patterns))
        self.assertTrue(should_exclude_event("VOLUNTEER SHIFT", patterns))
        self.assertTrue(should_exclude_event("VolUnTeEr ShIfT", patterns))
        
    def test_exact_subtring_required(self):
        """Test that subtring matches trigger exclusion"""
        patterns = ["Volunteer Shift"]
        
        self.assertTrue(should_exclude_event("Volunteer shift 1", patterns))
        self.assertTrue(should_exclude_event("The Volunteer Shift", patterns))

        # These should NOT be excluded (not substring matches)
        self.assertFalse(should_exclude_event("Volunteer", patterns))
        self.assertFalse(should_exclude_event("Shift", patterns))
        
    def test_multiple_patterns(self):
        """Test matching against multiple exclusion patterns"""
        patterns = ["UBCO Heat", "Kelowna Falcons", "Gift Pack"]
        
        self.assertTrue(should_exclude_event("UBCO Heat", patterns))
        self.assertTrue(should_exclude_event("Kelowna Falcons", patterns))
        self.assertTrue(should_exclude_event("Gift Pack", patterns))
        self.assertTrue(should_exclude_event("gift pack", patterns))
        
    def test_no_match(self):
        """Test that non-matching events are not excluded"""
        patterns = ["Gift Voucher"]
        
        self.assertFalse(should_exclude_event("Regular Event", patterns))
        self.assertFalse(should_exclude_event("Concert", patterns))
        self.assertFalse(should_exclude_event("Gift", patterns))
        
    def test_empty_patterns_list(self):
        """Test that empty patterns list excludes nothing"""
        self.assertFalse(should_exclude_event("Any Event", []))
        self.assertFalse(should_exclude_event("Volunteer Shift", []))
        
    def test_none_patterns(self):
        """Test that None patterns list excludes nothing"""
        self.assertFalse(should_exclude_event("Any Event", None))
        
    def test_empty_event_name(self):
        """Test handling of empty event names"""
        patterns = ["Gift Voucher"]
        
        self.assertFalse(should_exclude_event("", patterns))
        self.assertFalse(should_exclude_event(None, patterns))


if __name__ == '__main__':
    unittest.main()