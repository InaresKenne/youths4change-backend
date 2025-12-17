from flask import Blueprint, request, jsonify
from config.database import execute_query

# Create blueprint
project_images_bp = Blueprint('project_images', __name__)

# ============================================
# GET PROJECT IMAGES
# ============================================
@project_images_bp.route('/api/projects/<int:project_id>/images', methods=['GET'])
def get_project_images(project_id):
    """Get all images for a specific project"""
    try:
        query = """
            SELECT pi.*, a.full_name as uploaded_by_name
            FROM project_images pi
            LEFT JOIN admins a ON pi.uploaded_by = a.id
            WHERE pi.project_id = %s
            ORDER BY pi.order_position ASC, pi.created_at DESC
        """
        images = execute_query(query, (project_id,))
        
        return jsonify({
            "success": True,
            "data": images,
            "count": len(images)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# ADD PROJECT IMAGE
# ============================================
@project_images_bp.route('/api/projects/<int:project_id>/images', methods=['POST'])
def add_project_image(project_id):
    """Add a new image to a project"""
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('cloudinary_public_id'):
            return jsonify({"error": "Image is required"}), 400
        
        # Get next order position
        max_pos_query = """
            SELECT COALESCE(MAX(order_position), 0) as max_pos 
            FROM project_images 
            WHERE project_id = %s
        """
        max_pos_result = execute_query(max_pos_query, (project_id,))
        max_pos = max_pos_result[0]['max_pos'] if max_pos_result else 0
        
        # Insert image
        query = """
            INSERT INTO project_images 
            (project_id, cloudinary_public_id, caption, order_position, uploaded_by)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        
        result = execute_query(query, (
            project_id,
            data['cloudinary_public_id'],
            data.get('caption', ''),
            max_pos + 1,
            data.get('uploaded_by')
        ), fetch=False)
        
        new_id = result[0]['id'] if result else None
        
        return jsonify({
            "success": True,
            "message": "Image added successfully",
            "id": new_id
        }), 201
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# UPDATE PROJECT IMAGE
# ============================================
@project_images_bp.route('/api/projects/<int:project_id>/images/<int:image_id>', methods=['PUT'])
def update_project_image(project_id, image_id):
    """Update image caption or order"""
    try:
        data = request.get_json()
        
        query = """
            UPDATE project_images 
            SET caption = %s, order_position = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s AND project_id = %s
        """
        
        affected = execute_query(query, (
            data.get('caption', ''),
            data.get('order_position', 0),
            image_id,
            project_id
        ), fetch=False)
        
        if affected == 0:
            return jsonify({
                "success": False,
                "error": "Image not found"
            }), 404
        
        return jsonify({
            "success": True,
            "message": "Image updated successfully"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# DELETE PROJECT IMAGE
# ============================================
@project_images_bp.route('/api/projects/<int:project_id>/images/<int:image_id>', methods=['DELETE'])
def delete_project_image(project_id, image_id):
    """Delete a project image"""
    try:
        query = "DELETE FROM project_images WHERE id = %s AND project_id = %s"
        affected = execute_query(query, (image_id, project_id), fetch=False)
        
        if affected == 0:
            return jsonify({
                "success": False,
                "error": "Image not found"
            }), 404
        
        return jsonify({
            "success": True,
            "message": "Image deleted successfully"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================
# REORDER PROJECT IMAGES
# ============================================
@project_images_bp.route('/api/projects/<int:project_id>/images/reorder', methods=['PUT'])
def reorder_project_images(project_id):
    """Reorder project images"""
    try:
        data = request.get_json()
        image_orders = data.get('images', [])  # Array of {id, order_position}
        
        for item in image_orders:
            query = """
                UPDATE project_images 
                SET order_position = %s
                WHERE id = %s AND project_id = %s
            """
            execute_query(query, (item['order_position'], item['id'], project_id), fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Images reordered successfully"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
