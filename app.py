from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Enable CORS (allows React to connect)
CORS(app)

# Basic test route
@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple endpoint to test if API is running"""
    return jsonify({
        "status": "healthy",
        "message": "Youths4Change API is running!"
    })

# Test database route
@app.route('/api/test-db', methods=['GET'])
def test_db():
    """Test database connection"""
    from config.database import execute_query
    
    try:
        projects = execute_query("SELECT COUNT(*) as count FROM projects")
        count = projects[0]['count']
        
        return jsonify({
            "success": True,
            "message": f"Database connected! Found {count} projects."
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)