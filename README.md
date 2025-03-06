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

## Contributing

Contributions are welcome! Please see [README-DEV.md](README-DEV.md) for development guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [CAMeL Tools](https://github.com/CAMeL-Lab/camel_tools) - The primary NLP toolkit used for Arabic language processing
- V. Van Renterghem (Inalco) - For the Arabica transliteration system documentation
