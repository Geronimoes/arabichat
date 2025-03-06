"""
Core transliteration functionality for converting Arabic chat to Arabica transliteration.
"""

import re
import os
import json
import logging
from typing import Dict, List, Optional, Tuple, Set

try:
    from camel_tools.utils.charmap import CharMapper
    CAMEL_TOOLS_AVAILABLE = True
except ImportError:
    CAMEL_TOOLS_AVAILABLE = False
    logging.warning("CAMeL Tools not available. Using fallback implementation.")

class TransliterationMapper:
    """
    Main class for handling transliteration from Arabic chat to Arabica system.
    """
    
    def __init__(self, custom_mapping_path: Optional[str] = None):
        """
        Initialize the mapper with the appropriate character mappings.
        
        Args:
            custom_mapping_path: Path to custom mapping files
        """
        self.logger = logging.getLogger(__name__)
        
        # Base mapping for Arabic chat to Arabica transliteration
        self.base_mapping = {
            # Numbers to Arabic letters
            '2': 'ʾ',  # hamza
            '3': 'ʿ',  # ayn
            '5': 'ḫ',  # kha
            '6': 'ṭ',  # emphatic ta (sometimes used)
            '7': 'ḥ',  # ha
            '8': 'q',  # qaf (alternative in some systems)
            '9': 'q',  # qaf
            
            # Capitalized letters for emphatics (example)
            'D': 'ḍ',  # emphatic d
            'S': 'ṣ',  # emphatic s
            'T': 'ṭ',  # emphatic t
            'Z': 'ẓ',  # emphatic z
            
            # Basic consonants
            'b': 'b',
            'd': 'd',
            'f': 'f',
            'g': 'g',  # Used in Moroccan Arabic
            'h': 'h',
            'j': 'ǧ',
            'k': 'k',
            'l': 'l',
            'm': 'm',
            'n': 'n',
            'r': 'r',
            's': 's',
            't': 't',
            'w': 'w',
            'y': 'y',
            'z': 'z',
        }
        
        # Multi-character sequences
        self.digraphs = [
            ('ch', 'š'),
            ('sh', 'š'),
            ('th', 'ṯ'),
            ('dh', 'ḏ'),
            ('gh', 'ġ'),
            ('kh', 'ḫ'),
        ]
        
        # Vowels
        self.vowels = [
            ('aa', 'ā'),
            ('ee', 'ī'),
            ('ii', 'ī'),
            ('oo', 'ū'),
            ('uu', 'ū'),
            ('a', 'a'),
            ('i', 'i'),
            ('u', 'u'),
            ('e', 'e'),  # For dialectal usage
            ('o', 'o'),  # For dialectal usage
        ]
        
        # Load dialect-specific mappings
        self.dialect_mappings = {}
        self._load_dialect_mappings(custom_mapping_path)
        
        # Initialize CAMeL Tools if available
        if CAMEL_TOOLS_AVAILABLE:
            self._init_camel_tools()
    
    def _init_camel_tools(self):
        """Initialize CAMeL Tools components."""
        # This is a placeholder for now - we'll implement actual CAMeL Tools initialization
        # when we get to that phase of development
        self.logger.info("Initializing CAMeL Tools components")
        
    def _load_dialect_mappings(self, custom_path: Optional[str] = None):
        """
        Load dialect-specific mapping files.
        
        Args:
            custom_path: Path to custom mapping files
        """
        # Default paths
        default_path = os.path.join(os.path.dirname(__file__), 'mappings')
        
        # Use custom path if provided
        search_path = custom_path if custom_path else default_path
        
        # Create directory if it doesn't exist
        if not os.path.exists(search_path):
            os.makedirs(search_path)
            
            # Create default Moroccan mapping file
            moroccan_path = os.path.join(search_path, 'moroccan.json')
            with open(moroccan_path, 'w') as f:
                json.dump({
                    "name": "Moroccan Arabic",
                    "description": "Mapping for Moroccan Arabic dialect features",
                    "mappings": {
                        "g": "g",  # In Moroccan, qaf is often pronounced as g
                        "v": "v",  # For loan words in Moroccan
                        "p": "p"   # For loan words in Moroccan
                    },
                    "patterns": [
                        # Examples of Moroccan-specific patterns
                        {"pattern": "sh", "replacement": "š"},
                        {"pattern": "ch", "replacement": "š"}
                    ]
                }, f, indent=2)
        
        # Load all mapping files
        try:
            for filename in os.listdir(search_path):
                if filename.endswith('.json'):
                    dialect_name = filename.split('.')[0]
                    file_path = os.path.join(search_path, filename)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.dialect_mappings[dialect_name] = json.load(f)
                        self.logger.info(f"Loaded mapping for {dialect_name} dialect")
        except Exception as e:
            self.logger.error(f"Error loading dialect mappings: {str(e)}")
    
    def convert(self, text: str, dialect: str = 'moroccan') -> str:
        """
        Convert Arabic chat text to Arabica transliteration.
        
        Args:
            text: The Arabic chat text to convert
            dialect: The dialect to use for conversion
            
        Returns:
            The text converted to Arabica transliteration
        """
        if not text:
            return ""
            
        # If CAMeL Tools is available, use it for the conversion
        if CAMEL_TOOLS_AVAILABLE:
            return self._convert_with_camel(text, dialect)
        else:
            return self._convert_fallback(text, dialect)
    
    def _convert_with_camel(self, text: str, dialect: str) -> str:
        """
        Convert text using CAMeL Tools.
        
        This is a placeholder that will be implemented properly once we
        integrate CAMeL Tools in the next phase.
        """
        # For now, just use the fallback
        return self._convert_fallback(text, dialect)
    
    def _convert_fallback(self, text: str, dialect: str) -> str:
        """
        Fallback conversion method when CAMeL Tools is not available.
        
        Args:
            text: The Arabic chat text to convert
            dialect: The dialect to use for conversion
            
        Returns:
            The text converted to Arabica transliteration
        """
        # Process the text through various transformation stages
        
        # 1. Apply digraphs first (they should take precedence)
        for chat, arabica in self.digraphs:
            text = text.replace(chat, arabica)
        
        # 2. Apply dialect-specific patterns if available
        if dialect in self.dialect_mappings:
            patterns = self.dialect_mappings[dialect].get('patterns', [])
            for pattern_info in patterns:
                pattern = pattern_info.get('pattern', '')
                replacement = pattern_info.get('replacement', '')
                if pattern and replacement:
                    text = text.replace(pattern, replacement)
        
        # 3. Apply vowel mappings
        for chat, arabica in self.vowels:
            text = text.replace(chat, arabica)
        
        # 4. Apply single character mappings
        result = ""
        i = 0
        while i < len(text):
            char = text[i]
            if char in self.base_mapping:
                result += self.base_mapping[char]
            else:
                # Check dialect-specific mappings
                if (dialect in self.dialect_mappings and 
                    'mappings' in self.dialect_mappings[dialect] and
                    char in self.dialect_mappings[dialect]['mappings']):
                    result += self.dialect_mappings[dialect]['mappings'][char]
                else:
                    result += char
            i += 1
        
        # 5. Post-processing for specific Arabica rules
        
        # Handle definite article (al-)
        result = re.sub(r'\bal[ -]([a-zA-Z])', r'al-\1', result)
        
        # Handle taa marbutah
        result = re.sub(r'a_t\b', 'a', result)  # End of word
        result = re.sub(r'a_t ([\w])', r'at \1', result)  # Before a word (construct state)
        
        return result
