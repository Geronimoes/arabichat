"""
Simple test script for the basic functionality.
"""

import logging
from transliteration.mapper import TransliterationMapper

# Set up minimal logging - only show warnings and above
logging.basicConfig(level=logging.WARNING)

def test_conversion():
    """Test basic conversion functionality."""
    mapper = TransliterationMapper()
    
    # Sample texts from various contexts
    test_cases = [
        "Salam 3alikom",
        "Kaifa 7aloka?",
        "ana sa2imtu min al-intidhar",
        "hal turid shay2an lilshorb?",
        "shabab, ta3alu huna!",
        "hadhihi mushkila kabiira",
        "ana dhaahib ila al-madrasah",
        "yawm al-ithnayn sa-adhhabu ila al-souq",
        "SbaH l5ir, kifach nta?"
    ]
    
    print("\n=== Testing Basic Conversion ===\n")
    
    # Process and display results
    for test in test_cases:
        result = mapper.convert(test)
        print(f"Input:  {test}")
        print(f"Output: {result}")
        print("-" * 60)

if __name__ == "__main__":
    test_conversion()
