from flask import Flask, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv
import os
from routes.contact import contact_bp
from routes.settings import settings_bp




# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Secret key for sessions
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Enable CORS with credentials support (for sessions)
CORS(app, supports_credentials=True, origins=['http://localhost:5173', 'http://localhost:3000'])

# Import blueprints
from routes.projects import projects_bp
from routes.applications import applications_bp
from routes.donations import donations_bp
from routes.auth import auth_bp
from routes.analytics import analytics_bp


# Register blueprints
app.register_blueprint(projects_bp)
app.register_blueprint(applications_bp)
app.register_blueprint(donations_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(settings_bp)

# Basic test routes
@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple endpoint to test if API is running"""
    return jsonify({
        "status": "healthy",
        "message": "Youths4Change API is running!"
    })

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

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
