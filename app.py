"""
ArabiChat - A web application for Arabic chat to academic transliteration conversion.
"""

from flask import Flask, render_template, request, jsonify
import os
from transliteration.mapper import TransliterationMapper

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize transliteration mapper
mapper = TransliterationMapper()

@app.route('/')
def index():
    """Render the main application page."""
    return render_template('index.html')

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
        return jsonify({
            'status': 'success',
            'result': result
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
    return render_template('help.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
