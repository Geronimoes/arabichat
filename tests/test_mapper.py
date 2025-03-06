"""
Tests for the TransliterationMapper class.
"""

import pytest
import sys
import os

# Add the parent directory to the path so we can import the application modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from transliteration.mapper import TransliterationMapper

class TestTransliterationMapper:
    """Test suite for the TransliterationMapper class."""
    
    def setup_method(self):
        """Set up the test environment."""
        self.mapper = TransliterationMapper()
    
    def test_basic_conversion(self):
        """Test basic character conversion."""
        assert self.mapper.convert("mar7aba") == "marḥaba"
        assert self.mapper.convert("3arabi") == "ʿarabi"
        assert self.mapper.convert("shukran") == "šukran"
    
    def test_moroccan_dialect(self):
        """Test Moroccan dialect specific features."""
        # Test "g" for qaf
        assert self.mapper.convert("gal", dialect="moroccan") == "gal"
        
        # Test emphatic consonants
        assert self.mapper.convert("Tarig", dialect="moroccan") == "ṭarig"
        assert self.mapper.convert("Sa7ra", dialect="moroccan") == "ṣaḥra"
    
    def test_long_vowels(self):
        """Test long vowel conversion."""
        assert self.mapper.convert("kitaab") == "kitāb"
        assert self.mapper.convert("kariim") == "karīm"
        assert self.mapper.convert("3uyuun") == "ʿuyūn"
    
    def test_definite_article(self):
        """Test definite article handling."""
        assert self.mapper.convert("al-shams") == "al-šams"
        assert self.mapper.convert("al shams") == "al-šams"
        
    def test_empty_input(self):
        """Test empty input handling."""
        assert self.mapper.convert("") == ""
        assert self.mapper.convert(None) == ""

    def test_taa_marbutah(self):
        """Test taa marbutah handling."""
        assert self.mapper.convert("madina_t al-maghrib") == "madīnat al-maġrib"
        assert self.mapper.convert("madina_t") == "madīna"
