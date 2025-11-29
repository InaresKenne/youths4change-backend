from flask import Blueprint, jsonify, request
from config.database import execute_query

contact_bp = Blueprint('contact', __name__)

# ============================================
# GET MAIN CONTACT INFO
# ============================================
@contact_bp.route('/api/contact-info', methods=['GET'])
def get_contact_info():
    """Get main contact information"""
    try:
        query = """
            SELECT id, contact_type, label, value, link, icon, order_position
            FROM contact_info
            ORDER BY order_position
        """
        contacts = execute_query(query)
        
        return jsonify({
            "success": True,
            "data": contacts
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================
# UPDATE CONTACT INFO
# ============================================
@contact_bp.route('/api/contact-info/<int:contact_id>', methods=['PUT'])
def update_contact_info(contact_id):
    """Update a contact info entry"""
    try:
        data = request.get_json()
        
        query = """
            UPDATE contact_info 
            SET label = %s, value = %s, link = %s, icon = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        execute_query(query, (
            data.get('label'),
            data.get('value'),
            data.get('link'),
            data.get('icon'),
            contact_id
        ), fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Contact info updated successfully"
        })
    except Exception as e:
        print(f"Error updating contact info: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# GET SOCIAL MEDIA LINKS
# ============================================
@contact_bp.route('/api/social-media', methods=['GET'])
def get_social_media():
    """Get social media links"""
    try:
        query = """
            SELECT id, platform, platform_name, url, icon, color_class, is_active, order_position
            FROM social_media
            ORDER BY order_position
        """
        socials = execute_query(query)
        
        return jsonify({
            "success": True,
            "data": socials
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================
# GET ALL SOCIAL MEDIA (Including inactive for admin)
# ============================================
@contact_bp.route('/api/social-media/all', methods=['GET'])
def get_all_social_media():
    """Get all social media links including inactive"""
    try:
        query = """
            SELECT id, platform, platform_name, url, icon, color_class, is_active, order_position
            FROM social_media
            ORDER BY order_position
        """
        socials = execute_query(query)
        
        return jsonify({
            "success": True,
            "data": socials
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================
# CREATE SOCIAL MEDIA
# ============================================
@contact_bp.route('/api/social-media', methods=['POST'])
def create_social_media():
    """Create a new social media link"""
    try:
        data = request.get_json()
        
        required = ['platform', 'platform_name', 'url']
        for field in required:
            if not data.get(field):
                return jsonify({"success": False, "error": f"{field} is required"}), 400
        
        # Get next order position
        max_pos_result = execute_query("SELECT COALESCE(MAX(order_position), 0) as max_pos FROM social_media")
        max_pos = max_pos_result[0]['max_pos'] if max_pos_result else 0
        
        query = """
            INSERT INTO social_media (platform, platform_name, url, icon, color_class, is_active, order_position)
            VALUES (%s, %s, %s, %s, %s, TRUE, %s)
        """
        execute_query(query, (
            data['platform'],
            data['platform_name'],
            data['url'],
            data.get('icon', data['platform_name']),
            data.get('color_class', 'text-gray-600 hover:bg-gray-50'),
            max_pos + 1
        ), fetch=False)
        
        # Get the inserted ID
        id_result = execute_query("SELECT id FROM social_media ORDER BY id DESC LIMIT 1")
        new_id = id_result[0]['id'] if id_result else None
        
        return jsonify({
            "success": True,
            "data": {"id": new_id},
            "message": "Social media link created successfully"
        }), 201
    except Exception as e:
        print(f"Error creating social media: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# UPDATE SOCIAL MEDIA
# ============================================
@contact_bp.route('/api/social-media/<int:social_id>', methods=['PUT'])
def update_social_media(social_id):
    """Update a social media link"""
    try:
        data = request.get_json()
        
        query = """
            UPDATE social_media 
            SET platform = %s, platform_name = %s, url = %s, icon = %s, 
                color_class = %s, is_active = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        execute_query(query, (
            data.get('platform'),
            data.get('platform_name'),
            data.get('url'),
            data.get('icon'),
            data.get('color_class'),
            data.get('is_active', True),
            social_id
        ), fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Social media link updated successfully"
        })
    except Exception as e:
        print(f"Error updating social media: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# DELETE SOCIAL MEDIA
# ============================================
@contact_bp.route('/api/social-media/<int:social_id>', methods=['DELETE'])
def delete_social_media(social_id):
    """Delete a social media link (hard delete)"""
    try:
        # Hard delete - actually remove from database
        query = "DELETE FROM social_media WHERE id = %s"
        execute_query(query, (social_id,), fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Social media link deleted successfully"
        })
    except Exception as e:
        print(f"Error deleting social media: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    """Delete a social media link"""
    try:
        query = "DELETE FROM social_media WHERE id = %s"
        execute_query(query, (social_id,), fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Social media link deleted successfully"
        })
    except Exception as e:
        print(f"Error deleting social media: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# GET REGIONAL OFFICES
# ============================================
@contact_bp.route('/api/regional-offices', methods=['GET'])
def get_regional_offices():
    """Get regional office contacts"""
    try:
        query = """
            SELECT id, country, email, phone, address, is_active, order_position
            FROM regional_offices
            WHERE is_active = TRUE
            ORDER BY order_position
        """
        offices = execute_query(query)
        
        return jsonify({
            "success": True,
            "data": offices
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================
# GET ALL REGIONAL OFFICES (Including inactive for admin)
# ============================================
@contact_bp.route('/api/regional-offices/all', methods=['GET'])
def get_all_regional_offices():
    """Get all regional offices including inactive"""
    try:
        query = """
            SELECT id, country, email, phone, address, is_active, order_position
            FROM regional_offices
            ORDER BY order_position
        """
        offices = execute_query(query)
        
        return jsonify({
            "success": True,
            "data": offices
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================
# CREATE REGIONAL OFFICE
# ============================================
@contact_bp.route('/api/regional-offices', methods=['POST'])
def create_regional_office():
    """Create a new regional office"""
    try:
        data = request.get_json()
        
        required = ['country', 'email', 'phone']
        for field in required:
            if not data.get(field):
                return jsonify({"success": False, "error": f"{field} is required"}), 400
        
        # Check if country already exists (only check active offices)
        existing = execute_query(
            "SELECT id FROM regional_offices WHERE country = %s",
            (data['country'],)
        )
        if existing and len(existing) > 0:
            return jsonify({"success": False, "error": "Office for this country already exists"}), 400
        
        # Get next order position
        max_pos_result = execute_query("SELECT COALESCE(MAX(order_position), 0) as max_pos FROM regional_offices")
        max_pos = max_pos_result[0]['max_pos'] if max_pos_result else 0
        
        query = """
            INSERT INTO regional_offices (country, email, phone, address, is_active, order_position)
            VALUES (%s, %s, %s, %s, TRUE, %s)
        """
        execute_query(query, (
            data['country'],
            data['email'],
            data['phone'],
            data.get('address', ''),
            max_pos + 1
        ), fetch=False)
        
        # Get the inserted ID
        id_result = execute_query("SELECT id FROM regional_offices ORDER BY id DESC LIMIT 1")
        new_id = id_result[0]['id'] if id_result else None
        
        return jsonify({
            "success": True,
            "data": {"id": new_id},
            "message": "Regional office created successfully"
        }), 201
    except Exception as e:
        print(f"Error creating regional office: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    """Create a new regional office"""
    try:
        data = request.get_json()
        
        required = ['country', 'email', 'phone']
        for field in required:
            if not data.get(field):
                return jsonify({"success": False, "error": f"{field} is required"}), 400
        
        # Check if country already exists (only check active offices)
        existing = execute_query(
            "SELECT id FROM regional_offices WHERE country = %s",
            (data['country'],)
        )
        if existing and len(existing) > 0:
            return jsonify({"success": False, "error": "Office for this country already exists"}), 400
        
        # Get next order position
        max_pos_result = execute_query("SELECT COALESCE(MAX(order_position), 0) as max_pos FROM regional_offices")
        max_pos = max_pos_result[0]['max_pos'] if max_pos_result else 0
        
        query = """
            INSERT INTO regional_offices (country, email, phone, address, is_active, order_position)
            VALUES (%s, %s, %s, %s, TRUE, %s)
        """
        execute_query(query, (
            data['country'],
            data['email'],
            data['phone'],
            data.get('address', ''),
            max_pos + 1
        ), fetch=False)
        
        # Get the inserted ID
        id_result = execute_query("SELECT id FROM regional_offices ORDER BY id DESC LIMIT 1")
        new_id = id_result[0]['id'] if id_result else None
        
        return jsonify({
            "success": True,
            "data": {"id": new_id},
            "message": "Regional office created successfully"
        }), 201
    except Exception as e:
        print(f"Error creating regional office: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    """Create a new regional office"""
    try:
        data = request.get_json()
        
        required = ['country', 'email', 'phone']
        for field in required:
            if not data.get(field):
                return jsonify({"success": False, "error": f"{field} is required"}), 400
        
        # Check if country already exists
        existing = execute_query(
            "SELECT id FROM regional_offices WHERE country = %s",
            (data['country'],)
        )
        if existing and len(existing) > 0:
            return jsonify({"success": False, "error": "Office for this country already exists"}), 400
        
        # Get next order position
        max_pos_result = execute_query("SELECT COALESCE(MAX(order_position), 0) as max_pos FROM regional_offices")
        max_pos = max_pos_result[0]['max_pos'] if max_pos_result else 0
        
        query = """
            INSERT INTO regional_offices (country, email, phone, address, is_active, order_position)
            VALUES (%s, %s, %s, %s, TRUE, %s)
        """
        execute_query(query, (
            data['country'],
            data['email'],
            data['phone'],
            data.get('address', ''),
            max_pos + 1
        ), fetch=False)
        
        # Get the inserted ID
        id_result = execute_query("SELECT id FROM regional_offices ORDER BY id DESC LIMIT 1")
        new_id = id_result[0]['id'] if id_result else None
        
        return jsonify({
            "success": True,
            "data": {"id": new_id},
            "message": "Regional office created successfully"
        }), 201
    except Exception as e:
        print(f"Error creating regional office: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# UPDATE REGIONAL OFFICE
# ============================================
@contact_bp.route('/api/regional-offices/<int:office_id>', methods=['PUT'])
def update_regional_office(office_id):
    """Update a regional office"""
    try:
        data = request.get_json()
        
        query = """
            UPDATE regional_offices 
            SET country = %s, email = %s, phone = %s, address = %s, 
                is_active = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        execute_query(query, (
            data.get('country'),
            data.get('email'),
            data.get('phone'),
            data.get('address'),
            data.get('is_active', True),
            office_id
        ), fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Regional office updated successfully"
        })
    except Exception as e:
        print(f"Error updating regional office: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# DELETE REGIONAL OFFICE
# ============================================
@contact_bp.route('/api/regional-offices/<int:office_id>', methods=['DELETE'])
def delete_regional_office(office_id):
    """Delete a regional office (hard delete)"""
    try:
        # Hard delete - actually remove from database
        query = "DELETE FROM regional_offices WHERE id = %s"
        execute_query(query, (office_id,), fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Regional office deleted successfully"
        })
    except Exception as e:
        print(f"Error deleting regional office: {e}")
        return jsonify({"success": False, "error": str(e)}), 500