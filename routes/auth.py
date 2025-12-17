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

            session.permanent = True
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
        
        new_id = result[0]['id'] if result else None
        
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
    
    # ============================================
# GET ADMIN PROFILE
# ============================================
@auth_bp.route('/api/auth/profile', methods=['GET'])
def get_profile():


    # DEBUG: Print session contents
    print("=== DEBUG SESSION ===")
    print(f"Session contents: {dict(session)}")
    print(f"admin_id in session: {'admin_id' in session}")
    print("=====================")
    

    
    """Get current admin's profile"""
    if 'admin_id' not in session:
        return jsonify({"success": False, "error": "Not authenticated"}), 401
    
    try:
        query = """
            SELECT id, username, email, full_name, role, created_at 
            FROM admins WHERE id = %s
        """
        admins = execute_query(query, (session['admin_id'],))
        
        if not admins or len(admins) == 0:
            return jsonify({"success": False, "error": "Admin not found"}), 404
        
        admin = admins[0]
        
        return jsonify({
            "success": True,
            "data": {
                "id": admin['id'],
                "username": admin['username'],
                "email": admin['email'],
                "full_name": admin['full_name'],
                "role": admin['role'],
                "created_at": admin['created_at'].isoformat() if admin['created_at'] else None
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# UPDATE ADMIN PROFILE
# ============================================
@auth_bp.route('/api/auth/profile', methods=['PUT'])
def update_profile():
    """Update current admin's profile"""
    if 'admin_id' not in session:
        return jsonify({"success": False, "error": "Not authenticated"}), 401
    
    try:
        data = request.get_json()
        
        full_name = data.get('full_name')
        email = data.get('email')
        
        if not full_name:
            return jsonify({"success": False, "error": "Full name is required"}), 400
        
        if not email:
            return jsonify({"success": False, "error": "Email is required"}), 400
        
        # Check if email is already used by another admin
        existing = execute_query(
            "SELECT id FROM admins WHERE email = %s AND id != %s",
            (email, session['admin_id'])
        )
        if existing and len(existing) > 0:
            return jsonify({"success": False, "error": "Email already in use"}), 400
        
        # Update profile
        query = """
            UPDATE admins 
            SET full_name = %s, email = %s
            WHERE id = %s
        """
        execute_query(query, (full_name, email, session['admin_id']), fetch=False)
        
        # Update session
        session['full_name'] = full_name
        session['email'] = email
        
        return jsonify({
            "success": True,
            "message": "Profile updated successfully"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# CHANGE PASSWORD
# ============================================
@auth_bp.route('/api/auth/password', methods=['PUT'])
def change_password():
    """Change current admin's password"""
    if 'admin_id' not in session:
        return jsonify({"success": False, "error": "Not authenticated"}), 401
    
    try:
        data = request.get_json()
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        # Validate inputs
        if not current_password:
            return jsonify({"success": False, "error": "Current password is required"}), 400
        
        if not new_password:
            return jsonify({"success": False, "error": "New password is required"}), 400
        
        if len(new_password) < 6:
            return jsonify({"success": False, "error": "New password must be at least 6 characters"}), 400
        
        if new_password != confirm_password:
            return jsonify({"success": False, "error": "Passwords do not match"}), 400
        
        # Get current admin
        admin = execute_query(
            "SELECT password_hash FROM admins WHERE id = %s",
            (session['admin_id'],)
        )
        
        if not admin or len(admin) == 0:
            return jsonify({"success": False, "error": "Admin not found"}), 404
        
        # Verify current password
        if not bcrypt.checkpw(current_password.encode('utf-8'), admin[0]['password_hash'].encode('utf-8')):
            return jsonify({"success": False, "error": "Current password is incorrect"}), 400
        
        # Hash new password
        new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Update password
        execute_query(
            "UPDATE admins SET password_hash = %s WHERE id = %s",
            (new_hash, session['admin_id']),
            fetch=False
        )
        
        return jsonify({
            "success": True,
            "message": "Password changed successfully"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500