# ArabiChat

A web application for converting Arabic chat language (Arabizi/Franco-Arabic) to formal academic transliteration using the Arabica system.

## Overview

ArabiChat is designed to help scholars and students working with Arabic dialectal data, particularly Moroccan Arabic. It converts informal Arabic chat text (Latin characters with numbers) to standardized academic transliteration following the Arabica system.

### Key Features

- Convert Arabic chat text to Arabica transliteration
- Specialized support for Moroccan Arabic dialectal features
- Customizable character mappings
- Simple, easy-to-use web interface
- Batch processing capabilities

## Installation

### Prerequisites

- Python 3.8+
- pip

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/arabichat.git
cd arabichat

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Then open your browser to `http://localhost:5000`.

## Usage

1. Enter or paste your Arabic chat text into the input field
2. Select dialect options if needed
3. Click "Convert" to see the academic transliteration
4. Use the "Copy" button to copy the results to your clipboard

## Contributing

Contributions are welcome! Please see [README-DEV.md](README-DEV.md) for development guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [CAMeL Tools](https://github.com/CAMeL-Lab/camel_tools) - The primary NLP toolkit used for Arabic language processing
- V. Van Renterghem (Inalco) - For the Arabica transliteration system documentation
