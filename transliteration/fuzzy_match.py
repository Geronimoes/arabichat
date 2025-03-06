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
            result = process.extractOne(
                word.lower(),
                list(dictionary.keys()),
                scorer=fuzz.ratio,
                score_cutoff=threshold
            )
            
            if result is not None:
                # Different versions of rapidfuzz return different formats
                
                # Handle 3-element tuple (match, score, index)
                if isinstance(result, tuple) and len(result) == 3:
                    matched_key, score, _ = result
                    return matched_key, dictionary[matched_key], score
                    
                # Handle 2-element tuple (match, score)
                elif isinstance(result, tuple) and len(result) == 2:
                    matched_key, score = result
                    return matched_key, dictionary[matched_key], score
                    
                # Handle Match object
                elif hasattr(result, 'match') and hasattr(result, 'score'):
                    matched_key = result.match
                    score = result.score
                    return matched_key, dictionary[matched_key], score
                
                # Log unexpected format and try to extract what we can
                else:
                    self.logger.warning(f"Unexpected result format from rapidfuzz: {result}")
                    # Try to extract information in a best-effort way
                    if isinstance(result, tuple) and len(result) > 0:
                        matched_key = result[0]
                        if isinstance(matched_key, str) and matched_key in dictionary:
                            return matched_key, dictionary[matched_key], 0
                    return None, None, None
            
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
            results = process.extract(
                word.lower(),
                list(dictionary.keys()),
                scorer=fuzz.ratio,
                score_cutoff=threshold,
                limit=limit
            )
            
            if results:
                # Handle different return formats based on rapidfuzz version
                matched_results = []
                
                for result in results:
                    # Handle 3-element tuple (key, score, index)
                    if isinstance(result, tuple) and len(result) == 3:
                        key, score, _ = result
                        if key in dictionary:
                            matched_results.append((key, dictionary[key], score))
                    # Handle 2-element tuple (key, score) format
                    elif isinstance(result, tuple) and len(result) == 2:
                        key, score = result
                        if key in dictionary:
                            matched_results.append((key, dictionary[key], score))
                    # Handle Match object format
                    elif hasattr(result, 'match') and hasattr(result, 'score'):
                        key = result.match
                        score = result.score
                        if key in dictionary:
                            matched_results.append((key, dictionary[key], score))
                    # Try to handle other formats
                    elif isinstance(result, tuple) and len(result) > 0:
                        key = result[0]
                        if isinstance(key, str) and key in dictionary:
                            matched_results.append((key, dictionary[key], 0))
                    
                return matched_results
            
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
            
        # Simple implementation that's more robust
        best_score = 0
        best_match = None
        word_lower = word.lower()
        
        # Use regular ratio comparison but compare with all keys
        for key in dictionary.keys():
            score = fuzz.ratio(word_lower, key.lower())
            if score > best_score and score >= (threshold or self.default_threshold):
                best_score = score
                best_match = key
                
        if best_match:
            return dictionary[best_match]
            
        return None
