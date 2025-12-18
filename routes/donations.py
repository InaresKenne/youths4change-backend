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
# CREATE DONATION (Manual Payment)
# ============================================
@donations_bp.route('/api/donations', methods=['POST'])
def create_donation():
    """
    Record a donation with manual payment verification
    Supports Mobile Money and Bank Transfer
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['donor_name', 'email', 'amount', 'project_id', 'country', 'payment_method']
        for field in required:
            if not data.get(field):
                return jsonify({
                    "error": f"{field.replace('_', ' ').title()} is required"
                }), 400
        
        # Validate payment method
        valid_methods = ['mobile_money', 'bank_transfer']
        if data['payment_method'] not in valid_methods:
            return jsonify({"error": "Invalid payment method"}), 400
        
        # Validate transaction reference is provided
        if not data.get('transaction_id'):
            return jsonify({"error": "Transaction reference is required"}), 400
        
        # Validate email
        email_pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$'
        if not re.match(email_pattern, data['email']):
            return jsonify({"error": "Invalid email format"}), 400
        
        # Validate amount (decimal, min 5 GHS)
        amount = float(data['amount'])
        if amount < 5:
            return jsonify({"error": "Minimum donation is 5 GHS"}), 400
        
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
        
        # Insert donation with pending status
        query = """
            INSERT INTO donations (
                donor_name, email, amount, project_id, country, 
                payment_method, transaction_id, payment_proof_url,
                currency, payment_status, status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        
        result = execute_query(query, (
            data['donor_name'],
            data['email'],
            amount,
            data['project_id'],
            data['country'],
            data['payment_method'],
            data['transaction_id'],
            data.get('payment_proof_url'),  # Optional payment screenshot
            data.get('currency', 'GHS'),
            'pending',  # Pending verification
            'pending'   # Overall status
        ), fetch=False)
        
        new_id = result[0]['id'] if result else None
        
        return jsonify({
            "success": True,
            "message": "Donation submitted successfully. We'll verify your payment within 24 hours.",
            "id": new_id,
            "payment_status": "pending"
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
                p.name as project_name,
                a.username as verified_by_username
            FROM donations d
            LEFT JOIN projects p ON d.project_id = p.id
            LEFT JOIN admins a ON d.verified_by = a.id
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

# ============================================
# VERIFY DONATION (Admin)
# ============================================
@donations_bp.route('/api/donations/<int:donation_id>/verify', methods=['PUT'])
def verify_donation(donation_id):
    """Admin endpoint to verify a pending donation"""
    try:
        data = request.get_json()
        
        # Get admin ID from session (you should implement proper auth)
        admin_id = data.get('admin_id', 3)  # Default admin for now
        
        # Check if donation exists
        donation = execute_query(
            "SELECT id, payment_status FROM donations WHERE id = %s",
            (donation_id,)
        )
        
        if not donation:
            return jsonify({"error": "Donation not found"}), 404
        
        if donation[0]['payment_status'] == 'verified':
            return jsonify({"error": "Donation already verified"}), 400
        
        # Update donation status to verified
        query = """
            UPDATE donations
            SET payment_status = 'verified',
                status = 'completed',
                verified_by = %s,
                verified_at = CURRENT_TIMESTAMP,
                verification_notes = %s
            WHERE id = %s
        """
        
        execute_query(query, (
            admin_id,
            data.get('notes', 'Payment verified'),
            donation_id
        ), fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Donation verified successfully"
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# REJECT DONATION (Admin)
# ============================================
@donations_bp.route('/api/donations/<int:donation_id>/reject', methods=['PUT'])
def reject_donation(donation_id):
    """Admin endpoint to reject a pending donation"""
    try:
        data = request.get_json()
        
        # Get admin ID from session
        admin_id = data.get('admin_id', 3)  # Default admin for now
        
        # Validate rejection reason
        if not data.get('reason'):
            return jsonify({"error": "Rejection reason is required"}), 400
        
        # Check if donation exists
        donation = execute_query(
            "SELECT id, payment_status FROM donations WHERE id = %s",
            (donation_id,)
        )
        
        if not donation:
            return jsonify({"error": "Donation not found"}), 404
        
        if donation[0]['payment_status'] == 'verified':
            return jsonify({"error": "Cannot reject verified donation"}), 400
        
        # Update donation status to rejected
        query = """
            UPDATE donations
            SET payment_status = 'rejected',
                status = 'rejected',
                verified_by = %s,
                verified_at = CURRENT_TIMESTAMP,
                verification_notes = %s
            WHERE id = %s
        """
        
        execute_query(query, (
            admin_id,
            data['reason'],
            donation_id
        ), fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Donation rejected successfully"
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500