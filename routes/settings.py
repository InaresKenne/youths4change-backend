from flask import Blueprint, jsonify, request
from config.database import execute_query

settings_bp = Blueprint('settings', __name__)

# ============================================
# GET ALL SITE SETTINGS
# ============================================
@settings_bp.route('/api/settings', methods=['GET'])
def get_settings():
    """Get all site settings as key-value pairs"""
    try:
        query = """
            SELECT setting_key, setting_value, setting_type
            FROM site_settings
            ORDER BY setting_key
        """
        settings_list = execute_query(query)
        
        # Convert to dictionary for easier access
        settings_dict = {
            item['setting_key']: item['setting_value'] 
            for item in settings_list
        }
        
        return jsonify({
            "success": True,
            "data": settings_dict
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================
# GET SPECIFIC SETTING
# ============================================
@settings_bp.route('/api/settings/<setting_key>', methods=['GET'])
def get_setting(setting_key):
    """Get a specific setting by key"""
    try:
        query = """
            SELECT setting_key, setting_value, setting_type
            FROM site_settings
            WHERE setting_key = %s
        """
        settings = execute_query(query, (setting_key,))
        
        if not settings or len(settings) == 0:
            return jsonify({
                "success": False,
                "error": "Setting not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": settings[0]
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================
# UPDATE SITE SETTINGS
# ============================================
@settings_bp.route('/api/settings', methods=['PUT'])
def update_settings():
    """Update site settings"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Update each setting provided
        for key, value in data.items():
            # Skip if value is None
            if value is None:
                continue
                
            query = """
                UPDATE site_settings 
                SET setting_value = %s, updated_at = CURRENT_TIMESTAMP
                WHERE setting_key = %s
            """
            execute_query(query, (str(value), key), fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Settings updated successfully"
        })
    except Exception as e:
        print(f"Error updating settings: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# GET PAYMENT ACCOUNT DETAILS
# ============================================
@settings_bp.route('/api/payment-accounts', methods=['GET'])
def get_payment_accounts():
    """Get bank and mobile money account details for donations"""
    try:
        query = """
            SELECT setting_key, setting_value
            FROM site_settings
            WHERE setting_key LIKE %s OR setting_key LIKE %s
            ORDER BY setting_key
        """
        settings = execute_query(query, ('bank_%', 'momo_%'))
        
        # Organize into structured format
        payment_accounts = {
            'bank_account': {},
            'mobile_money': {
                'ghana': {},
                'cameroon': {}
            }
        }
        
        for setting in settings:
            key = setting['setting_key']
            value = setting['setting_value']
            
            if key.startswith('bank_'):
                payment_accounts['bank_account'][key.replace('bank_', '')] = value
            elif key == 'momo_number_ghana':
                payment_accounts['mobile_money']['ghana']['number'] = value
            elif key == 'momo_name_ghana':
                payment_accounts['mobile_money']['ghana']['name'] = value
            elif key == 'momo_number_cameroon':
                payment_accounts['mobile_money']['cameroon']['number'] = value
            elif key == 'momo_name_cameroon':
                payment_accounts['mobile_money']['cameroon']['name'] = value
        
        return jsonify({
            "success": True,
            "data": payment_accounts
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================
# GET PAGE CONTENT
# ============================================
@settings_bp.route('/api/content/<page_name>', methods=['GET'])
def get_page_content(page_name):
    """Get all content for a specific page"""
    try:
        query = """
            SELECT section_key, content_value, content_type, order_position
            FROM page_content
            WHERE page_name = %s
            ORDER BY order_position
        """
        content_list = execute_query(query, (page_name,))
        
        # Convert to dictionary
        content_dict = {
            item['section_key']: item['content_value'] 
            for item in content_list
        }
        
        return jsonify({
            "success": True,
            "data": content_dict
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================
# UPDATE PAGE CONTENT
# ============================================
@settings_bp.route('/api/content/<page_name>', methods=['PUT'])
def update_page_content(page_name):
    """Update content for a specific page"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Update each section provided
        for section_key, section_data in data.items():
            # Skip if value is None
            if section_data is None:
                continue
            
            # section_data can be either:
            # - A string (text content)
            # - A dict with 'cloudinary_public_id' key (image content)
            
            content_value = None
            cloudinary_public_id = None
            
            if isinstance(section_data, dict) and 'cloudinary_public_id' in section_data:
                # This is image content
                cloudinary_public_id = section_data['cloudinary_public_id']
            else:
                # This is text content
                content_value = section_data
            
            # Check if exists
            existing = execute_query(
                "SELECT id FROM page_content WHERE page_name = %s AND section_key = %s",
                (page_name, section_key)
            )
            
            if existing and len(existing) > 0:
                # Update
                query = """
                    UPDATE page_content 
                    SET content_value = %s, cloudinary_public_id = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE page_name = %s AND section_key = %s
                """
                execute_query(query, (content_value, cloudinary_public_id, page_name, section_key), fetch=False)
            else:
                # Insert
                query = """
                    INSERT INTO page_content (page_name, section_key, content_value, cloudinary_public_id)
                    VALUES (%s, %s, %s, %s)
                """
                execute_query(query, (page_name, section_key, content_value, cloudinary_public_id), fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Page content updated successfully"
        })
    except Exception as e:
        print(f"Error updating page content: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    """Update content for a specific page"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        # Update each section provided
        for section_key, content_value in data.items():
            # Skip if value is None
            if content_value is None:
                continue
            
            # Check if exists
            existing = execute_query(
                "SELECT id FROM page_content WHERE page_name = %s AND section_key = %s",
                (page_name, section_key)
            )
            
            if existing and len(existing) > 0:
                # Update
                query = """
                    UPDATE page_content 
                    SET content_value = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE page_name = %s AND section_key = %s
                """
                execute_query(query, (content_value, page_name, section_key), fetch=False)
            else:
                # Insert
                query = """
                    INSERT INTO page_content (page_name, section_key, content_value)
                    VALUES (%s, %s, %s)
                """
                execute_query(query, (page_name, section_key, content_value), fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Page content updated successfully"
        })
    except Exception as e:
        print(f"Error updating page content: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# GET CORE VALUES
# ============================================
@settings_bp.route('/api/core-values', methods=['GET'])
def get_core_values():
    """Get all active core values"""
    try:
        query = """
            SELECT id, title, description, icon, order_position
            FROM core_values
            WHERE is_active = TRUE
            ORDER BY order_position
        """
        values = execute_query(query)
        
        return jsonify({
            "success": True,
            "data": values
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================
# CREATE CORE VALUE
# ============================================
@settings_bp.route('/api/core-values', methods=['POST'])
def create_core_value():
    """Create a new core value"""
    try:
        data = request.get_json()
        
        required = ['title', 'description', 'icon']
        for field in required:
            if not data.get(field):
                return jsonify({"success": False, "error": f"{field} is required"}), 400
        
        # Get next order position
        max_pos_result = execute_query("SELECT COALESCE(MAX(order_position), 0) as max_pos FROM core_values")
        max_pos = max_pos_result[0]['max_pos'] if max_pos_result else 0
        
        query = """
            INSERT INTO core_values (title, description, icon, order_position, is_active)
            VALUES (%s, %s, %s, %s, TRUE)
            RETURNING id
        """
        result = execute_query(query, (
            data['title'],
            data['description'],
            data['icon'],
            max_pos + 1
        ), fetch=False)
        
        # Get the inserted ID
        id_result = execute_query("SELECT id FROM core_values ORDER BY id DESC LIMIT 1")
        new_id = id_result[0]['id'] if id_result else None
        
        return jsonify({
            "success": True,
            "data": {"id": new_id},
            "message": "Core value created successfully"
        }), 201
    except Exception as e:
        print(f"Error creating core value: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# UPDATE CORE VALUE
# ============================================
@settings_bp.route('/api/core-values/<int:value_id>', methods=['PUT'])
def update_core_value(value_id):
    """Update a core value"""
    try:
        data = request.get_json()
        
        query = """
            UPDATE core_values 
            SET title = %s, description = %s, icon = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        execute_query(query, (
            data.get('title'),
            data.get('description'),
            data.get('icon'),
            value_id
        ), fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Core value updated successfully"
        })
    except Exception as e:
        print(f"Error updating core value: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# DELETE CORE VALUE
# ============================================
@settings_bp.route('/api/core-values/<int:value_id>', methods=['DELETE'])
def delete_core_value(value_id):
    """Delete a core value (soft delete)"""
    try:
        query = "UPDATE core_values SET is_active = FALSE WHERE id = %s"
        execute_query(query, (value_id,), fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Core value deleted successfully"
        })
    except Exception as e:
        print(f"Error deleting core value: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# GET TEAM ROLES
# ============================================
@settings_bp.route('/api/team-roles', methods=['GET'])
def get_team_roles():
    """Get all active team roles"""
    try:
        query = """
            SELECT id, role_title, responsibilities, order_position
            FROM team_roles
            WHERE is_active = TRUE
            ORDER BY order_position
        """
        roles = execute_query(query)
        
        return jsonify({
            "success": True,
            "data": roles
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================
# CREATE TEAM ROLE
# ============================================
@settings_bp.route('/api/team-roles', methods=['POST'])
def create_team_role():
    """Create a new team role"""
    try:
        data = request.get_json()
        
        required = ['role_title', 'responsibilities']
        for field in required:
            if not data.get(field):
                return jsonify({"success": False, "error": f"{field} is required"}), 400
        
        # Get next order position
        max_pos_result = execute_query("SELECT COALESCE(MAX(order_position), 0) as max_pos FROM team_roles")
        max_pos = max_pos_result[0]['max_pos'] if max_pos_result else 0
        
        query = """
            INSERT INTO team_roles (role_title, responsibilities, order_position, is_active)
            VALUES (%s, %s, %s, TRUE)
            RETURNING id
        """
        execute_query(query, (
            data['role_title'],
            data['responsibilities'],
            max_pos + 1
        ), fetch=False)
        
        # Get the inserted ID
        id_result = execute_query("SELECT id FROM team_roles ORDER BY id DESC LIMIT 1")
        new_id = id_result[0]['id'] if id_result else None
        
        return jsonify({
            "success": True,
            "data": {"id": new_id},
            "message": "Team role created successfully"
        }), 201
    except Exception as e:
        print(f"Error creating team role: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# UPDATE TEAM ROLE
# ============================================
@settings_bp.route('/api/team-roles/<int:role_id>', methods=['PUT'])
def update_team_role(role_id):
    """Update a team role"""
    try:
        data = request.get_json()
        
        query = """
            UPDATE team_roles 
            SET role_title = %s, responsibilities = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        execute_query(query, (
            data.get('role_title'),
            data.get('responsibilities'),
            role_id
        ), fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Team role updated successfully"
        })
    except Exception as e:
        print(f"Error updating team role: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================
# DELETE TEAM ROLE
# ============================================
@settings_bp.route('/api/team-roles/<int:role_id>', methods=['DELETE'])
def delete_team_role(role_id):
    """Delete a team role (soft delete)"""
    try:
        query = "UPDATE team_roles SET is_active = FALSE WHERE id = %s"
        execute_query(query, (role_id,), fetch=False)
        
        return jsonify({
            "success": True,
            "message": "Team role deleted successfully"
        })
    except Exception as e:
        print(f"Error deleting team role: {e}")
        return jsonify({"success": False, "error": str(e)}), 500