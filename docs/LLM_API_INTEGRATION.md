# LLM API Integration for Arabic Chat Transliteration

This document evaluates the potential integration of Large Language Model (LLM) APIs like Anthropic, OpenAI, or Mistral as a fallback mechanism for transliterating unknown or ambiguous words in the ArabiChat system.

## Overview

The proposed approach would use LLM APIs as a fallback when the dictionary-based and rule-based approaches cannot confidently transliterate a word or phrase. This hybrid approach combines the efficiency and consistency of rule-based systems with the flexibility and contextual understanding of LLMs.

## Implementation Approach

### Basic Implementation

```python
import openai
import os
from typing import Dict, List, Optional
import time
import json

class LLMFallbackTransliterator:
    """
    LLM fallback transliterator that uses OpenAI API to transliterate unknown words.
    """
    
    def __init__(self, api_key: Optional[str] = None, cache_file: str = "llm_cache.json"):
        """
        Initialize the LLM fallback transliterator.
        
        Args:
            api_key: OpenAI API key (or use environment variable)
            cache_file: Path to cache file for API responses
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.cache_file = cache_file
        self.cache = self._load_cache()
        self.client = self._initialize_client()
        
    def _initialize_client(self):
        """Initialize the OpenAI client."""
        if not self.api_key:
            raise ValueError("API key is required")
        
        return openai.OpenAI(api_key=self.api_key)
    
    def _load_cache(self) -> Dict[str, str]:
        """Load cache from file."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading cache: {e}")
        return {}
    
    def _save_cache(self):
        """Save cache to file."""
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def transliterate(self, word: str, context: Optional[str] = None, max_retries: int = 3) -> str:
        """
        Transliterate a word using the OpenAI API.
        
        Args:
            word: Word to transliterate
            context: Optional context to help with transliteration
            max_retries: Maximum number of retries on failure
            
        Returns:
            Transliterated word
        """
        # Check cache first
        cache_key = f"{word}_{context or ''}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Prepare the prompt
        prompt = f"Convert this Moroccan Arabic chat word to the Arabica transliteration system: '{word}'"
        if context:
            prompt += f"\nContext: {context}"
        prompt += "\nRespond with ONLY the transliterated word, nothing else."
        
        # Send to API with retries
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4o",  # or another appropriate model
                    messages=[
                        {"role": "system", "content": "You are a specialized transliteration system for Moroccan Arabic (Darija) chat language to Arabica academic transliteration."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,  # Low temperature for more deterministic results
                    max_tokens=50     # Short response needed
                )
                
                result = response.choices[0].message.content.strip()
                
                # Cache the result
                self.cache[cache_key] = result
                self._save_cache()
                
                return result
                
            except Exception as e:
                print(f"API error (attempt {attempt+1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        # If all retries fail, return the original word
        return word
    
    def bulk_transliterate(self, words: List[str], batch_size: int = 10) -> Dict[str, str]:
        """
        Transliterate multiple words in batches.
        
        Args:
            words: List of words to transliterate
            batch_size: Number of words to process in one batch
            
        Returns:
            Dictionary mapping original words to transliterated words
        """
        results = {}
        
        # Process words in batches to reduce API calls
        for i in range(0, len(words), batch_size):
            batch = words[i:i+batch_size]
            
            # Check cache for each word
            uncached_words = [w for w in batch if w not in self.cache]
            
            if uncached_words:
                # Create a batch prompt
                prompt = "Transliterate these Moroccan Arabic chat words to the Arabica system:\n\n"
                for idx, word in enumerate(uncached_words):
                    prompt += f"{idx+1}. {word}\n"
                prompt += "\nRespond with a JSON object mapping each word to its transliteration."
                
                try:
                    response = self.client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a specialized transliteration system for Moroccan Arabic (Darija) chat language to Arabica academic transliteration."},
                            {"role": "user", "content": prompt}
                        ],
                        response_format={"type": "json_object"},
                        temperature=0.2
                    )
                    
                    # Parse JSON response
                    response_text = response.choices[0].message.content
                    transliterations = json.loads(response_text)
                    
                    # Update cache with new results
                    for word, transliteration in transliterations.items():
                        self.cache[word] = transliteration
                    
                    self._save_cache()
                    
                except Exception as e:
                    print(f"API error in batch processing: {e}")
            
            # Add all results from cache
            for word in batch:
                results[word] = self.cache.get(word, word)
            
            # Rate limiting pause between batches
            if i + batch_size < len(words):
                time.sleep(2)
        
        return results
```

### Integration with Existing System

```python
def transliterate_hybrid(text, dictionary, fallback_threshold=85):
    """
    Transliterate text using a hybrid approach:
    1. Dictionary lookup for exact matches
    2. Fuzzy matching for close matches
    3. LLM API fallback for unknown words
    
    Args:
        text: Text to transliterate
        dictionary: Dictionary of known words
        fallback_threshold: Threshold for fuzzy matching
        
    Returns:
        Transliterated text
    """
    from rapidfuzz import process, fuzz
    
    words = text.split()
    result = []
    unknown_words = []

    # First pass: Dictionary and fuzzy matching
    for word in words:
        word_lower = word.lower()
        
        # Exact dictionary match
        if word_lower in dictionary:
            result.append(dictionary[word_lower])
            continue
            
        # Fuzzy matching
        match = process.extractOne(
            word_lower,
            dictionary.keys(),
            scorer=fuzz.ratio,
            score_cutoff=fallback_threshold
        )
        
        if match:
            # Found a close match
            result.append(dictionary[match[0]])
        else:
            # No match found, mark for LLM processing
            result.append(f"__UNKNOWN__{word}__")
            unknown_words.append(word)
    
    # Second pass: LLM API for unknown words
    if unknown_words and LLM_FALLBACK_ENABLED:
        try:
            llm_translator = LLMFallbackTransliterator()
            translations = llm_translator.bulk_transliterate(unknown_words)
            
            # Replace unknown placeholders with LLM results
            final_result = []
            for item in result:
                if item.startswith("__UNKNOWN__"):
                    word = item[11:-2]  # Extract original word
                    final_result.append(translations.get(word, word))
                else:
                    final_result.append(item)
            
            result = final_result
        except Exception as e:
            # If LLM fails, remove the placeholder markers
            result = [item.replace("__UNKNOWN__", "").replace("__", "") if item.startswith("__UNKNOWN__") else item for item in result]
            print(f"LLM fallback error: {e}")
    else:
        # If LLM disabled, remove the placeholder markers
        result = [item.replace("__UNKNOWN__", "").replace("__", "") if item.startswith("__UNKNOWN__") else item for item in result]
    
    return " ".join(result)
```

## Benefits

1. **Handling Unknown Words**:
   - Provides transliterations for words not in the dictionary
   - Adapts to new slang or regional expressions

2. **Context-Aware Processing**:
   - Can consider surrounding words for better disambiguation
   - Understands idiomatic expressions

3. **Continuous Improvement**:
   - API responses can be cached and later added to the dictionary
   - Builds knowledge over time

4. **Fallback Safety Net**:
   - Only used when rule-based approaches fail
   - Ensures coverage of edge cases

## Challenges and Mitigations

| Challenge | Mitigation Strategy |
|-----------|---------------------|
| **API Costs** | - Use as last resort fallback<br>- Implement robust caching<br>- Batch processing for efficiency<br>- Make LLM usage configurable (on/off) |
| **Latency** | - Asynchronous processing for batch requests<br>- Aggressive caching<br>- Progress indicators for users |
| **Reliability** | - Implement retries with exponential backoff<br>- Graceful fallback to original text<br>- Error logging and monitoring |
| **Consistency** | - Use low temperature settings (0.1-0.3)<br>- Provide system prompt with examples<br>- Post-process responses for standardization |
| **Security** | - Store API keys in environment variables<br>- Rate limiting to prevent abuse<br>- No sensitive data transmission |

## Implementation Requirements

1. **API Access**:
   - OpenAI, Anthropic, or Mistral API key
   - Environment variable configuration
   - Rate limits consideration

2. **Caching System**:
   - JSON-based file cache
   - Database integration for production
   - TTL (time-to-live) for cache entries

3. **Configuration**:
   - Enable/disable LLM fallback
   - Confidence threshold settings
   - API provider selection
   - Rate limiting controls

4. **Monitoring**:
   - Usage tracking
   - Error logging
   - Performance metrics

## Cost Analysis

Assuming GPT-4 API usage:

- Input: ~$0.01 per 1K tokens
- Output: ~$0.03 per 1K tokens
- Average word: ~1.5 tokens

For 1,000 unknown words per day:
- Estimated daily cost: ~$0.06 (with batching)
- Monthly cost: ~$1.80

With caching, costs would decrease over time as the system learns more words.

## Phased Implementation Plan

### Phase 1: Basic Integration
- Implement simple API client with caching
- Add configuration toggle
- Test with small set of unknown words

### Phase 2: Enhanced Features
- Add batch processing
- Implement context-aware requests
- Add feedback mechanism for incorrect transliterations

### Phase 3: Learning System
- Create process to periodically review cached responses
- Add approved responses to dictionary
- Implement continuous improvement workflow

## Conclusion

The LLM API integration provides a powerful fallback mechanism for handling unknown words in Arabic chat transliteration. By implementing it as a configurable option with robust caching and error handling, we can balance accuracy, performance, and cost considerations.

The hybrid approach leverages the strengths of both rule-based and AI-driven systems, ensuring consistent results for known patterns while providing flexibility for novel expressions.
