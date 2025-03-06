# ArabiChat Developer Documentation

This document provides information for developers contributing to the ArabiChat project.

## Development Environment Setup

### Prerequisites

- Python 3.8+
- Git
- A text editor or IDE (VS Code recommended)

### Setting Up Your Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/arabichat.git
   cd arabichat
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Additional dependencies for development
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

5. Run the development server:
   ```bash
   flask run --debug
   ```

### Using Docker for Development

Docker provides a consistent environment with all dependencies pre-installed, including CAMeL Tools.

1. Build and start the Docker container:
   ```bash
   docker-compose up --build
   ```

2. For development with live reload:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
   ```

The application will be available at http://localhost:5000.

## Project Architecture

### Project Structure

```
arabichat/
├── app.py                  # Main application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Production dependencies
├── requirements-minimal.txt # Dependencies without CAMeL Tools
├── requirements-dev.txt    # Development dependencies
├── static/                 # Static assets (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/              # Jinja2 HTML templates
├── transliteration/        # Core transliteration functionality
│   ├── __init__.py
│   ├── mapper.py           # Character mapping logic
│   ├── corrections.py      # Post-processing corrections
│   ├── arabic_script.py    # Experimental Arabic script conversion
│   ├── moroccan.py         # Moroccan dialect specific rules
│   ├── mappings/           # JSON mapping files
│   │   ├── moroccan.json   # Moroccan dialect mappings
│   │   ├── common_words.json # Dictionary of common words
│   │   └── foreign_words.json # List of words to preserve
│   └── corrections/        # Correction files
│       ├── word_corrections.json
│       ├── pattern_corrections.json
│       └── suffix_corrections.json
└── tests/                  # Unit and integration tests
```

### Core Components

1. **Web Application Layer**
   - Flask-based web application
   - User interface for text input and display
   - Form handling and validation
   - Automatic conversion on paste

2. **Transliteration Engine**
   - Character mapping system
   - Dictionary-based approach for common words
   - Customizable mapping rules
   - Pattern-based conversion for special cases

3. **Correction System**
   - Post-processing corrections for common errors
   - Word-level, pattern-based, and suffix-based corrections
   - Configurable via JSON files

4. **Arabic Script Conversion**
   - Experimental feature for converting Arabica to Arabic script
   - Basic character mapping and contextual rules

5. **Utility Services**
   - Configuration management
   - Logging and error handling
   - Export and file handling

## Key Libraries and Technologies

### Primary Technologies

- **Flask**: Web framework
- **Python**: Core programming language
- **JSON**: Configuration and data storage
- **Bootstrap**: Frontend UI components
- **jQuery**: DOM manipulation and AJAX

### Potential Additional Libraries

- **rapidfuzz**: Fuzzy string matching for dictionary lookups
- **pyarabic**: Arabic text processing utilities
- **NLTK/spaCy**: Natural language processing for morphological analysis
- **CAMeL Tools**: Advanced Arabic language processing (optional, requires C++ dependencies)

### Potential API Integration

- **OpenAI/Anthropic/Mistral API**: LLM fallback for unknown words

## CAMeL Tools Integration

CAMeL Tools is our primary Arabic language processing library. It provides:

1. **Dialectal Arabic Support**: Handles various Arabic dialects including Moroccan
2. **Text Normalization**: Standardizes text before processing
3. **Morphological Analysis**: Understands word structure
4. **Named Entity Recognition**: Identifies proper nouns

### Basic Usage Example

```python
from camel_tools.utils.charmap import CharMapper

# Create a mapper from Arabic chat to Arabic script
arabizi_mapper = CharMapper(
    map_path="path/to/mapping/file.json",
    reverse=False
)

# Convert text
arabic_text = arabizi_mapper.map("mar7aba")
```

## Testing

### Running Tests

```bash
pytest
```

### Test Structure

- Unit tests for individual components
- Integration tests for end-to-end functionality
- Test fixtures for common test data

## Contribution Guidelines

### Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them with descriptive messages:
   ```bash
   git commit -m "Add feature: description of the feature"
   ```

3. Push your changes and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

### Coding Standards

- Follow PEP 8 style guidelines
- Write docstrings for all functions and classes
- Include type hints
- Keep functions small and focused on a single task

### Documentation

- Update relevant documentation when adding or changing features
- Include examples for new functionality
- Document any non-obvious behavior or edge cases

## Performance Considerations

- CAMeL Tools can be resource-intensive for large text processing
- Consider implementing caching for frequently used mappings
- Use batch processing for large files
- Profile code to identify bottlenecks

## Resources

### Arabic Language Resources

- [Arabica Transliteration System Documentation](docs/arabica_system.pdf)
- [Arabic Chat Alphabet (Wikipedia)](https://en.wikipedia.org/wiki/Arabic_chat_alphabet)
- [Moroccan Arabic Features Guide](docs/moroccan_features.md)

### Technical Resources

- [CAMeL Tools Documentation](https://camel-tools.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)
