from flask import Flask, request, jsonify, send_from_directory
from summarizers import summarize_text
import logging
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="huggingface_hub.file_download")
# Set up logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='static')  # Serves files from backend/static/

@app.route('/')
def index():
    """Serve the main HTML page."""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    """API endpoint for summarization."""
    try:
        # Parse JSON from frontend
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided.'}), 400

        text = data.get('text', '').strip()
        mode = data.get('mode', 'abstractive').lower()
        length = data.get('length')  # Integer for extractive; ignored for abstractive

        # Server-side validation (reinforces frontend checks)
        if not text:
            return jsonify({'error': 'Text is required.'}), 400
        if len(text) > 2000:
            return jsonify({'error': 'Text exceeds 2000 characters. Please shorten it.'}), 400
        if mode not in ['abstractive', 'extractive']:
            return jsonify({'error': 'Invalid mode. Use "abstractive" or "extractive".'}), 400
        if mode == 'extractive' and (not isinstance(length, int) or length < 1 or length > 10):
            return jsonify({'error': 'Length must be an integer between 1 and 10 for extractive mode.'}), 400

        logger.info(f"Summarizing text of length {len(text)} in {mode} mode.")

        # Generate summary
        summary = summarize_text(text, mode, length)

        return jsonify({'summary': summary})

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        logger.error(f"Summarization error: {e}")
        return jsonify({'error': 'Internal server error. Please try again.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # debug=True for development; set False in production