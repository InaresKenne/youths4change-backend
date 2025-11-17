from flask import Blueprint, request, jsonify
from config.database import execute_query
import re

applications_bp = Blueprint('applications', __name__)

# ============================================
# GET ALL APPLICATIONS (with filters)
# ============================================
@applications_bp.route('/api/applications', methods=['GET'])
def get_all_applications():
    """
    Get all applications, optionally filtered
    Query params: ?status=pending&country=Ghana
    """
    try:
        status = request.args.get('status', '')
        country = request.args.get('country', '')
        
        query = "SELECT * FROM applications WHERE 1=1"
        params = []
        
        if status:
            query += " AND status = %s"
            params.append(status)
        
        if country:
            query += " AND country = %s"
            params.append(country)
        
        query += " ORDER BY applied_at DESC"
        
        applications = execute_query(query, tuple(params) if params else None)
        
        return jsonify({
            "success": True,
            "data": applications,
            "count": len(applications)
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# GET SINGLE APPLICATION
# ============================================
@applications_bp.route('/api/applications/<int:id>', methods=['GET'])
def get_application(id):
    """Get one application by ID"""
    try:
        query = "SELECT * FROM applications WHERE id = %s"
        applications = execute_query(query, (id,))
        
        if not applications or len(applications) == 0:
            return jsonify({
                "success": False,
                "error": "Application not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": applications[0]
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# CREATE APPLICATION (Submit)
# ============================================
@applications_bp.route('/api/applications', methods=['POST'])
def create_application():
    """
    Submit a new application
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['full_name', 'email', 'phone', 'country', 'motivation']
        for field in required:
            if not data.get(field):
                return jsonify({
                    "error": f"{field.replace('_', ' ').title()} is required"
                }), 400
        
        # Validate email format
        # email_pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6}$'
        # if not re.match(email_pattern, data['email']):
        #     return jsonify({"error": "Invalid email format"}), 400
        
        # Validate phone format (international)
        # phone_pattern = r'^\\+?[0-9]{10,15}$'
        # if not re.match(phone_pattern, data['phone']):
        #     return jsonify({"error": "Invalid phone format"}), 400
        
        # Validate name (letters and spaces only, 3-50 chars)
        # name_pattern = r'^[a-zA-Z\\s]{3,50}$'
        # if not re.match(name_pattern, data['full_name']):
        #     return jsonify({"error": "Invalid name format"}), 400
        
        # Validate motivation length (100-500 words)
        motivation = data['motivation'].strip()
        word_count = len(motivation.split())
        if word_count < 100 or word_count > 500:
            return jsonify({
                "error": f"Motivation must be 100-500 words (you have {word_count})"
            }), 400
        
        # Insert into database
        query = """
            INSERT INTO applications (full_name, email, phone, country, motivation, status)
            VALUES (%s, %s, %s, %s, %s, 'pending')
            RETURNING id
        """
        
        result = execute_query(query, (
            data['full_name'],
            data['email'],
            data['phone'],
            data['country'],
            data['motivation']
        ), fetch=False)
        
        new_id = result['id']
        
        return jsonify({
            "success": True,
            "message": "Application submitted successfully",
            "id": new_id
        }), 201
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# UPDATE APPLICATION STATUS (Approve/Reject)
# ============================================
@applications_bp.route('/api/applications/<int:id>/review', methods=['PUT'])
def review_application(id):
    """
    Approve or reject an application
    Expects: {"status": "approved"} or {"status": "rejected"}
    """
    try:
        data = request.get_json()
        
        new_status = data.get('status')
        if new_status not in ['approved', 'rejected']:
            return jsonify({
                "error": "Status must be 'approved' or 'rejected'"
            }), 400
        
        query = """
            UPDATE applications 
            SET status = %s, reviewed_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        
        affected = execute_query(query, (new_status, id), fetch=False)
        
        if affected == 0:
            return jsonify({
                "success": False,
                "error": "Application not found"
            }), 404
        
        return jsonify({
            "success": True,
            "message": f"Application {new_status}"
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500