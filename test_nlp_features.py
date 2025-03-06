"""
Test script to demonstrate the integration of rapidfuzz and pyarabic.
"""

import logging
from transliteration.mapper import TransliterationMapper
from transliteration.fuzzy_match import FuzzyMatcher, RAPIDFUZZ_AVAILABLE
from transliteration.arabic_utils import ArabicProcessor, PYARABIC_AVAILABLE

# Set up minimal logging - only show warnings and above
logging.basicConfig(level=logging.WARNING)

def test_fuzzy_matching():
    """Test fuzzy matching with rapidfuzz."""
    if not RAPIDFUZZ_AVAILABLE:
        print("rapidfuzz is not available. Skipping fuzzy matching tests.")
        return
        
    print("\n=== Testing Fuzzy Matching ===\n")
    
    # Create a dictionary of words
    test_dict = {
        "salam": "salām",
        "shukran": "šukran",
        "marhaba": "marḥaba",
        "sabah": "ṣabāḥ",
        "khalas": "ḫalāṣ",
        "mumkin": "mumkin",
        "mamnun": "mamnūn"
    }
    
    # Create a fuzzy matcher
    matcher = FuzzyMatcher(default_threshold=75)
    
    # Test exact match
    word = "salam"
    match, value, score = matcher.find_match(word, test_dict)
    print(f"Exact match for '{word}': {match} -> {value} (score: {score})")
    
    # Test fuzzy matches
    test_words = [
        "slam",       # Typo: missing 'a'
        "shukren",    # Typo: 'e' instead of 'a'
        "mar7aba",    # Number: '7' instead of 'h'
        "sabaa",      # Typo: 'aa' instead of 'ah'
        "khalass",    # Typo: doubled 's'
        "mumken",     # Typo: 'e' instead of 'i'
        "mamnoun"     # Variation: 'ou' instead of 'u'
    ]
    
    for word in test_words:
        match, value, score = matcher.find_match(word, test_dict)
        if value:
            print(f"Fuzzy match for '{word}': {match} -> {value} (score: {score})")
        else:
            print(f"No match found for '{word}' using threshold {matcher.default_threshold}")
    
    # Test multiple matches
    word = "salam"
    matches = matcher.find_multiple_matches(word, test_dict, limit=3, threshold=60)
    print(f"\nTop 3 matches for '{word}':")
    for match, value, score in matches:
        print(f"  {match} -> {value} (score: {score})")

def test_arabic_processing():
    """Test Arabic text processing with pyarabic."""
    if not PYARABIC_AVAILABLE:
        print("pyarabic is not available. Skipping Arabic processing tests.")
        return
        
    print("\n=== Testing Arabic Processing ===\n")
    
    # Create an Arabic processor
    processor = ArabicProcessor()
    
    # Test some Arabic text
    arabic_text = "السَّلَامُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ"
    normalized = processor.normalize_arabic(arabic_text)
    print(f"Original Arabic text: {arabic_text}")
    print(f"Normalized text: {normalized}")
    
    # Test Arabica to Arabic conversion
    arabica_samples = [
        "salām ʿalaykum wa-raḥmatu llāhi wa-barakātuhu",
        "ʾayna l-madrasa?",
        "al-baytu kabīrun",
        "ḏahaba ʾilā l-sūqi",
        "hāḏā kitābun ǧamīlun"
    ]
    
    print("\nArabica to Arabic conversion:")
    for sample in arabica_samples:
        arabic = processor.convert_arabica_to_arabic(sample)
        print(f"  {sample} -> {arabic}")

def test_integrated_functionality():
    """Test the integrated functionality in the mapper."""
    print("\n=== Testing Integrated Functionality ===\n")
    
    # Create a mapper with a higher fuzzy threshold for demonstration
    mapper = TransliterationMapper(fuzzy_threshold=70)
    
    # Sample texts with variations and typos
    test_cases = [
        # Near matches that should be found with fuzzy matching
        "slam 3alikom",               # "salam" with a letter missing
        "mrhba bik ya sadiki",        # "marhaba" with a letter missing
        "shoukran jazilan",           # "shukran" with a vowel variation
        "l7mdullah 3la salama",       # Typical chat spelling
        
        # Standard test cases
        "kaifa 7aluka?",              # Mix of standard and chat spelling
        "ana sa2mot 3la maw3iduna",   # Numbers in chat alphabet
        "hal turid shay2an lilshrb?", # More formal text with chat elements
        
        # Test with mixed vocabulary
        "msh mushkila, sa2aji later", # Mix of Arabic and English
        "c'est kif kif binnisba li",  # Mix of French and Arabic
    ]
    
    # Test each case
    for test in test_cases:
        result = mapper.convert(test)
        print(f"Input : {test}")
        print(f"Output: {result}")
        print("-" * 50)

def main():
    """Run all tests."""
    test_fuzzy_matching()
    test_arabic_processing()
    test_integrated_functionality()

if __name__ == "__main__":
    main()
