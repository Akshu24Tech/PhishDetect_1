from flask import Blueprint, render_template, request, jsonify
from app.models.detector import PhishingDetector
import base64
import io
from PIL import Image
import logging
from werkzeug.exceptions import BadRequest, InternalServerError

main = Blueprint('main', __name__)
detector = PhishingDetector()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Validate request
        if not request.is_json:
            raise BadRequest('Request must be JSON')
        
        data = request.get_json()
        if not data or 'image' not in data:
            raise BadRequest('No image data received')

        # Get the image data from the request
        image_data = data['image']
        
        try:
            # Handle both base64 with and without data URI prefix
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64 image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
        except Exception as e:
            logger.error(f"Error processing image data: {str(e)}")
            raise BadRequest('Invalid image format or corrupted image data')

        # Analyze the image
        try:
            result = detector.analyze_image(image)
            return jsonify(result)
        except Exception as e:
            logger.error(f"Error during image analysis: {str(e)}")
            raise InternalServerError('Error analyzing image')
    
    except BadRequest as e:
        logger.warning(f"Bad request: {str(e)}")
        return jsonify({'error': str(e)}), 400
    
    except InternalServerError as e:
        logger.error(f"Internal server error: {str(e)}")
        return jsonify({'error': 'An internal server error occurred'}), 500
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

# Error handlers
@main.errorhandler(400)
def handle_bad_request(e):
    return jsonify({'error': str(e)}), 400

@main.errorhandler(500)
def handle_internal_server_error(e):
    return jsonify({'error': 'An internal server error occurred'}), 500

