"""
FloatChat-AI Backend Server
A Flask-based API server for oceanographic data chatbot
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from services.ai_service import AIService
from services.data_service import DataService
from db.session import SessionLocal
from db.models import Base, ArgoRecord

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize services
data_service = DataService()
ai_service = AIService()

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "service": "FloatChat-AI API",
        "version": "1.0.0"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint that processes user messages and returns AI responses
    
    Request body:
    {
        "message": "What is the average temperature in the Indian Ocean?"
    }
    
    Response:
    {
        "reply": "Based on the ARGO data, the average temperature is..."
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' field"}), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Get relevant ARGO data based on the query
        context_data = data_service.get_relevant_context(user_message)
        
        # Generate AI response using the context
        ai_response = ai_service.generate_response(user_message, context_data)
        
        return jsonify({"reply": ai_response})
    
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500

@app.route('/api/data/stats', methods=['GET'])
def get_stats():
    """
    Get statistics about the ARGO dataset
    
    Returns:
    {
        "total_records": 1000,
        "floats": ["2902746"],
        "date_range": {"min": "2023-01-01", "max": "2023-12-31"},
        "depth_range": {"min": 0, "max": 2000},
        "temp_range": {"min": 10.5, "max": 30.2}
    }
    """
    try:
        stats = data_service.get_dataset_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/data/query', methods=['POST'])
def query_data():
    """
    Query ARGO data with filters
    
    Request body:
    {
        "min_depth": 0,
        "max_depth": 100,
        "min_temp": 20,
        "max_temp": 30,
        "limit": 100
    }
    """
    try:
        filters = request.get_json() or {}
        results = data_service.query_records(filters)
        return jsonify({"data": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Ensure database tables exist
    from db.session import engine
    Base.metadata.create_all(bind=engine)
    
    # Get configuration from environment
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"🌊 FloatChat-AI Server starting on http://{host}:{port}")
    print(f"🔍 Debug mode: {debug}")
    
    app.run(host=host, port=port, debug=debug)
