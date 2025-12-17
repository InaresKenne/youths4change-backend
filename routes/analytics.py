from flask import Blueprint, jsonify
from config.database import execute_query

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/api/analytics/overview', methods=['GET'])
def get_overview():
    """Get overall statistics - calculated from real data in a single optimized query"""
    try:
        # Single query to get all statistics at once using CTEs
        query = """
            WITH project_stats AS (
                SELECT 
                    COUNT(*) FILTER (WHERE status != 'deleted') as total_projects,
                    COUNT(*) FILTER (WHERE status = 'active') as active_projects,
                    COALESCE(SUM(beneficiaries_count) FILTER (WHERE status = 'active'), 0) as total_beneficiaries,
                    COUNT(DISTINCT country) FILTER (WHERE status != 'deleted') as countries_count
                FROM projects
            ),
            application_stats AS (
                SELECT 
                    COUNT(*) as total_applications,
                    COUNT(*) FILTER (WHERE status = 'approved') as approved_applications
                FROM applications
            ),
            donation_stats AS (
                SELECT COALESCE(SUM(amount), 0) as total_donations
                FROM donations
            ),
            team_stats AS (
                SELECT 
                    COUNT(*) FILTER (WHERE is_active = true) as total_team_members
                FROM team_members
            )
            SELECT 
                p.total_projects,
                p.active_projects,
                p.total_beneficiaries,
                p.countries_count,
                a.total_applications,
                a.approved_applications,
                d.total_donations,
                t.total_team_members
            FROM project_stats p, application_stats a, donation_stats d, team_stats t
        """
        
        result = execute_query(query)[0]
        
        return jsonify({
            "success": True,
            "data": {
                "total_projects": result['total_projects'],
                "active_projects": result['active_projects'],
                "total_applications": result['total_applications'],
                "approved_applications": result['approved_applications'],
                "total_donations": float(result['total_donations']),
                "total_beneficiaries": result['total_beneficiaries'],
                "countries_count": result['countries_count'],
                "total_team_members": result['total_team_members'],
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


@analytics_bp.route('/api/analytics/countries', methods=['GET'])
def get_countries():
    """Get list of all active countries from projects"""
    try:
        query = """
            SELECT DISTINCT country 
            FROM projects 
            WHERE status != 'deleted' AND country IS NOT NULL AND country != ''
            ORDER BY country ASC
        """
        data = execute_query(query)
        countries = [row['country'] for row in data]
        
        return jsonify({
            "success": True,
            "data": countries
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