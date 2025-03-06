"""
LLM API integration module for Arabic chat transliteration.

This module provides integration with various LLM APIs for transliteration
of Arabic chat text to academic transliteration formats.
"""

import os
import json
import logging
import time
from enum import Enum
from typing import Dict, List, Optional, Union, Any, Tuple
import requests
from urllib.parse import urljoin

class LLMProvider(str, Enum):
    """Supported LLM API providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MISTRAL = "mistral"
    OPENROUTER = "openrouter"

class LLMFallbackTransliterator:
    """
    LLM fallback transliterator that uses various API providers to transliterate unknown words.
    """
    
    def __init__(
        self, 
        provider: LLMProvider = LLMProvider.OPENAI,
        api_key: Optional[str] = None, 
        model: Optional[str] = None,
        cache_file: str = "llm_cache.json"
    ):
        """
        Initialize the LLM fallback transliterator.
        
        Args:
            provider: LLM API provider to use
            api_key: API key (or use environment variable)
            model: Model to use (or use default for provider)
            cache_file: Path to cache file for API responses
        """
        self.logger = logging.getLogger(__name__)
        self.provider = provider
        self.api_key = api_key or self._get_api_key_for_provider(provider)
        self.model = model or self._get_default_model_for_provider(provider)
        self.cache_file = cache_file
        self.cache = self._load_cache()
        
        if not self.api_key:
            self.logger.warning(f"No API key provided for {provider}")
    
    def _get_api_key_for_provider(self, provider: LLMProvider) -> Optional[str]:
        """Get API key from environment variables based on provider."""
        env_var_map = {
            LLMProvider.OPENAI: "OPENAI_API_KEY",
            LLMProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
            LLMProvider.MISTRAL: "MISTRAL_API_KEY",
            LLMProvider.OPENROUTER: "OPENROUTER_API_KEY"
        }
        
        env_var = env_var_map.get(provider)
        return os.environ.get(env_var) if env_var else None
    
    def _get_default_model_for_provider(self, provider: LLMProvider) -> str:
        """Get default model for the specified provider."""
        default_models = {
            LLMProvider.OPENAI: "gpt-3.5-turbo",
            LLMProvider.ANTHROPIC: "claude-3-haiku-20240307",
            LLMProvider.MISTRAL: "mistral-small-latest",
            LLMProvider.OPENROUTER: "openai/gpt-3.5-turbo"
        }
        
        return default_models.get(provider, "")
    
    def _load_cache(self) -> Dict[str, str]:
        """Load cache from file."""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Error loading cache: {e}")
        return {}
    
    def _save_cache(self) -> None:
        """Save cache to file."""
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.warning(f"Error saving cache: {e}")
    
    def transliterate(
        self, 
        word: str, 
        context: Optional[str] = None, 
        max_retries: int = 3
    ) -> str:
        """
        Transliterate a word using the selected LLM API.
        
        Args:
            word: Word to transliterate
            context: Optional context to help with transliteration
            max_retries: Maximum number of retries on failure
            
        Returns:
            Transliterated word
        """
        if not self.api_key:
            self.logger.warning("API key not configured, cannot transliterate")
            return word
            
        # Check cache first
        cache_key = f"{word}_{context or ''}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Prepare the prompt
        prompt = self._create_transliteration_prompt(word, context)
        
        # Send to API with retries
        for attempt in range(max_retries):
            try:
                result = self._call_api(prompt)
                
                if result:
                    # Cache the result
                    self.cache[cache_key] = result
                    self._save_cache()
                    
                    return result
                    
            except Exception as e:
                self.logger.warning(f"API error (attempt {attempt+1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        # If all retries fail, return the original word
        return word
    
    def transliterate_text(
        self, 
        text: str,
        max_retries: int = 3
    ) -> str:
        """
        Transliterate entire text using the selected LLM API.
        
        Args:
            text: Complete text to transliterate
            max_retries: Maximum number of retries on failure
            
        Returns:
            Transliterated text
        """
        if not self.api_key:
            self.logger.warning("API key not configured, cannot transliterate")
            return text
            
        # Check cache first (though less likely to hit for full texts)
        cache_key = f"FULL_{text}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Prepare the prompt
        prompt = self._create_full_text_transliteration_prompt(text)
        
        # Send to API with retries
        for attempt in range(max_retries):
            try:
                result = self._call_api(prompt)
                
                if result:
                    # Cache the result
                    self.cache[cache_key] = result
                    self._save_cache()
                    
                    return result
                    
            except Exception as e:
                self.logger.warning(f"API error (attempt {attempt+1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        # If all retries fail, return the original text
        return text
    
    def bulk_transliterate(
        self, 
        words: List[str], 
        batch_size: int = 10
    ) -> Dict[str, str]:
        """
        Transliterate multiple words in batches.
        
        Args:
            words: List of words to transliterate
            batch_size: Number of words to process in one batch
            
        Returns:
            Dictionary mapping original words to transliterated words
        """
        if not self.api_key:
            self.logger.warning("API key not configured, cannot transliterate")
            return {word: word for word in words}
            
        results = {}
        
        # Process words in batches to reduce API calls
        for i in range(0, len(words), batch_size):
            batch = words[i:i+batch_size]
            
            # Check cache for each word
            uncached_words = [w for w in batch if w not in self.cache]
            
            if uncached_words:
                # Create a batch prompt
                prompt = self._create_batch_transliteration_prompt(uncached_words)
                
                try:
                    response_text = self._call_api(prompt)
                    
                    if response_text:
                        # Try to parse as JSON
                        try:
                            transliterations = json.loads(response_text)
                            
                            # Update cache with new results
                            for word, transliteration in transliterations.items():
                                if word in uncached_words:  # Ensure we only cache valid results
                                    self.cache[word] = transliteration
                            
                            self._save_cache()
                            
                        except json.JSONDecodeError:
                            self.logger.warning(f"Could not parse API response as JSON: {response_text}")
                
                except Exception as e:
                    self.logger.warning(f"API error in batch processing: {e}")
            
            # Add all results from cache
            for word in batch:
                results[word] = self.cache.get(word, word)
            
            # Rate limiting pause between batches
            if i + batch_size < len(words):
                time.sleep(1)
        
        return results
    
    def _create_transliteration_prompt(self, word: str, context: Optional[str] = None) -> str:
        """Create a prompt for single word transliteration."""
        prompt = (
            "You are an expert in Moroccan Arabic transliteration. "
            f"Convert this Moroccan Arabic chat word to the Arabica transliteration system: '{word}'"
        )
        
        if context:
            prompt += f"\n\nContext: {context}"
            
        prompt += (
            "\n\nFollow the Arabica transliteration system strictly, using proper diacritics. "
            "Respond with ONLY the transliterated word, nothing else."
        )
        
        return prompt
    
    def _create_batch_transliteration_prompt(self, words: List[str]) -> str:
        """Create a prompt for batch word transliteration."""
        prompt = (
            "You are an expert in Moroccan Arabic transliteration. "
            "Convert these Moroccan Arabic chat words to the Arabica transliteration system:\n\n"
        )
        
        for i, word in enumerate(words):
            prompt += f"{i+1}. {word}\n"
            
        prompt += (
            "\n\nFollow the Arabica transliteration system strictly, using proper diacritics. "
            "Respond with a JSON object mapping each word to its transliteration. "
            "For example: {\"salam\": \"salām\", \"shukran\": \"šukran\"}"
        )
        
        return prompt
    
    def _create_full_text_transliteration_prompt(self, text: str) -> str:
        """Create a prompt for full text transliteration."""
        prompt = (
            "You are an expert in Moroccan Arabic transliteration. "
            "Convert the following Moroccan Arabic chat text to the Arabica transliteration system:\n\n"
            f"\"{text}\"\n\n"
            "Follow these guidelines:\n"
            "1. Use the Arabica transliteration system with proper diacritics\n"
            "2. Preserve punctuation and spacing\n"
            "3. Keep French or English words unchanged\n"
            "4. Maintain sentence structure\n"
            "5. Return ONLY the transliterated text, no explanations\n"
            "6. Properly handle dialectal features of Moroccan Arabic"
        )
        
        return prompt
    
    def _call_api(self, prompt: str) -> str:
        """Call the appropriate API based on the selected provider."""
        if self.provider == LLMProvider.OPENAI:
            return self._call_openai_api(prompt)
        elif self.provider == LLMProvider.ANTHROPIC:
            return self._call_anthropic_api(prompt)
        elif self.provider == LLMProvider.MISTRAL:
            return self._call_mistral_api(prompt)
        elif self.provider == LLMProvider.OPENROUTER:
            return self._call_openrouter_api(prompt)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _call_openai_api(self, prompt: str) -> str:
        """Call the OpenAI API."""
        url = "https://api.openai.com/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a specialized Arabic transliteration assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 500
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"].strip()
    
    def _call_anthropic_api(self, prompt: str) -> str:
        """Call the Anthropic API."""
        url = "https://api.anthropic.com/v1/messages"
        
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 500
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        response_data = response.json()
        return response_data["content"][0]["text"].strip()
    
    def _call_mistral_api(self, prompt: str) -> str:
        """Call the Mistral AI API."""
        url = "https://api.mistral.ai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a specialized Arabic transliteration assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 500
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"].strip()
    
    def _call_openrouter_api(self, prompt: str) -> str:
        """Call the OpenRouter API."""
        url = "https://openrouter.ai/api/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://arabichat.app",  # Required by OpenRouter
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a specialized Arabic transliteration assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 500
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"].strip()

class ProviderModels:
    """Maintains lists of available models for each provider."""
    
    # These lists can be expanded as new models become available
    
    OPENAI_MODELS = [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o"
    ]
    
    ANTHROPIC_MODELS = [
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    ]
    
    MISTRAL_MODELS = [
        "mistral-tiny",
        "mistral-small",
        "mistral-medium",
        "mistral-large-latest"
    ]
    
    OPENROUTER_MODELS = [
        # OpenAI models
        "openai/gpt-3.5-turbo",
        "openai/gpt-4",
        "openai/gpt-4-turbo",
        # Anthropic models
        "anthropic/claude-3-opus-20240229",
        "anthropic/claude-3-sonnet-20240229",
        "anthropic/claude-3-haiku-20240307",
        # Mistral models
        "mistral/mistral-small-latest",
        "mistral/mistral-medium-latest",
        "mistral/mistral-large-latest"
    ]
    
    @classmethod
    def get_models_for_provider(cls, provider: LLMProvider) -> List[str]:
        """Get list of models for the specified provider."""
        if provider == LLMProvider.OPENAI:
            return cls.OPENAI_MODELS
        elif provider == LLMProvider.ANTHROPIC:
            return cls.ANTHROPIC_MODELS
        elif provider == LLMProvider.MISTRAL:
            return cls.MISTRAL_MODELS
        elif provider == LLMProvider.OPENROUTER:
            return cls.OPENROUTER_MODELS
        else:
            return []
