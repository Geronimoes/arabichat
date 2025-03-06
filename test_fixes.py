"""
Script to test the fixes to the rapidfuzz and pyarabic implementations.
"""

import logging
import sys
from transliteration.mapper import TransliterationMapper
from transliteration.fuzzy_match import FuzzyMatcher

# Silence warnings for cleaner output
logging.basicConfig(level=logging.ERROR)

def test_al_spacing():
    """Test the al- spacing issue."""
    mapper = TransliterationMapper()
    
    test_phrases = [
        "al-kitab",
        "al kitab",
        "al -kitab",
        "al- kitab",
        "qara'tu fi al-kitab",
        "madrasat al-banin",
        "hatha min al manzil"
    ]
    
    print("\n=== Testing al- Spacing Fix ===\n")
    for phrase in test_phrases:
        result = mapper.convert(phrase)
        print(f"Input:  {phrase}")
        print(f"Output: {result}")
        print("-" * 50)

def test_punctuation_spacing():
    """Test spacing around punctuation."""
    mapper = TransliterationMapper()
    
    test_phrases = [
        "marhaba, kaifa haluka?",
        "shukran ! ana bikhair.",
        "hal anta; am akhouka?",
        "qala : na'am"
    ]
    
    print("\n=== Testing Punctuation Spacing Fix ===\n")
    for phrase in test_phrases:
        result = mapper.convert(phrase)
        print(f"Input:  {phrase}")
        print(f"Output: {result}")
        print("-" * 50)

def test_fuzzy_matching():
    """Test fuzzy matching with the updated code."""
    try:
        # Create a simple dictionary
        test_dict = {
            "salam": "salām",
            "marhaba": "marḥaba",
            "shukran": "šukran"
        }
        
        # Create a matcher
        matcher = FuzzyMatcher(default_threshold=70)
        
        # Test words
        test_words = ["salam", "slam", "salaam", "marhba", "marhabaa", "shokran"]
        
        print("\n=== Testing Fixed Fuzzy Matching ===\n")
        for word in test_words:
            match, value, score = matcher.find_match(word, test_dict)
            if match:
                print(f"'{word}' matched with '{match}' -> '{value}' (score: {score})")
            else:
                print(f"No match found for '{word}'")
    except Exception as e:
        print(f"Error in fuzzy matching test: {e}")

def main():
    """Run all tests."""
    print("\nTesting fixes for ArabiChat...\n")
    
    # Test each fixed issue
    test_al_spacing()
    test_punctuation_spacing()
    test_fuzzy_matching()
    
    print("\nTests completed.\n")

if __name__ == "__main__":
    main()
