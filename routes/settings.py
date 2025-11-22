from flask import Blueprint, jsonify
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