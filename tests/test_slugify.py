import unittest
from src.util import slugify


class TestSlugify(unittest.TestCase):
    """Test cases for the slugify function with real-world examples from Spektrix sources"""

    def test_apostrophe_removal_curly(self):
        """Test removal of curly apostrophes"""
        # Tidemark Theatre example
        self.assertEqual(
            slugify("CRFF Local's Showcase"),
            "crff-locals-showcase"
        )
        
    def test_apostrophe_removal_straight(self):
        """Test removal of straight apostrophes"""
        # NACC example
        self.assertEqual(
            slugify("Alex Mackenzie's Never Been Better Tour"),
            "alex-mackenzies-never-been-better-tour"
        )
        
    def test_apostrophe_in_contractions(self):
        """Test apostrophe removal in contractions"""
        # Sid Williams Theatre example
        self.assertEqual(
            slugify("Let's Go Surfin'! A Beach Boys Tribute"),
            "lets-go-surfin-a-beach-boys-tribute"
        )
        
    def test_possessive_names(self):
        """Test possessive forms with apostrophes"""
        # Calgary Philharmonic example
        self.assertEqual(
            slugify("Vivaldi's Ring of Mystery"),
            "vivaldis-ring-of-mystery"
        )
        
        # Metro Theatre example
        self.assertEqual(
            slugify("Neil Simon's Barefoot in the Park"),
            "neil-simons-barefoot-in-the-park"
        )
        
    def test_complex_apostrophes(self):
        """Test complex cases with multiple apostrophes"""
        # Port Theatre example
        self.assertEqual(
            slugify("SPOTLIGHT: Netflix's The Making of Life on Our Planet"),
            "spotlight-netflixs-the-making-of-life-on-our-planet"
        )
        
    def test_accent_removal(self):
        """Test removal of accents from characters"""
        self.assertEqual(
            slugify("Café Théâtre"),
            "cafe-theatre"
        )

    def test_lowercase_conversion(self):
        """Test that text is converted to lowercase"""
        self.assertEqual(
            slugify("HELLO WORLD"),
            "hello-world"
        )
        
        self.assertEqual(
            slugify("MiXeD CaSe"),
            "mixed-case"
        )
        
    def test_special_characters_replacement(self):
        """Test that special characters are replaced with hyphens"""
        self.assertEqual(
            slugify("Hello & World"),
            "hello-world"
        )
        
        self.assertEqual(
            slugify("Let's Get Loud!"),
            "lets-get-loud"
        )
        
        self.assertEqual(
            slugify("Question?"),
            "question"
        )
        
    def test_multiple_hyphens_collapsed(self):
        """Test that multiple hyphens are collapsed into one"""
        self.assertEqual(
            slugify("Hello   World"),
            "hello-world"
        )
        
        self.assertEqual(
            slugify("A -- B"),
            "a-b"
        )
        
    def test_leading_trailing_hyphens_removed(self):
        """Test that leading and trailing hyphens are removed"""
        self.assertEqual(
            slugify("---Hello World---"),
            "hello-world"
        )
        
        self.assertEqual(
            slugify("   Test   "),
            "test"
        )
        
    def test_numbers_preserved(self):
        """Test that numbers are preserved in slugs"""
        self.assertEqual(
            slugify("Event 2026"),
            "event-2026"
        )
        
        self.assertEqual(
            slugify("123 Main Street"),
            "123-main-street"
        )
        
    def test_combined_complex_case(self):
        """Test a complex real-world case combining multiple features"""
        # Combines apostrophes, accents, special chars
        self.assertEqual(
            slugify("Simon's Café: A Naïve Approach!"),
            "simons-cafe-a-naive-approach"
        )
        
    def test_empty_string(self):
        """Test handling of empty strings"""
        self.assertEqual(slugify(""), "")
        
    def test_only_special_characters(self):
        """Test strings with only special characters"""
        self.assertEqual(slugify("!!!"), "")
        self.assertEqual(slugify("---"), "")
        

if __name__ == '__main__':
    unittest.main()