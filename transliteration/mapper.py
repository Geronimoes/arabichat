"""
Core transliteration functionality for converting Arabic chat to Arabica transliteration.
"""

import re
import os
import json
import logging
from typing import Dict, List, Optional, Tuple, Set, Any

# Try to import CAMeL Tools, but don't fail if not available
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
            
            # Emphatic consonants (lowercase only to avoid casing issues)
            'd': 'd',
            'D': 'ḍ',  # emphatic d when explicitly capitalized mid-word
            's': 's',
            'S': 'ṣ',  # emphatic s when explicitly capitalized mid-word
            't': 't',
            'T': 'ṭ',  # emphatic t when explicitly capitalized mid-word
            'z': 'z',
            'Z': 'ẓ',  # emphatic z when explicitly capitalized mid-word
            
            # Basic consonants
            'b': 'b',
            'f': 'f',
            'g': 'g',  # Used in Moroccan Arabic
            'h': 'h',
            'j': 'ǧ',
            'k': 'k',
            'l': 'l',
            'm': 'm',
            'n': 'n',
            'r': 'r',
            'w': 'w',
            'y': 'y',
        }
        }
        
        # Multi-character sequences
        self.digraphs = [
            ('ch', 'š'),
            ('Ch', 'Š'),  # Capitalized version
            ('sh', 'š'),
            ('Sh', 'Š'),  # Capitalized version
            ('th', 'ṯ'),
            ('Th', 'Ṯ'),  # Capitalized version
            ('dh', 'ḏ'),
            ('Dh', 'Ḏ'),  # Capitalized version
            ('gh', 'ġ'),
            ('Gh', 'Ġ'),  # Capitalized version
            ('kh', 'ḫ'),
            ('Kh', 'Ḫ'),  # Capitalized version
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
        
        # Common loanwords to preserve
        self.loanwords = [
            'café', 'projet', 'planning', 'normal', 'mais', 'pour', 'mon',
            'call', 'tired', 'week', 'weekend', 'email', 'internet', 'online',
            'smartphone', 'computer', 'taxi', 'bus', 'train'
        ]
        
        # Common French/English words pattern
        self.foreign_word_patterns = [
            r'\b[a-zA-Z]+[\-\'\s]',  # Words with apostrophes or hyphens
            r'\b[pv][a-z]+\b',  # Words starting with p or v (rare in Arabic)
        ]
        
        # Load dialect-specific mappings
        self.dialect_mappings = {}
        self.common_words = {}
        self.foreign_words = set()
        self._load_dialect_mappings(custom_mapping_path)
        self._load_common_words(custom_mapping_path)
        self._load_foreign_words(custom_mapping_path)
        
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
            try:
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
            except Exception as e:
                self.logger.warning(f"Could not create mapping directory: {str(e)}")
        
        # Load all mapping files
        try:
            for filename in os.listdir(search_path):
                if filename.endswith('.json') and filename not in ['common_words.json', 'foreign_words.json']:
                    dialect_name = filename.split('.')[0]
                    file_path = os.path.join(search_path, filename)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.dialect_mappings[dialect_name] = json.load(f)
                        self.logger.info(f"Loaded mapping for {dialect_name} dialect")
        except Exception as e:
            self.logger.error(f"Error loading dialect mappings: {str(e)}")

    def _load_common_words(self, custom_path: Optional[str] = None):
        """
        Load common words dictionary for more accurate transliteration.
        
        Args:
            custom_path: Path to custom mapping files
        """
        # Default paths
        default_path = os.path.join(os.path.dirname(__file__), 'mappings')
        
        # Use custom path if provided
        search_path = custom_path if custom_path else default_path
        
        # Path to common words file
        common_words_path = os.path.join(search_path, 'common_words.json')
        
        # Create the file if it doesn't exist
        if not os.path.exists(common_words_path):
            try:
                # Create a basic common words file
                with open(common_words_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        "description": "Common Moroccan Arabic words with correct Arabica transliteration",
                        "words": {
                            "salam": "salām",
                            "shukran": "šukran",
                            "inshallah": "inšāʾallāh",
                            "habibi": "ḥabībi"
                        }
                    }, f, indent=2, ensure_ascii=False)
                self.logger.info(f"Created default common words file at {common_words_path}")
            except Exception as e:
                self.logger.warning(f"Could not create common words file: {str(e)}")
                return
                
        # Load the common words
        try:
            with open(common_words_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.common_words = data.get("words", {})
                self.logger.info(f"Loaded {len(self.common_words)} common words")
        except Exception as e:
            self.logger.error(f"Error loading common words: {str(e)}")
            
    def _load_foreign_words(self, custom_path: Optional[str] = None):
        """
        Load foreign words list that should be preserved during transliteration.
        
        Args:
            custom_path: Path to custom mapping files
        """
        # Default paths
        default_path = os.path.join(os.path.dirname(__file__), 'mappings')
        
        # Use custom path if provided
        search_path = custom_path if custom_path else default_path
        
        # Path to foreign words file
        foreign_words_path = os.path.join(search_path, 'foreign_words.json')
        
        # Create the file if it doesn't exist
        if not os.path.exists(foreign_words_path):
            try:
                # Create a basic foreign words file
                with open(foreign_words_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        "description": "Common foreign words that should be preserved during transliteration",
                        "words": [
                            "café", "internet", "taxi", "bus", "email", "facebook",
                            "hotel", "restaurant", "airport", "project", "planning"
                        ]
                    }, f, indent=2, ensure_ascii=False)
                self.logger.info(f"Created default foreign words file at {foreign_words_path}")
            except Exception as e:
                self.logger.warning(f"Could not create foreign words file: {str(e)}")
                return
                
        # Load the foreign words
        try:
            with open(foreign_words_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.foreign_words = set(data.get("words", []))
                self.logger.info(f"Loaded {len(self.foreign_words)} foreign words")
        except Exception as e:
            self.logger.error(f"Error loading foreign words: {str(e)}")
    
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
            
        # Always use the fallback for now, CAMeL Tools integration will be added later
        # if CAMEL_TOOLS_AVAILABLE:
        #     return self._convert_with_camel(text, dialect)
        # else:
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
        
        # Split the text into words for word-level processing
        words = re.findall(r'\b\w+\b|\S+', text)
        result_words = []
        
        for word in words:
            # Check if it's a common word with a predefined transliteration
            word_lower = word.lower()
            if word_lower in self.common_words:
                # Apply capitalization if the original word was capitalized
                if word[0].isupper() and len(word) > 1:
                    result_words.append(self.common_words[word_lower].capitalize())
                else:
                    result_words.append(self.common_words[word_lower])
                continue
                
            # Check if it's a foreign word that should be preserved
            if word_lower in self.foreign_words or any(word_lower.startswith(f) for f in ['l\'', 'el-']):
                result_words.append(word)
                continue
                
            # Proceed with character-by-character transliteration
            processed_word = word
            
            # 1. Apply digraphs first (they should take precedence)
            for chat, arabica in self.digraphs:
                processed_word = processed_word.lower().replace(chat, arabica)
                # Also handle capitalized versions
                cap_chat = chat.capitalize()
                processed_word = processed_word.replace(cap_chat, arabica.capitalize())
            
            # 2. Apply dialect-specific patterns if available
            if dialect in self.dialect_mappings:
                patterns = self.dialect_mappings[dialect].get('patterns', [])
                for pattern_info in patterns:
                    pattern = pattern_info.get('pattern', '')
                    replacement = pattern_info.get('replacement', '')
                    if pattern and replacement:
                        processed_word = processed_word.replace(pattern, replacement)
            
            # 3. Apply vowel mappings
            for chat, arabica in self.vowels:
                processed_word = processed_word.replace(chat, arabica)
            
            # 4. Apply single character mappings
            result_chars = []
            i = 0
            while i < len(processed_word):
                char = processed_word[i]
                if char in self.base_mapping:
                    result_chars.append(self.base_mapping[char])
                else:
                    # Check dialect-specific mappings
                    if (dialect in self.dialect_mappings and 
                        'mappings' in self.dialect_mappings[dialect] and
                        char in self.dialect_mappings[dialect]['mappings']):
                        result_chars.append(self.dialect_mappings[dialect]['mappings'][char])
                    else:
                        result_chars.append(char)
                i += 1
            
            processed_word = ''.join(result_chars)
            result_words.append(processed_word)
        
        # Combine words back into text
        result = ' '.join(result_words)
        
        # 5. Post-processing for specific Arabica rules
        
        # Handle definite article (al-)
        result = re.sub(r'\bal[ -]([a-zA-Z])', r'al-\1', result)
        
        # Handle taa marbutah
        result = re.sub(r'a_t\b', 'a', result)  # End of word
        result = re.sub(r'a_t ([\w])', r'at \1', result)  # Before a word (construct state)
        
        # Preserve punctuation
        result = re.sub(r'([^\w\s])\s+([^\w\s])', r'\1\2', result)
        
        return result
