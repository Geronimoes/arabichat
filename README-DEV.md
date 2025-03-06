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

## Project Architecture

### Project Structure

```
arabichat/
├── app.py                  # Main application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── static/                 # Static assets (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/              # Jinja2 HTML templates
├── transliteration/        # Core transliteration functionality
│   ├── __init__.py
│   ├── mapper.py           # Character mapping logic
│   ├── moroccan.py         # Moroccan dialect specific rules
│   └── arabica.py          # Arabica transliteration system
└── tests/                  # Unit and integration tests
```

### Core Components

1. **Web Application Layer**
   - Flask-based web application
   - User interface for text input and display
   - Form handling and validation

2. **Transliteration Engine**
   - Integration with CAMeL Tools
   - Custom mapping rules for Arabica system
   - Dialect-specific processing

3. **Utility Services**
   - Configuration management
   - Logging and error handling
   - Export and file handling

## Key Libraries and Technologies

### Primary Technologies

- **Flask**: Web framework
- **CAMeL Tools**: Arabic language processing
- **Bootstrap**: Frontend UI components
- **jQuery**: DOM manipulation and AJAX

### Alternative/Complementary Libraries

- **PyArabic**: Alternative for basic Arabic text operations
- **ArabicTransliterator**: Could be used for specific transliteration tasks
- **arabizi**: Specific tools for Arabizi (Arabic chat) processing

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
