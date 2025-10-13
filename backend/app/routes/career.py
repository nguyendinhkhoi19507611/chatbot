"""
Career information routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.career_service import CareerService

career_bp = Blueprint('career', __name__)

# Initialize career service
career_service = CareerService()

# Support both / and no trailing slash
# Add explicit OPTIONS handlers to avoid 308 preflight redirects on preflight
@career_bp.route('', methods=['OPTIONS'])
@career_bp.route('/', methods=['OPTIONS'])
def careers_options():
    return ('', 204)

@career_bp.route('', methods=['GET'])
@career_bp.route('/', methods=['GET'])
def get_all_careers():
    """Get all careers"""
    try:
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 50))
        
        careers = career_service.get_all_careers(skip, limit)
        
        return jsonify({
            'careers': careers,
            'total': len(careers)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@career_bp.route('/<int:career_id>', methods=['GET'])
def get_career(career_id):
    """Get career by ID"""
    try:
        career = career_service.get_career_by_id(career_id)
        
        if not career:
            return jsonify({'error': 'Career not found'}), 404
        
        return jsonify({
            'career': career
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@career_bp.route('/search', methods=['GET'])
def search_careers():
    """Search careers by keyword"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        careers = career_service.search_careers(query)
        
        return jsonify({
            'careers': careers,
            'total': len(careers)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@career_bp.route('/search', methods=['OPTIONS'])
def search_careers_options():
    return ('', 204)

@career_bp.route('/recommend', methods=['POST'])
@jwt_required()
def recommend_careers():
    """Get career recommendations based on interests"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        interests = data.get('interests', '')
        if not interests:
            return jsonify({'error': 'Interests are required'}), 400
        
        recommendations = career_service.get_recommendations(interests)
        
        return jsonify({
            'recommendations': recommendations
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@career_bp.route('/recommend', methods=['OPTIONS'])
def recommend_careers_options():
    return ('', 204)
