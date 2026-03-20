from flask import Flask, request, jsonify
from flask_cors import CORS
import prediction
import resume_parser
import chatbot
import os
import json
from werkzeug.utils import secure_filename
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = os.urandom(24).hex()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def home():
    """Root endpoint with API info"""
    return jsonify({
        "name": "CareerBuddy AI API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/api/health [GET]",
            "predict": "/api/predict [POST]",
            "chat": "/api/chat [POST]",
            "parse_resume": "/api/parse-resume [POST]",
            "linkedin_jobs": "/api/linkedin-jobs [POST]"
        },
        "documentation": "See README.md for more details"
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "CareerBuddy API is running",
        "groq_api_configured": bool(os.getenv("GROQ_API_KEY"))
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict job titles based on skills and role"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        skills = data.get('skills', '')
        role = data.get('role', '')
        
        if not skills:
            return jsonify({"error": "Skills are required"}), 400
        
        input_text = f"{role} {skills}" if role else skills
        
        # Get predictions
        predictions = prediction.predict_job_titles(input_text)
        
        # Enhance predictions with LinkedIn links
        enhanced_predictions = []
        for title, confidence in predictions:
            linkedin_links = prediction.get_linkedin_job_links(title, num_links=3)
            enhanced_predictions.append({
                "title": title.title(),
                "confidence": float(confidence),
                "linkedin_links": linkedin_links
            })
        
        return jsonify({
            "success": True,
            "predictions": enhanced_predictions,
            "input": {"skills": skills, "role": role}
        })
    except Exception as e:
        app.logger.error(f"Prediction error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/parse-resume', methods=['POST'])
def parse_resume():
    """Parse resume and extract skills"""
    try:
        if 'resume' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"error": "Only PDF files are allowed"}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse resume
        result = resume_parser.parse_resume(filepath)
        
        # Clean up temp file
        try:
            os.remove(filepath)
        except:
            pass
        
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Resume parsing error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Get chatbot response"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        # Check if Groq API key is configured
        if not os.getenv("GROQ_API_KEY"):
            return jsonify({
                "success": False,
                "responses": [{
                    "type": "text",
                    "content": "Groq API key is not configured. Please set GROQ_API_KEY in .env file."
                }]
            }), 200
        
        responses = chatbot.get_chatbot_response(query)
        
        return jsonify({
            "success": True,
            "responses": responses,
            "query": query
        })
    except Exception as e:
        app.logger.error(f"Chat error: {str(e)}")
        return jsonify({
            "success": False,
            "responses": [{
                "type": "text",
                "content": f"Error: {str(e)}"
            }]
        }), 200

@app.route('/api/linkedin-jobs', methods=['POST'])
def get_linkedin_jobs():
    """Fetch LinkedIn job links"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        job_title = data.get('job_title', '')
        num_links = data.get('num_links', 5)
        
        if not job_title:
            return jsonify({"error": "Job title is required"}), 400
        
        links = prediction.get_linkedin_job_links(job_title, num_links)
        
        return jsonify({
            "success": True,
            "links": links,
            "job_title": job_title
        })
    except Exception as e:
        app.logger.error(f"LinkedIn jobs error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Train model if not exists
    model_path = os.path.join(os.path.dirname(__file__), prediction.MODEL_FILENAME)
    if not os.path.exists(model_path):
        print("🔄 Training model...")
        prediction.train_model()
    
    # Check Groq API key
    if not os.getenv("GROQ_API_KEY"):
        print("⚠️  Warning: GROQ_API_KEY not found in .env file")
        print("   Chatbot will use fallback responses")
    else:
        print("✅ Groq API key found")
    
    print("\n🚀 CareerBuddy API Server")
    print("=" * 50)
    print(f"📍 Server: http://127.0.0.1:5000")
    print(f"📚 API Docs: http://127.0.0.1:5000/")
    print("=" * 50)
    
    app.run(debug=True, port=5000, host='0.0.0.0')