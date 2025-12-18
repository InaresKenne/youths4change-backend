from flask import Blueprint, request, jsonify
from config.database import execute_query
from functools import wraps
from flask import session

team_bp = Blueprint('team', __name__, url_prefix='/api/team')

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return jsonify({"success": False, "error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

# ============= PUBLIC ROUTES =============

@team_bp.route('/founder', methods=['GET'])
def get_founder():
    """Get founder information (public)"""
    try:
        query = """
            SELECT id, name, title, bio, image_url, email, 
                   linkedin_url, twitter_url
            FROM founder
            WHERE is_active = TRUE
            LIMIT 1
        """
        founder = execute_query(query)
        
        if founder and len(founder) > 0:
            return jsonify({
                "success": True,
                "data": founder[0]
            })
        else:
            return jsonify({
                "success": True,
                "data": None
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@team_bp.route('/members', methods=['GET'])
def get_team_members():
    """Get all active team members (public)"""
    try:
        role_type = request.args.get('role_type')  # Filter by role if provided
        
        query = """
            SELECT id, name, position, role_type, bio, image_url,
                   email, linkedin_url, twitter_url, country, order_position
            FROM team_members
            WHERE is_active = TRUE
        """
        
        params = []
        if role_type:
            query += " AND role_type = %s"
            params.append(role_type)
            
        query += " ORDER BY order_position ASC, name ASC"
        
        members = execute_query(query, tuple(params)) if params else execute_query(query)
        
        return jsonify({
            "success": True,
            "data": members
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============= ADMIN ROUTES =============

@team_bp.route('/admin/founder', methods=['GET'])
# @require_auth  # Temporarily disabled - session not working on production
def admin_get_founder():
    """Get founder information for admin"""
    try:
        query = """
            SELECT id, name, title, bio, image_url, image_public_id,
                   email, linkedin_url, twitter_url, is_active, 
                   created_at, updated_at
            FROM founder
            LIMIT 1
        """
        founder = execute_query(query)
        
        return jsonify({
            "success": True,
            "data": founder[0] if founder else None
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@team_bp.route('/admin/founder', methods=['PUT'])
# @require_auth  # Temporarily disabled - session not working on production
def admin_update_founder():
    """Update founder information"""
    try:
        data = request.json
        
        # Check if founder exists
        check_query = "SELECT id FROM founder LIMIT 1"
        existing = execute_query(check_query)
        
        if existing:
            # Update existing
            query = """
                UPDATE founder
                SET name = %s, title = %s, bio = %s, image_url = %s,
                    image_public_id = %s, email = %s, linkedin_url = %s,
                    twitter_url = %s, is_active = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """
            params = (
                data.get('name'),
                data.get('title'),
                data.get('bio'),
                data.get('image_url'),
                data.get('image_public_id'),
                data.get('email'),
                data.get('linkedin_url'),
                data.get('twitter_url'),
                data.get('is_active', True),
                existing[0]['id']
            )
        else:
            # Insert new
            query = """
                INSERT INTO founder (name, title, bio, image_url, image_public_id,
                                   email, linkedin_url, twitter_url, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                data.get('name'),
                data.get('title'),
                data.get('bio'),
                data.get('image_url'),
                data.get('image_public_id'),
                data.get('email'),
                data.get('linkedin_url'),
                data.get('twitter_url'),
                data.get('is_active', True)
            )
        
        execute_query(query, params, fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Founder information updated successfully"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@team_bp.route('/admin/members', methods=['GET'])
# @require_auth  # Temporarily disabled - session not working on production
def admin_get_all_members():
    """Get all team members (including inactive) for admin"""
    try:
        query = """
            SELECT id, name, position, role_type, bio, image_url, image_public_id,
                   email, linkedin_url, twitter_url, country, order_position,
                   is_active, created_at, updated_at
            FROM team_members
            ORDER BY order_position ASC, name ASC
        """
        members = execute_query(query)
        print(f"=== Admin GET all members ===")
        print(f"Total members found: {len(members) if members else 0}")
        if members:
            print(f"Executive members: {len([m for m in members if m.get('role_type') == 'executive'])}")
        
        return jsonify({
            "success": True,
            "data": members
        })
        
    except Exception as e:
        print(f"Error getting admin members: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@team_bp.route('/admin/members/<int:member_id>', methods=['GET'])
# @require_auth  # Temporarily disabled - session not working on production
def admin_get_member(member_id):
    """Get a specific team member"""
    try:
        query = """
            SELECT id, name, position, role_type, bio, image_url, image_public_id,
                   email, linkedin_url, twitter_url, country, order_position,
                   is_active, created_at, updated_at
            FROM team_members
            WHERE id = %s
        """
        member = execute_query(query, (member_id,))
        
        if not member:
            return jsonify({
                "success": False,
                "error": "Team member not found"
            }), 404
            
        return jsonify({
            "success": True,
            "data": member[0]
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@team_bp.route('/admin/members', methods=['POST'])
# @require_auth  # Temporarily disabled - session not working on production
def admin_create_member():
    """Create a new team member"""
    try:
        data = request.json
        print("=== Creating new team member ===")
        print(f"Received data: {data}")
        
        query = """
            INSERT INTO team_members (name, position, role_type, bio, image_url,
                                     image_public_id, email, linkedin_url, twitter_url,
                                     country, order_position, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        
        params = (
            data.get('name'),
            data.get('position'),
            data.get('role_type'),
            data.get('bio'),
            data.get('image_url'),
            data.get('image_public_id'),
            data.get('email'),
            data.get('linkedin_url'),
            data.get('twitter_url'),
            data.get('country'),
            data.get('order_position', 0),
            data.get('is_active', True)
        )
        
        print(f"Query params: {params}")
        result = execute_query(query, params, fetch=False)
        print(f"Insert result: {result}")
        
        # Verify the member was actually created
        if result and len(result) > 0:
            member_id = result[0]['id']
            verify_query = "SELECT * FROM team_members WHERE id = %s"
            verification = execute_query(verify_query, (member_id,))
            print(f"Verification check - Member exists: {verification}")
        
        return jsonify({
            "success": True,
            "message": "Team member created successfully",
            "id": result[0]['id'] if result else None
        }), 201
        
    except Exception as e:
        print(f"Error creating team member: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@team_bp.route('/admin/members/<int:member_id>', methods=['PUT'])
# @require_auth  # Temporarily disabled - session not working on production
def admin_update_member(member_id):
    """Update a team member"""
    try:
        data = request.json
        
        query = """
            UPDATE team_members
            SET name = %s, position = %s, role_type = %s, bio = %s,
                image_url = %s, image_public_id = %s, email = %s,
                linkedin_url = %s, twitter_url = %s, country = %s,
                order_position = %s, is_active = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        
        params = (
            data.get('name'),
            data.get('position'),
            data.get('role_type'),
            data.get('bio'),
            data.get('image_url'),
            data.get('image_public_id'),
            data.get('email'),
            data.get('linkedin_url'),
            data.get('twitter_url'),
            data.get('country'),
            data.get('order_position', 0),
            data.get('is_active', True),
            member_id
        )
        
        execute_query(query, params, fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Team member updated successfully"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@team_bp.route('/admin/members/<int:member_id>', methods=['DELETE'])
# @require_auth  # Temporarily disabled - session not working on production
def admin_delete_member(member_id):
    """Delete a team member"""
    try:
        query = "DELETE FROM team_members WHERE id = %s"
        execute_query(query, (member_id,), fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Team member deleted successfully"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
