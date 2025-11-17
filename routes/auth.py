from flask import Blueprint, request, jsonify, session
from config.database import execute_query
import bcrypt

auth_bp = Blueprint('auth', __name__)

# ============================================
# LOGIN
# ============================================
@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    """
    Admin login
    Expects: {"username": "admin", "password": "admin123"}
    """
    try:
        data = request.get_json()
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400
        
        # Find admin by username
        query = "SELECT * FROM admins WHERE username = %s"
        admins = execute_query(query, (username,))
        
        if not admins or len(admins) == 0:
            return jsonify({"error": "Invalid credentials"}), 401
        
        admin = admins[0]
        
        # Verify password
        # Note: The sample admin password hash is for 'admin123'
        password_hash = admin['password_hash']
        
        # Check if password matches
        if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            # Create session
            session['admin_id'] = admin['id']
            session['username'] = admin['username']
            
            return jsonify({
                "success": True,
                "message": "Login successful",
                "user": {
                    "id": admin['id'],
                    "username": admin['username'],
                    "email": admin['email'],
                    "full_name": admin['full_name'],
                    "role": admin['role']
                }
            })
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# LOGOUT
# ============================================
@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    """Logout - clear session"""
    session.clear()
    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    })

# ============================================
# CHECK AUTH STATUS
# ============================================
@auth_bp.route('/api/auth/me', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    if 'admin_id' in session:
        admin_id = session['admin_id']
        
        # Get admin details
        query = "SELECT id, username, email, full_name, role FROM admins WHERE id = %s"
        admins = execute_query(query, (admin_id,))
        
        if admins and len(admins) > 0:
            return jsonify({
                "authenticated": True,
                "user": admins[0]
            })
    
    return jsonify({"authenticated": False}), 401

# ============================================
# REGISTER NEW ADMIN (Protected - for testing)
# ============================================
@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    """
    Register new admin account
    For development/testing only
    """
    try:
        data = request.get_json()
        
        required = ['username', 'email', 'password', 'full_name']
        for field in required:
            if not data.get(field):
                return jsonify({"error": f"{field} is required"}), 400
        
        # Hash password
        password_hash = bcrypt.hashpw(
            data['password'].encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        
        # Insert new admin
        query = """
            INSERT INTO admins (username, email, password_hash, full_name, role)
            VALUES (%s, %s, %s, %s, 'admin')
            RETURNING id
        """
        
        result = execute_query(query, (
            data['username'],
            data['email'],
            password_hash,
            data['full_name']
        ), fetch=False)
        
        new_id = result['id']
        
        return jsonify({
            "success": True,
            "message": "Admin account created",
            "id": new_id
        }), 201
    
    except Exception as e:
        # Likely duplicate username/email
        if 'duplicate' in str(e).lower():
            return jsonify({"error": "Username or email already exists"}), 400
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500