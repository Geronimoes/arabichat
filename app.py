"""
ArabiChat - A web application for Arabic chat to academic transliteration conversion.
"""

from flask import Flask, render_template, request, jsonify
import os
import logging
from datetime import datetime
from transliteration.mapper import TransliterationMapper

# Import Arabic script conversion (experimental)
try:
    from transliteration.arabic_script import to_arabic_script
    ARABIC_SCRIPT_AVAILABLE = True
except ImportError:
    ARABIC_SCRIPT_AVAILABLE = False
    logging.warning("Arabic script conversion not available.")

# Configure logging
logging.basicConfig(
    level=logging.WARNING,  # Only show warnings and errors in production
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize transliteration mapper
mapper = TransliterationMapper()

@app.route('/')
def index():
    """Render the main application page."""
    return render_template('index.html', current_year=datetime.now().year)

@app.route('/convert', methods=['POST'])
def convert():
    """
    Convert Arabic chat text to academic transliteration.
    
    Returns:
        JSON response with converted text
    """
    data = request.json
    text = data.get('text', '')
    dialect = data.get('dialect', 'moroccan')
    
    try:
        result = mapper.convert(text, dialect=dialect)
        
        # Add Arabic script conversion if available
        arabic_script = None
        if ARABIC_SCRIPT_AVAILABLE:
            try:
                arabic_script = to_arabic_script(result)
            except Exception as e:
                app.logger.warning(f"Arabic script conversion error: {str(e)}")
                
        return jsonify({
            'status': 'success',
            'result': result,
            'arabic_script': arabic_script
        })
    except Exception as e:
        app.logger.error(f"Conversion error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@app.route('/help')
def help_page():
    """Render the help documentation page."""
    return render_template('help.html', current_year=datetime.now().year)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
