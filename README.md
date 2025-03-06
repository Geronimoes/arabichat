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

## How Conversion Works

### Current Approach (Without CAMeL Tools)

The current conversion process is a specialized "search and replace" system with several layers:

#### 1. Character Mapping Tables

The system maintains several mapping tables:

- **Single characters**: Maps individual characters like '3' → 'ʿ' (ayn) or '7' → 'ḥ' (ha)
- **Multi-character sequences**: Handles combinations like 'sh' → 'š' or 'kh' → 'ḫ'
- **Vowels**: Maps regular and long vowels (e.g., 'aa' → 'ā')
- **Dialect-specific mappings**: Special rules for Moroccan Arabic (like using 'g' for ق/qaf)

#### 2. Conversion Process

When you enter text like "mar7aba 3alaikum", the conversion happens in this order:

1. **Apply digraph replacements first**
   - Replace character combinations (like 'sh', 'kh') before single characters
   - This ensures 'sh' becomes 'š' rather than processing 's' and 'h' separately

2. **Apply dialect-specific patterns**
   - If Moroccan dialect is selected, apply any Moroccan-specific rules
   - For example, maintain 'g' when it represents ق in Moroccan Arabic

3. **Process vowel mappings**
   - Convert repeated vowels to their long forms (e.g., 'aa' → 'ā')
   - Handle other vowel patterns

4. **Convert remaining single characters**
   - Process any remaining characters one by one using the base mapping table
   - Characters without a mapping rule remain unchanged

5. **Post-processing**
   - Format the definite article properly (ensure it's "al-word" with hyphen)
   - Handle special cases like taa marbutah (ة) differently depending on position

#### Example of a Conversion

For the input "mar7aba al-3alam":

1. First pass: Finds and replaces `7` → `ḥ`
2. Second pass: Formats `al-` consistently
3. Third pass: Replaces `3` → `ʿ`
4. Result: "marḥaba al-ʿalam"

### Future CAMeL Tools Integration

When CAMeL Tools is integrated, the process will be more sophisticated:

1. Convert chat text to proper Arabic script
2. Apply morphological analysis to understand word structure
3. Convert from Arabic script to Arabica transliteration

This will provide more accurate results for complex texts while handling dialectal variations better.

## Contributing

Contributions are welcome! Please see [README-DEV.md](README-DEV.md) for development guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [CAMeL Tools](https://github.com/CAMeL-Lab/camel_tools) - The primary NLP toolkit used for Arabic language processing
- V. Van Renterghem (Inalco) - For the Arabica transliteration system documentation
