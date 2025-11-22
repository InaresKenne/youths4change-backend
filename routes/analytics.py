from flask import Blueprint, jsonify
from config.database import execute_query

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/api/analytics/overview', methods=['GET'])
def get_overview():
    """Get overall statistics - calculated from real data"""
    try:
        # Count active projects
        total_projects = execute_query(
            "SELECT COUNT(*) as count FROM projects WHERE status != 'deleted'"
        )[0]['count']
        
        # Count all applications
        total_applications = execute_query(
            "SELECT COUNT(*) as count FROM applications"
        )[0]['count']
        
        # Count approved applications (young leaders)
        approved_applications = execute_query(
            "SELECT COUNT(*) as count FROM applications WHERE status = 'approved'"
        )[0]['count']
        
        # Sum total donations
        total_donations = execute_query(
            "SELECT COALESCE(SUM(amount), 0) as total FROM donations"
        )[0]['total']
        
        # Sum beneficiaries from active projects
        total_beneficiaries = execute_query(
            "SELECT COALESCE(SUM(beneficiaries_count), 0) as total FROM projects WHERE status = 'active'"
        )[0]['total']
        
        # Count distinct countries we operate in
        countries_count = execute_query(
            "SELECT COUNT(DISTINCT country) as count FROM projects WHERE status != 'deleted'"
        )[0]['count']
        
        return jsonify({
            "success": True,
            "data": {
                "total_projects": total_projects,
                "active_projects": execute_query(
                    "SELECT COUNT(*) as count FROM projects WHERE status = 'active'"
                )[0]['count'],
                "total_applications": total_applications,
                "approved_applications": approved_applications,
                "total_donations": float(total_donations),
                "total_beneficiaries": total_beneficiaries,
                "countries_count": countries_count,
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@analytics_bp.route('/api/analytics/projects-by-country', methods=['GET'])
def projects_by_country():
    """Get project count and members by country"""
    try:
        query = """
            SELECT 
                country, 
                COUNT(*) as project_count,
                COALESCE(SUM(beneficiaries_count), 0) as total_beneficiaries
            FROM projects 
            WHERE status != 'deleted'
            GROUP BY country
            ORDER BY project_count DESC
        """
        data = execute_query(query)
        
        return jsonify({
            "success": True,
            "data": data
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@analytics_bp.route('/api/analytics/applications-status', methods=['GET'])
def applications_status():
    """Get application counts by status"""
    try:
        query = """
            SELECT status, COUNT(*) as count 
            FROM applications 
            GROUP BY status
        """
        data = execute_query(query)
        
        return jsonify({
            "success": True,
            "data": data
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500