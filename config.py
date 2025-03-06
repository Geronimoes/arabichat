"""
Configuration settings for the ArabiChat application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-development-only')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Application settings
    DEFAULT_DIALECT = 'moroccan'
    
    # Transliteration settings
    CUSTOM_MAPPING_PATH = os.environ.get(
        'CUSTOM_MAPPING_PATH', 
        os.path.join(os.path.dirname(__file__), 'transliteration', 'mappings')
    )

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
# Set the active configuration based on environment
if os.environ.get('FLASK_ENV') == 'production':
    ActiveConfig = ProductionConfig
else:
    ActiveConfig = DevelopmentConfig
