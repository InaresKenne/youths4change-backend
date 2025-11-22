from flask import Blueprint, jsonify
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
# GET SOCIAL MEDIA LINKS
# ============================================
@contact_bp.route('/api/social-media', methods=['GET'])
def get_social_media():
    """Get social media links"""
    try:
        query = """
            SELECT id, platform, platform_name, url, icon, color_class, is_active, order_position
            FROM social_media
            WHERE is_active = TRUE
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