"""
Core transliteration functionality for converting Arabic chat to Arabica transliteration.
"""

import re
import os
import json
import logging
from typing import Dict, List, Optional, Tuple, Set, Any

# Import the fuzzy matching module
try:
    from transliteration.fuzzy_match import FuzzyMatcher
    FUZZY_MATCHING_AVAILABLE = True
except ImportError:
    FUZZY_MATCHING_AVAILABLE = False
    logging.warning("Fuzzy matching module not available. Fuzzy matching will be disabled.")

# Import the Arabic utilities module
try:
    from transliteration.arabic_utils import ArabicProcessor
    ARABIC_UTILS_AVAILABLE = True
except ImportError:
    ARABIC_UTILS_AVAILABLE = False
    logging.warning("Arabic utilities module not available. Advanced Arabic processing will be disabled.")

# Import the correction module (if available)
try:
    from transliteration.corrections import TransliterationCorrector
    CORRECTIONS_AVAILABLE = True
except ImportError:
    CORRECTIONS_AVAILABLE = False
    logging.warning("Correction module not available. Skipping correction pass.")

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
    
    def __init__(self, custom_mapping_path: Optional[str] = None, fuzzy_threshold: int = 85):
        """
        Initialize the mapper with the appropriate character mappings.
        
        Args:
            custom_mapping_path: Path to custom mapping files
            fuzzy_threshold: Threshold for fuzzy matching (0-100)
        """
        self.logger = logging.getLogger(__name__)
        self.fuzzy_threshold = fuzzy_threshold
        
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
            
            # Basic consonants with regular and emphatic versions
            'd': 'd',
            'D': 'ḍ',  # emphatic d when explicitly capitalized mid-word
            's': 's',
            'S': 'ṣ',  # emphatic s when explicitly capitalized mid-word
            't': 't',
            'T': 'ṭ',  # emphatic t when explicitly capitalized mid-word
            'z': 'z',
            'Z': 'ẓ',  # emphatic z when explicitly capitalized mid-word
            
            # Other basic consonants
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
            
        # Initialize the corrector if available
        self.corrector = None
        if CORRECTIONS_AVAILABLE:
            self.corrector = TransliterationCorrector()
            self.logger.info("Initialized correction module")
            
        # Initialize the fuzzy matcher if available
        self.fuzzy_matcher = None
        if FUZZY_MATCHING_AVAILABLE:
            self.fuzzy_matcher = FuzzyMatcher(default_threshold=self.fuzzy_threshold)
            self.logger.info("Initialized fuzzy matching module")
            
        # Initialize the Arabic processor if available
        self.arabic_processor = None
        if ARABIC_UTILS_AVAILABLE:
            self.arabic_processor = ArabicProcessor()
            self.logger.info("Initialized Arabic processing module")
            
        # Arabic script mapping (for converting from Arabica to Arabic script)
        self.arabic_script_mapping = {
            'ʾ': 'ء',
            'ā': 'ا',
            'a': 'َ',
            'b': 'ب',
            't': 'ت',
            'ṯ': 'ث',
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
            'ū': 'و',
            'u': 'ُ',
            'y': 'ي',
            'ī': 'ي',
            'i': 'ِ',
            'g': 'ج', # Moroccan specific
            'e': 'ي', # Dialectal
            'o': 'و'  # Dialectal
        }
    
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
        #     result = self._convert_with_camel(text, dialect)
        # else:
        result = self._convert_fallback(text, dialect)
        
        # Apply corrections if available
        if self.corrector is not None:
            result = self.corrector.apply_corrections(result)
            
        return result
    
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
        if not text:
            return ""
            
        # Process by splitting into tokens (words and punctuation)
        tokens = re.findall(r'\b\w+\b|\S|\s+', text)
        result_tokens = []
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # Skip whitespace tokens
            if token.isspace():
                result_tokens.append(token)
                i += 1
                continue
                
            # Check if it's a word (not punctuation)
            if re.match(r'\w+', token):
                # Check if it's a common word with a predefined transliteration
                token_lower = token.lower()
                if token_lower in self.common_words:
                    # Use the predefined transliteration
                    transliteration = self.common_words[token_lower]
                    # Preserve capitalization
                    if token[0].isupper() and len(transliteration) > 0:
                        transliteration = transliteration[0].upper() + transliteration[1:]
                    result_tokens.append(transliteration)
                    i += 1
                    continue
                
                # Try fuzzy matching if exact match fails
                if self.fuzzy_matcher is not None:
                    fuzzy_match, fuzzy_value, score = self.fuzzy_matcher.find_match(
                        token_lower, self.common_words
                    )
                    if fuzzy_value:
                        self.logger.debug(f"Fuzzy match: {token_lower} -> {fuzzy_match} (score: {score})")
                        # Preserve capitalization
                        if token[0].isupper() and len(fuzzy_value) > 0:
                            fuzzy_value = fuzzy_value[0].upper() + fuzzy_value[1:]
                        result_tokens.append(fuzzy_value)
                        i += 1
                        continue
                    
                # Check if it's a loanword to preserve
                if token_lower in self.loanwords or token_lower in self.foreign_words:
                    result_tokens.append(token)
                    i += 1
                    continue
                    
                # Check if it matches foreign word patterns
                is_foreign = False
                for pattern in self.foreign_word_patterns:
                    if re.match(pattern, token):
                        is_foreign = True
                        break
                if is_foreign:
                    result_tokens.append(token)
                    i += 1
                    continue
                
                # Check if it's a special case like l'prix or l-prix
                if i < len(tokens) - 1 and token.lower() in ['l', 'el'] and tokens[i+1] in ["'", "-"]:
                    # French article or definite article with apostrophe/hyphen
                    result_tokens.append(token)
                    result_tokens.append(tokens[i+1])
                    i += 2
                    continue
                
                # Process the word character by character, with special handling for first letter
                processed_token = self._process_word(token, dialect)
                result_tokens.append(processed_token)
            else:
                # It's punctuation or something else, keep as is
                result_tokens.append(token)
                
            i += 1
        
        # Join the results
        result = ''.join(result_tokens)
        
        # Post-processing for specific Arabica rules
        
        # Handle definite article (al-)
        result = re.sub(r'\bal[ -]([a-zA-Z])', r'al-\1', result)
        
        # Handle taa marbutah
        result = re.sub(r'a_t\b', 'a', result)  # End of word
        result = re.sub(r'a_t ([\w])', r'at \1', result)  # Before a word (construct state)
        
        return result
        
    def _process_word(self, word: str, dialect: str) -> str:
        """
        Process a single word for transliteration.
        
        Args:
            word: The word to process
            dialect: The dialect to use
            
        Returns:
            The processed word
        """
        # Special case for first letter capitalization
        is_first_cap = word[0].isupper() if word else False
        
        # 1. Apply digraphs first (they should take precedence)
        # We need to handle capitalized digraphs specially
        processed = word
        for chat, arabica in self.digraphs:
            # Case-sensitive replacements for digraphs
            processed = processed.replace(chat, arabica)
        
        # 2. Apply dialect-specific patterns if available
        if dialect in self.dialect_mappings:
            patterns = self.dialect_mappings[dialect].get('patterns', [])
            for pattern_info in patterns:
                pattern = pattern_info.get('pattern', '')
                replacement = pattern_info.get('replacement', '')
                if pattern and replacement:
                    processed = processed.replace(pattern, replacement)
        
        # 3. Apply vowel mappings
        for chat, arabica in self.vowels:
            processed = processed.replace(chat, arabica)
        
        # 4. Apply single character mappings with special handling for first letter
        result = ""
        for i, char in enumerate(processed):
            # Special handling for capitalized first letter
            if i == 0 and is_first_cap:
                # Don't apply emphatic mapping to capitalized first letter
                # Instead, map to regular consonant and keep capitalized
                if char.lower() in ['s', 'd', 't', 'z']:
                    result += char.lower()
                elif char.lower() in self.base_mapping:
                    # Get mapping and preserve capitalization
                    mapped = self.base_mapping[char.lower()]
                    result += mapped.upper() if mapped.isalpha() else mapped
                else:
                    result += char
            # Regular mapping for all other characters
            elif char in self.base_mapping:
                result += self.base_mapping[char]
            # Dialect-specific mapping
            elif (dialect in self.dialect_mappings and 
                'mappings' in self.dialect_mappings[dialect] and 
                char in self.dialect_mappings[dialect]['mappings']):
                result += self.dialect_mappings[dialect]['mappings'][char]
            # No mapping, keep as is
            else:
                result += char
        
        # Re-capitalize first letter if needed
        if is_first_cap and result and not result[0].isupper() and result[0].isalpha():
            result = result[0].upper() + result[1:]
            
        return result
