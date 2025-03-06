"""
Fuzzy matching utility for finding close matches in dictionaries.

This module provides functions for fuzzy string matching using the rapidfuzz library,
which helps find dictionary entries that are similar to a given word even if they
don't match exactly.
"""

import logging
from typing import Dict, Any, Optional, List, Tuple

# Try to import rapidfuzz, but don't fail if not available
try:
    from rapidfuzz import fuzz, process
    RAPIDFUZZ_AVAILABLE = True
except ImportError:
    RAPIDFUZZ_AVAILABLE = False
    logging.warning("rapidfuzz not available. Fuzzy matching will be disabled.")

class FuzzyMatcher:
    """
    Provides fuzzy matching capabilities for dictionaries.
    """
    
    def __init__(self, default_threshold: int = 85):
        """
        Initialize the fuzzy matcher.
        
        Args:
            default_threshold: Default similarity threshold (0-100)
        """
        self.logger = logging.getLogger(__name__)
        self.default_threshold = default_threshold
        
        if not RAPIDFUZZ_AVAILABLE:
            self.logger.warning("FuzzyMatcher initialized but rapidfuzz is not available.")
    
    def find_match(self, word: str, dictionary: Dict[str, Any], 
                   threshold: Optional[int] = None) -> Tuple[Optional[str], Optional[Any], Optional[int]]:
        """
        Find the closest match for a word in a dictionary.
        
        Args:
            word: The word to look for
            dictionary: The dictionary to search in
            threshold: Optional similarity threshold (0-100)
            
        Returns:
            Tuple of (matched_key, matched_value, score) or (None, None, None) if no match
        """
        if not RAPIDFUZZ_AVAILABLE:
            self.logger.warning("Fuzzy matching attempted but rapidfuzz is not available.")
            return None, None, None
            
        if not word or not dictionary:
            return None, None, None
            
        threshold = threshold if threshold is not None else self.default_threshold
        
        try:
            # Find the closest match
            match = process.extractOne(
                word.lower(),
                list(dictionary.keys()),
                scorer=fuzz.ratio,
                score_cutoff=threshold
            )
            
            if match:
                matched_key, score = match
                return matched_key, dictionary[matched_key], score
            
            return None, None, None
            
        except Exception as e:
            self.logger.error(f"Error in fuzzy matching: {str(e)}")
            return None, None, None
    
    def find_multiple_matches(self, word: str, dictionary: Dict[str, Any], 
                             limit: int = 5, threshold: Optional[int] = None) -> List[Tuple[str, Any, int]]:
        """
        Find multiple potential matches for a word in a dictionary.
        
        Args:
            word: The word to look for
            dictionary: The dictionary to search in
            limit: Maximum number of matches to return
            threshold: Optional similarity threshold (0-100)
            
        Returns:
            List of tuples (matched_key, matched_value, score)
        """
        if not RAPIDFUZZ_AVAILABLE:
            self.logger.warning("Fuzzy matching attempted but rapidfuzz is not available.")
            return []
            
        if not word or not dictionary:
            return []
            
        threshold = threshold if threshold is not None else self.default_threshold
        
        try:
            # Find multiple matches
            matches = process.extract(
                word.lower(),
                list(dictionary.keys()),
                scorer=fuzz.ratio,
                score_cutoff=threshold,
                limit=limit
            )
            
            if matches:
                return [(key, dictionary[key], score) for key, score in matches]
            
            return []
            
        except Exception as e:
            self.logger.error(f"Error in fuzzy matching: {str(e)}")
            return []
    
    def get_top_match(self, word: str, dictionary: Dict[str, Any], 
                     threshold: Optional[int] = None) -> Optional[Any]:
        """
        Get only the value of the best match (convenience method).
        
        Args:
            word: The word to look for
            dictionary: The dictionary to search in
            threshold: Optional similarity threshold (0-100)
            
        Returns:
            The matched value or None if no match
        """
        _, value, _ = self.find_match(word, dictionary, threshold)
        return value
    
    def find_partial_token_match(self, word: str, dictionary: Dict[str, Any], 
                               threshold: Optional[int] = None) -> Optional[Any]:
        """
        Find match by comparing tokens (useful for phrases).
        
        Args:
            word: The word or phrase to look for
            dictionary: The dictionary to search in
            threshold: Optional similarity threshold (0-100)
            
        Returns:
            The matched value or None if no match
        """
        if not RAPIDFUZZ_AVAILABLE:
            self.logger.warning("Token fuzzy matching attempted but rapidfuzz is not available.")
            return None
            
        if not word or not dictionary:
            return None
            
        threshold = threshold if threshold is not None else self.default_threshold
        
        try:
            # Use token sort ratio for phrases
            match = process.extractOne(
                word.lower(),
                list(dictionary.keys()),
                scorer=fuzz.token_sort_ratio,
                score_cutoff=threshold
            )
            
            if match:
                matched_key, _ = match
                return dictionary[matched_key]
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error in token fuzzy matching: {str(e)}")
            return None
