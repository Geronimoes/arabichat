# ArabiChat

A web application for converting Arabic chat language (Arabizi/Franco-Arabic) to formal academic transliteration using the Arabica system.

## Overview

ArabiChat is designed to help scholars and students working with Arabic dialectal data, particularly Moroccan Arabic. It converts informal Arabic chat text (Latin characters with numbers) to standardized academic transliteration following the Arabica system.

### Key Features

- Convert Arabic chat text to Arabica transliteration
- Specialized support for Moroccan Arabic dialectal features
- Dictionary-based approach for improved accuracy
- Automatic correction of common errors and inconsistencies
- Experimental Arabic script conversion
- Customizable character mappings
- Simple, easy-to-use web interface
- Automatic conversion on paste

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

# Install basic dependencies (without CAMeL Tools)
pip install -r requirements-minimal.txt

# Run the application
python app.py
```

### Installation Notes

#### CAMeL Tools Installation

CAMeL Tools provides advanced Arabic language processing capabilities, but it can be difficult to install on Windows due to C++ dependencies. The application provides a fallback implementation that works without CAMeL Tools.

If you want to use CAMeL Tools (recommended for production):

**Option 1: Use a Docker container**
- This is the simplest approach if you have Docker installed
- Instructions for Docker setup will be added soon

**Option 2: Install on Linux (or WSL)**
- CAMeL Tools installs more easily on Linux systems
- You can use Windows Subsystem for Linux (WSL) to create a Linux environment on Windows

**Option 3: Advanced Windows installation**
- Requires Visual Studio Build Tools with C++ workload
- May require additional configuration due to package dependencies
```
pip install camel-tools
```

Then open your browser to `http://localhost:5000`.

## Usage

1. Enter or paste your Arabic chat text into the input field
2. Select dialect options if needed
3. Click "Convert" to see the academic transliteration
4. Use the "Copy" button to copy the results to your clipboard

## Advanced Features

### Fuzzy Matching with RapidFuzz

ArabiChat uses fuzzy string matching to handle variations in spelling and typos, making the conversion more robust. This allows for:

- Handling common misspellings
- Supporting different ways of writing the same word
- Detecting close matches when exact matches aren't found

### Arabic Text Processing with PyArabic

The application leverages PyArabic for improved handling of Arabic text:

- Arabic text normalization
- Character-specific handling
- Improved Arabic script rendering

### Future Enhancements

We plan to add these features in upcoming releases:

1. Integration with CAMeL Tools for users who can install it
2. Advanced morphological analysis
3. Better handling of dialectal variations

## Integration with Other Systems

### CAMeL Tools (Optional)

For advanced users who can install CAMeL Tools, the application can use its capabilities to:

1. Perform morphological analysis
2. Handle dialectal variations better
3. Convert from Arabic script to Arabica transliteration

This will provide more accurate results for complex texts while handling dialectal variations better.

## Known Issues and Troubleshooting

### RapidFuzz API

If you encounter errors related to RapidFuzz, it might be due to API changes between versions. The code should handle both older and newer API formats, but if you encounter issues:

```
pip install --upgrade rapidfuzz==3.6.1
```

### PyArabic Functions

Some implementations reference functions that might not be available in the current PyArabic version. The code includes fallbacks, but for best results:

```
pip install --upgrade pyarabic==0.6.15
```

### Basic Testing

To test basic functionality without relying on advanced features:

```bash
python test_basic.py
```

## Contributing

Contributions are welcome! Please see [README-DEV.md](README-DEV.md) for development guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [CAMeL Tools](https://github.com/CAMeL-Lab/camel_tools) - The primary NLP toolkit used for Arabic language processing
- [PyArabic](https://github.com/linuxscout/pyarabic) - Arabic language utilities for Python
- [RapidFuzz](https://github.com/maxbachmann/rapidfuzz) - Rapid fuzzy string matching library
- V. Van Renterghem (Inalco) - For the Arabica transliteration system documentation
