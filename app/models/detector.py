import tensorflow as tf
import numpy as np
from PIL import Image
import pytesseract
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input

class PhishingDetector:
    def __init__(self):
        # Load pre-trained ResNet model
        self.model = ResNet50(weights='imagenet', include_top=False)
        # Common legitimate domains for comparison
        self.legitimate_domains = ['facebook.com', 'google.com', 'amazon.com', 'apple.com']
    
    def extract_text(self, image):
        """Extract text from image using OCR"""
        text = pytesseract.image_to_string(image)
        return text
    
    def extract_features(self, image):
        """Extract visual features using ResNet50"""
        # Resize image to standard size
        image = image.resize((224, 224))
        # Convert to array and preprocess
        img_array = tf.keras.preprocessing.image.img_to_array(image)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        
        # Get features
        features = self.model.predict(img_array)
        return features
    
    def analyze_image(self, image):
        """Analyze the screenshot for potential phishing indicators"""
        # Extract text and features
        text = self.extract_text(image)
        features = self.extract_features(image)
        
        # Basic analysis (you would expand this)
        suspicious_indicators = []
        
        # Check for suspicious text patterns
        text_lower = text.lower()
        if 'login' in text_lower and not any(domain in text_lower for domain in self.legitimate_domains):
            suspicious_indicators.append("Unknown domain detected")
        
        if 'urgent' in text_lower or 'verify account' in text_lower:
            suspicious_indicators.append("Suspicious urgency language detected")
        
        # Add more sophisticated detection logic here
        
        return {
            'suspicious_indicators': suspicious_indicators,
            'risk_level': 'high' if suspicious_indicators else 'low',
            'extracted_text': text
        }