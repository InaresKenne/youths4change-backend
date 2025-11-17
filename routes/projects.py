from flask import Blueprint, request, jsonify
from config.database import execute_query
import re

# Create blueprint
projects_bp = Blueprint('projects', __name__)

# ============================================
# GET ALL PROJECTS (with optional filters)
# ============================================
@projects_bp.route('/api/projects', methods=['GET'])
def get_all_projects():
    """
    Get all projects, optionally filtered by country or status
    Query params: ?country=Ghana&status=active
    """
    try:
        # Get filter parameters from URL
        country = request.args.get('country', '')
        status = request.args.get('status', '')
        
        # Build query dynamically based on filters
        query = "SELECT * FROM projects WHERE 1=1"
        params = []
        
        if country:
            query += " AND country = %s"
            params.append(country)
        
        if status:
            query += " AND status = %s"
            params.append(status)
        
        query += " ORDER BY created_at DESC"
        
        # Execute query
        projects = execute_query(query, tuple(params) if params else None)
        
        return jsonify({
            "success": True,
            "data": projects,
            "count": len(projects)
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# GET SINGLE PROJECT
# ============================================
@projects_bp.route('/api/projects/<int:id>', methods=['GET'])
def get_project(id):
    """
    Get one specific project by ID
    """
    try:
        query = "SELECT * FROM projects WHERE id = %s"
        projects = execute_query(query, (id,))
        
        if not projects or len(projects) == 0:
            return jsonify({
                "success": False,
                "error": "Project not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": projects[0]
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# CREATE PROJECT
# ============================================
@projects_bp.route('/api/projects', methods=['POST'])
def create_project():
    """
    Create a new project
    Expects JSON body with project data
    """
    try:
        data = request.get_json()
        
        # Validation - check required fields
        if not data.get('name'):
            return jsonify({"error": "Name is required"}), 400
        
        if not data.get('description'):
            return jsonify({"error": "Description is required"}), 400
        
        # Regex validation for name (5-100 chars, alphanumeric, spaces, hyphens, ampersands)
        name_pattern = r'^[a-zA-Z0-9\\s\\-&]{5,100}$'
        if not re.match(name_pattern, data['name']):
            return jsonify({
                "error": "Invalid project name format. Must be 5-100 characters, alphanumeric, spaces, hyphens, and ampersands only."
            }), 400
        
        # Validate description length (50-1000 chars)
        description = data.get('description', '')
        if len(description) < 50 or len(description) > 1000:
            return jsonify({
                "error": "Description must be between 50 and 1000 characters"
            }), 400
        
        # Insert into database
        query = """
            INSERT INTO projects (name, description, country, beneficiaries_count, budget, status, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        
        result = execute_query(query, (
            data['name'],
            data['description'],
            data.get('country', ''),
            data.get('beneficiaries_count', 0),
            data.get('budget', 0),
            data.get('status', 'active'),
            data.get('image_url', '')
        ), fetch=False)
        
        new_id = result['id']
        
        return jsonify({
            "success": True,
            "message": "Project created successfully",
            "id": new_id
        }), 201
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# UPDATE PROJECT
# ============================================
@projects_bp.route('/api/projects/<int:id>', methods=['PUT'])
def update_project(id):
    """
    Update existing project
    """
    try:
        data = request.get_json()
        
        # Validate name if provided
        if data.get('name'):
            name_pattern = r'^[a-zA-Z0-9\\s\\-&]{5,100}$'
            if not re.match(name_pattern, data['name']):
                return jsonify({
                    "error": "Invalid project name format"
                }), 400
        
        # Validate description if provided
        if data.get('description'):
            description = data['description']
            if len(description) < 50 or len(description) > 1000:
                return jsonify({
                    "error": "Description must be between 50 and 1000 characters"
                }), 400
        
        # Update database
        query = """
            UPDATE projects 
            SET name = %s, description = %s, country = %s, 
                beneficiaries_count = %s, budget = %s, status = %s, 
                image_url = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        
        affected = execute_query(query, (
            data['name'],
            data['description'],
            data['country'],
            data['beneficiaries_count'],
            data['budget'],
            data['status'],
            data.get('image_url', ''),
            id
        ), fetch=False)
        
        if affected == 0:
            return jsonify({
                "success": False,
                "error": "Project not found"
            }), 404
        
        return jsonify({
            "success": True,
            "message": "Project updated successfully"
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# DELETE PROJECT (Soft Delete)
# ============================================
@projects_bp.route('/api/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    """
    Soft delete a project (mark as deleted instead of removing)
    """
    try:
        # Soft delete - just mark as deleted
        query = "UPDATE projects SET status = 'deleted' WHERE id = %s"
        affected = execute_query(query, (id,), fetch=False)
        
        if affected == 0:
            return jsonify({
                "success": False,
                "error": "Project not found"
            }), 404
        
        return jsonify({
            "success": True,
            "message": "Project deleted successfully"
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500