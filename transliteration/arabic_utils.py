"""
Arabic text processing utilities using pyarabic.

This module provides functions for processing Arabic text, including normalization,
diacritics handling, and other Arabic-specific operations.
"""

import logging
from typing import Dict, List, Optional, Set

# Try to import pyarabic, but don't fail if not available
try:
    import pyarabic.araby as araby
    import pyarabic.trans
    PYARABIC_AVAILABLE = True
except ImportError:
    PYARABIC_AVAILABLE = False
    logging.warning("pyarabic not available. Arabic text processing will be limited.")

class ArabicProcessor:
    """
    Provides Arabic text processing capabilities.
    """
    
    def __init__(self):
        """Initialize the Arabic processor."""
        self.logger = logging.getLogger(__name__)
        
        if not PYARABIC_AVAILABLE:
            self.logger.warning("ArabicProcessor initialized but pyarabic is not available.")
    
    def normalize_arabic(self, text: str) -> str:
        """
        Normalize Arabic text by removing diacritics and normalizing characters.
        
        Args:
            text: Arabic text to normalize
            
        Returns:
            Normalized text
        """
        if not PYARABIC_AVAILABLE:
            self.logger.warning("Arabic normalization attempted but pyarabic is not available.")
            return text
            
        if not text:
            return ""
            
        try:
            # Remove diacritics
            text = araby.strip_tashkeel(text)
            
            # Normalize hamza forms
            text = araby.normalize_hamza(text)
            
            # Normalize lam-alef
            text = araby.normalize_lamalef(text)
            
            return text
            
        except Exception as e:
            self.logger.error(f"Error in Arabic normalization: {str(e)}")
            return text
    
    def add_diacritics(self, text: str) -> str:
        """
        Add missing diacritics to Arabic text (best effort).
        This is a simplified approach and won't be perfect.
        
        Args:
            text: Arabic text to add diacritics to
            
        Returns:
            Text with diacritics
        """
        if not PYARABIC_AVAILABLE:
            self.logger.warning("Arabic diacritization attempted but pyarabic is not available.")
            return text
            
        if not text:
            return ""
            
        # This is a placeholder - pyarabic doesn't have a built-in diacritizer
        # In a real implementation, you might use a machine learning model or rules
        # For now, we'll just return the original text
        return text
    
    def is_arabic(self, text: str) -> bool:
        """
        Check if text contains Arabic characters.
        
        Args:
            text: Text to check
            
        Returns:
            True if text contains Arabic characters
        """
        if not PYARABIC_AVAILABLE:
            self.logger.warning("Arabic detection attempted but pyarabic is not available.")
            # Fallback implementation
            arabic_ranges = [
                (0x0600, 0x06FF),  # Arabic
                (0x0750, 0x077F),  # Arabic Supplement
                (0x08A0, 0x08FF),  # Arabic Extended-A
                (0xFB50, 0xFDFF),  # Arabic Presentation Forms-A
                (0xFE70, 0xFEFF),  # Arabic Presentation Forms-B
            ]
            
            for char in text:
                code = ord(char)
                for start, end in arabic_ranges:
                    if start <= code <= end:
                        return True
            return False
            
        try:
            return araby.is_arabicstring(text)
        except Exception as e:
            self.logger.error(f"Error in Arabic detection: {str(e)}")
            return False
    
    def convert_arabica_to_arabic(self, text: str) -> str:
        """
        Convert text from Arabica transliteration to Arabic script.
        This uses a more sophisticated approach than the basic mapper.
        
        Args:
            text: Text in Arabica transliteration
            
        Returns:
            Text in Arabic script
        """
        if not PYARABIC_AVAILABLE:
            self.logger.warning("Arabica to Arabic conversion attempted but pyarabic is not available.")
            return text
            
        if not text:
            return ""
            
        # Define custom transliteration map that's closer to Arabica system
        # This extends the basic pyarabic transliteration system
        trans_map = {
            'ʾ': 'ء',  # hamza
            'ā': 'ا',  # alif
            'b': 'ب',  # ba
            't': 'ت',  # ta
            'ṯ': 'ث',  # tha
            'j': 'ج',  # jim
            'ǧ': 'ج',  # jim (alt)
            'ḥ': 'ح',  # ha
            'ḫ': 'خ',  # kha
            'd': 'د',  # dal
            'ḏ': 'ذ',  # dhal
            'r': 'ر',  # ra
            'z': 'ز',  # zay
            's': 'س',  # sin
            'š': 'ش',  # shin
            'ṣ': 'ص',  # sad
            'ḍ': 'ض',  # dad
            'ṭ': 'ط',  # ta
            'ẓ': 'ظ',  # za
            'ʿ': 'ع',  # ayn
            'ġ': 'غ',  # ghayn
            'f': 'ف',  # fa
            'q': 'ق',  # qaf
            'k': 'ك',  # kaf
            'l': 'ل',  # lam
            'm': 'م',  # mim
            'n': 'ن',  # nun
            'h': 'ه',  # ha
            'w': 'و',  # waw
            'ū': 'و',  # waw with damma
            'y': 'ي',  # ya
            'ī': 'ي',  # ya with kasra
            'g': 'گ',  # gaf (for Persian/Urdu/Kurdish)
            'p': 'پ',  # pe (for Persian/Urdu)
            'v': 'ڤ',  # ve (for foreign words)
            'a': 'َ',   # fatha
            'i': 'ِ',   # kasra
            'u': 'ُ',   # damma
        }
        
        # Special patterns to handle before character-by-character conversion
        special_patterns = {
            'al-': 'ال',
            'wa-': 'وَ',
            'bi-': 'بِ',
            'li-': 'لِ',
            'fī': 'في',
            'min': 'مِن',
            'ʿan': 'عَن',
            'maʿa': 'مَعَ',
            'ʾilā': 'إلى',
            'ʾillā': 'إلَّا',
            'baʿḍ': 'بَعض',
            'baʿd': 'بَعد',
            'qabla': 'قَبلَ',
            'ḥattā': 'حَتَّى',
            'kullu': 'كُلُّ',
            'kull': 'كُلّ',
            'ʾanna': 'أَنَّ',
            'ʾinna': 'إِنَّ',
            'ʾin': 'إِن',
            'ʾiḏā': 'إِذَا',
            'kaṯīr': 'كَثِير',
            'kabīr': 'كَبِير',
            'ṣaġīr': 'صَغِير',
            'ǧamīl': 'جَمِيل',
            'ǧadīd': 'جَدِيد',
            'qadīm': 'قَدِيم',
        }
        
        # Apply special patterns
        for pattern, replacement in special_patterns.items():
            text = text.replace(pattern, replacement)
        
        # Apply character-by-character conversion with context awareness
        result = ""
        i = 0
        while i < len(text):
            # Check for multi-character sequences
            found = False
            for seq_len in range(3, 0, -1):  # Try 3-char, then 2-char, then 1-char
                if i + seq_len <= len(text):
                    seq = text[i:i+seq_len]
                    if seq in trans_map:
                        result += trans_map[seq]
                        i += seq_len
                        found = True
                        break
            
            # If no multi-character match, process single character
            if not found:
                char = text[i]
                if char in trans_map:
                    result += trans_map[char]
                else:
                    result += char
                i += 1
        
        # Apply Arabic text normalization and cleanup
        if PYARABIC_AVAILABLE:
            try:
                # Join letters properly
                result = araby.join_letters(result)
                
                # Fix tashkeel placement
                result = araby.normalize_tashkeel(result)
                
                # Handle lamalef
                result = araby.normalize_lamalef(result)
            except Exception as e:
                self.logger.error(f"Error in Arabic normalization: {str(e)}")
        
        return result
    
    def get_word_root(self, word: str) -> Optional[str]:
        """
        Get the root of an Arabic word (if pyarabic supports it).
        
        Args:
            word: Arabic word
            
        Returns:
            Root of the word or None if not found
        """
        # Note: pyarabic doesn't currently offer good root extraction
        # This is a placeholder for future implementation
        return None
