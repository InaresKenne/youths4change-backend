from flask import Blueprint, request, jsonify
from config.database import execute_query
import re

donations_bp = Blueprint('donations', __name__)

# ============================================
# GET ALL DONATIONS (with filters)
# ============================================
@donations_bp.route('/api/donations', methods=['GET'])
def get_donations():
    """Get all donations with optional filters"""
    try:
        project_id = request.args.get('project_id')
        country = request.args.get('country')
        search = request.args.get('search')
        
        query = """
            SELECT 
                d.*,
                p.name as project_name
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
        
        if search:
            query += " AND (d.donor_name ILIKE %s OR d.email ILIKE %s)"
            params.extend([f'%{search}%', f'%{search}%'])
        
        query += " ORDER BY d.donation_date DESC"
        
        donations = execute_query(query, tuple(params) if params else None)
        
        # Convert Decimal to float for JSON serialization
        for donation in donations:
            donation['amount'] = float(donation['amount'])
        
        return jsonify({
            "success": True,
            "data": donations,
            "count": len(donations)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
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
        email_pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$'
        if not re.match(email_pattern, data['email']):
            return jsonify({"error": "Invalid email format"}), 400
        
        # Validate amount (decimal, min $5)
        amount = float(data['amount'])
        if amount < 5:
            return jsonify({"error": "Minimum donation is $5"}), 400
        
        # Validate name
        name_pattern = r'^[a-zA-Z\s]{2,50}$'
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
        
        new_id = result[0]['id'] if result else None
        
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
# ============================================
# GET DONATION STATISTICS (Admin)
# ============================================
@donations_bp.route('/api/donations/stats', methods=['GET'])
def get_donation_stats():
    """Get donation statistics for admin dashboard"""
    try:
        # Total donations
        total_query = """
            SELECT 
                COUNT(*) as total_count,
                COALESCE(SUM(amount), 0) as total_amount
            FROM donations
        """
        totals = execute_query(total_query)[0]
        
        # By country
        country_query = """
            SELECT 
                country,
                COUNT(*) as count,
                COALESCE(SUM(amount), 0) as amount
            FROM donations
            GROUP BY country
            ORDER BY amount DESC
        """
        by_country = execute_query(country_query)
        
        # By project
        project_query = """
            SELECT 
                d.project_id,
                p.name as project_name,
                COUNT(*) as count,
                COALESCE(SUM(d.amount), 0) as amount
            FROM donations d
            LEFT JOIN projects p ON d.project_id = p.id
            GROUP BY d.project_id, p.name
            ORDER BY amount DESC
        """
        by_project = execute_query(project_query)
        
        return jsonify({
            "success": True,
            "data": {
                "total_count": totals['total_count'],
                "total_amount": float(totals['total_amount']),
                "by_country": [
                    {"country": r['country'], "count": r['count'], "amount": float(r['amount'])}
                    for r in by_country
                ],
                "by_project": [
                    {"project_id": r['project_id'], "project_name": r['project_name'], "count": r['count'], "amount": float(r['amount'])}
                    for r in by_project
                ]
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ============================================
# GET SINGLE DONATION BY ID
# ============================================
@donations_bp.route('/api/donations/<int:donation_id>', methods=['GET'])
def get_donation(donation_id):
    """Get a single donation by ID"""
    try:
        query = """
            SELECT 
                d.*,
                p.name as project_name
            FROM donations d
            LEFT JOIN projects p ON d.project_id = p.id
            WHERE d.id = %s
        """
        donations = execute_query(query, (donation_id,))
        
        if not donations or len(donations) == 0:
            return jsonify({
                "success": False,
                "error": "Donation not found"
            }), 404
        
        donation = donations[0]
        donation['amount'] = float(donation['amount'])
        
        return jsonify({
            "success": True,
            "data": donation
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500