from flask import Blueprint, request, jsonify
from config.database import execute_query
import re

donations_bp = Blueprint('donations', __name__)

# ============================================
# GET ALL DONATIONS (with filters)
# ============================================
@donations_bp.route('/api/donations', methods=['GET'])
def get_all_donations():
    """
    Get all donations, optionally filtered
    Query params: ?project_id=1&country=Ghana
    """
    try:
        project_id = request.args.get('project_id', '')
        country = request.args.get('country', '')
        
        query = """
            SELECT d.*, p.name as project_name
            FROM donations d
            LEFT JOIN projects p ON d.project_id = p.id
            WHERE 1=1
        """
        params = []
        
        if project_id:
            query += " AND d.project_id = %s"
            params.append(project_id)
        
        if country:
            query += " AND d.country = %s"
            params.append(country)
        
        query += " ORDER BY d.donation_date DESC"
        
        donations = execute_query(query, tuple(params) if params else None)
        
        return jsonify({
            "success": True,
            "data": donations,
            "count": len(donations)
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# CREATE DONATION (Mock)
# ============================================
@donations_bp.route('/api/donations', methods=['POST'])
def create_donation():
    """
    Record a mock donation
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['donor_name', 'email', 'amount', 'project_id', 'country']
        for field in required:
            if not data.get(field):
                return jsonify({
                    "error": f"{field.replace('_', ' ').title()} is required"
                }), 400
        
        # Validate email
        email_pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,6}$'
        if not re.match(email_pattern, data['email']):
            return jsonify({"error": "Invalid email format"}), 400
        
        # Validate amount (decimal, min $5)
        amount = float(data['amount'])
        if amount < 5:
            return jsonify({"error": "Minimum donation is $5"}), 400
        
        # Validate name
        name_pattern = r'^[a-zA-Z\\s]{2,50}$'
        if not re.match(name_pattern, data['donor_name']):
            return jsonify({"error": "Invalid donor name format"}), 400
        
        # Check if project exists
        project_check = execute_query(
            "SELECT id FROM projects WHERE id = %s",
            (data['project_id'],)
        )
        if not project_check:
            return jsonify({"error": "Project not found"}), 404
        
        # Insert donation
        query = """
            INSERT INTO donations (donor_name, email, amount, project_id, country, status)
            VALUES (%s, %s, %s, %s, %s, 'completed')
            RETURNING id
        """
        
        result = execute_query(query, (
            data['donor_name'],
            data['email'],
            amount,
            data['project_id'],
            data['country']
        ), fetch=False)
        
        new_id = result['id']
        
        return jsonify({
            "success": True,
            "message": "Donation recorded successfully",
            "id": new_id,
            "note": "This is a mock donation - no real payment processed"
        }), 201
    
    except ValueError:
        return jsonify({"error": "Invalid amount format"}), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500