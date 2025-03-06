"""
Module for applying dictionary-based corrections to transliterated text.
This provides a final pass to fix common errors and inconsistencies.
"""

import re
import os
import json
import logging
from typing import Dict, List, Optional, Set

class TransliterationCorrector:
    """
    Applies dictionary-based and pattern-based corrections to transliterated text.
    """
    
    def __init__(self, custom_path: Optional[str] = None):
        """
        Initialize the corrector with correction dictionaries.
        
        Args:
            custom_path: Optional path to custom correction files
        """
        self.logger = logging.getLogger(__name__)
        
        # Default path
        default_path = os.path.join(os.path.dirname(__file__), 'corrections')
        
        # Use custom path if provided
        self.corrections_path = custom_path if custom_path else default_path
        
        # Load correction dictionaries
        self.word_corrections = {}
        self.pattern_corrections = []
        self.suffix_corrections = {}
        self.load_corrections()
    
    def load_corrections(self):
        """Load correction dictionaries from files."""
        # Create directory if it doesn't exist
        if not os.path.exists(self.corrections_path):
            try:
                os.makedirs(self.corrections_path)
                
                # Create default word corrections file
                word_corrections_path = os.path.join(self.corrections_path, 'word_corrections.json')
                with open(word_corrections_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        "description": "Word-level corrections for transliterated text",
                        "corrections": {
                            "salam": "salām",
                            "mabruk": "mabrūk",
                            "shukran": "šukran"
                        }
                    }, f, indent=2, ensure_ascii=False)
                
                # Create default pattern corrections file
                pattern_corrections_path = os.path.join(self.corrections_path, 'pattern_corrections.json')
                with open(pattern_corrections_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        "description": "Pattern-based corrections for transliterated text",
                        "corrections": [
                            {"pattern": "([aeiou])\\1", "replacement": "\\1"},
                            {"pattern": "([^aeiou])([^aeiou])\\2", "replacement": "\\1\\2"},
                            {"pattern": "al (\w)", "replacement": "al-\\1"}
                        ]
                    }, f, indent=2, ensure_ascii=False)
                
                # Create default suffix corrections file
                suffix_corrections_path = os.path.join(self.corrections_path, 'suffix_corrections.json')
                with open(suffix_corrections_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        "description": "Suffix-based corrections for transliterated text",
                        "corrections": {
                            "i$": "ī",
                            "a$": "ā",
                            "u$": "ū"
                        }
                    }, f, indent=2, ensure_ascii=False)
                
                self.logger.info("Created default correction files")
            except Exception as e:
                self.logger.warning(f"Could not create correction files: {str(e)}")
        
        # Load word corrections
        word_corrections_path = os.path.join(self.corrections_path, 'word_corrections.json')
        if os.path.exists(word_corrections_path):
            try:
                with open(word_corrections_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.word_corrections = data.get("corrections", {})
                    self.logger.info(f"Loaded {len(self.word_corrections)} word corrections")
            except Exception as e:
                self.logger.error(f"Error loading word corrections: {str(e)}")
        
        # Load pattern corrections
        pattern_corrections_path = os.path.join(self.corrections_path, 'pattern_corrections.json')
        if os.path.exists(pattern_corrections_path):
            try:
                with open(pattern_corrections_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.pattern_corrections = data.get("corrections", [])
                    self.logger.info(f"Loaded {len(self.pattern_corrections)} pattern corrections")
            except Exception as e:
                self.logger.error(f"Error loading pattern corrections: {str(e)}")
        
        # Load suffix corrections
        suffix_corrections_path = os.path.join(self.corrections_path, 'suffix_corrections.json')
        if os.path.exists(suffix_corrections_path):
            try:
                with open(suffix_corrections_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.suffix_corrections = data.get("corrections", {})
                    self.logger.info(f"Loaded {len(self.suffix_corrections)} suffix corrections")
            except Exception as e:
                self.logger.error(f"Error loading suffix corrections: {str(e)}")
    
    def apply_corrections(self, text: str) -> str:
        """
        Apply all corrections to the transliterated text.
        
        Args:
            text: Transliterated text to correct
            
        Returns:
            Corrected text
        """
        if not text:
            return ""
        
        # Process by splitting into words
        words = re.findall(r'\b\w+\b|\S+', text)
        result_words = []
        
        for word in words:
            # Skip non-word tokens
            if not re.match(r'^\w+$', word):
                result_words.append(word)
                continue
            
            # Check if it's in the word corrections dictionary
            word_lower = word.lower()
            if word_lower in self.word_corrections:
                correction = self.word_corrections[word_lower]
                # Preserve capitalization
                if word[0].isupper() and len(correction) > 0:
                    correction = correction[0].upper() + correction[1:]
                result_words.append(correction)
                continue
            
            # Apply suffix corrections
            corrected_word = word
            for suffix_pattern, replacement in self.suffix_corrections.items():
                corrected_word = re.sub(f'{suffix_pattern}', replacement, corrected_word)
            
            result_words.append(corrected_word)
        
        # Join words back into text
        result = ' '.join(result_words)
        
        # Apply pattern corrections
        for pattern_info in self.pattern_corrections:
            pattern = pattern_info.get("pattern", "")
            replacement = pattern_info.get("replacement", "")
            if pattern and replacement:
                result = re.sub(pattern, replacement, result)
        
        return result
