"""
Module for converting Arabica transliteration to Arabic script.
This is an experimental feature and provides only basic conversion.
"""

import re

# Mapping from Arabica transliteration to Arabic script
ARABICA_TO_ARABIC = {
    # Consonants
    'b': 'ب',
    't': 'ت',
    'ṯ': 'ث',
    'j': 'ج',
    'ǧ': 'ج',
    'ḥ': 'ح',
    'ḫ': 'خ',
    'd': 'د',
    'ḏ': 'ذ',
    'r': 'ر',
    'z': 'ز',
    's': 'س',
    'š': 'ش',
    'ṣ': 'ص',
    'ḍ': 'ض',
    'ṭ': 'ط',
    'ẓ': 'ظ',
    'ʿ': 'ع',
    'ġ': 'غ',
    'f': 'ف',
    'q': 'ق',
    'k': 'ك',
    'l': 'ل',
    'm': 'م',
    'n': 'ن',
    'h': 'ه',
    'w': 'و',
    'y': 'ي',
    'g': 'گ',  # For Moroccan Arabic
    
    # Vowels
    'a': 'َ',  # fatha
    'i': 'ِ',  # kasra
    'u': 'ُ',  # damma
    'ā': 'ا',  # alif
    'ī': 'ي',  # ya
    'ū': 'و',  # waw
    
    # Hamza and special characters
    'ʾ': 'ء',  # hamza
    '-': ' ',  # hyphen to space
}

# Special combinations and context-dependent rules
SPECIAL_PATTERNS = [
    # Al definite article
    (r'al-([^\s]+)', r'ال\1'),
    
    # Taa marbouta
    (r'a\b', r'ة'),
    
    # Alif laam combinations
    (r'lā', r'لا'),
    
    # Initial alif
    (r'^\s*a', r'ا'),
    (r'\s+a', r' ا'),
    
    # Doubled consonants
    (r'([bcdfghjklmnpqrstvwxyz])\1', r'\1ّ'),
    
    # Custom rules for Moroccan dialectal forms
    (r'š', r'ش'),
    
    # Punctuation
    (r'\.', r'۔'),
    (r'\?', r'؟'),
    (r',', r'،'),
]

def to_arabic_script(text):
    """
    Convert Arabica transliteration to Arabic script.
    This is a basic implementation and may not handle all cases correctly.
    
    Args:
        text: Text in Arabica transliteration
        
    Returns:
        Text converted to Arabic script (approximate)
    """
    if not text:
        return ""
    
    # Apply special patterns first
    for pattern, replacement in SPECIAL_PATTERNS:
        text = re.sub(pattern, replacement, text)
    
    # Convert character by character
    result = ""
    i = 0
    while i < len(text):
        char = text[i]
        if char in ARABICA_TO_ARABIC:
            result += ARABICA_TO_ARABIC[char]
        else:
            result += char
        i += 1
    
    return result
