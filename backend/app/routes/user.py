"""
User profile and test routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.test_result import TestResult
from app.services.test_service import TestService

user_bp = Blueprint('user', __name__)

# Initialize test service
test_service = TestService()

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': User.serialize(user)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        user = User.update_profile(user_id, data)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': User.serialize(user)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/test/questions', methods=['GET'])
@jwt_required()
def get_test_questions():
    """Get career test questions"""
    try:
        test_type = request.args.get('type', 'interest')
        questions = test_service.get_questions(test_type)
        
        return jsonify({
            'questions': questions,
            'test_type': test_type
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/test/questions', methods=['OPTIONS'])
def get_test_questions_options():
    return ('', 204)

@user_bp.route('/test/submit', methods=['POST'])
@jwt_required()
def submit_test():
    """Submit career test answers"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json(silent=True)
        if data is None:
            return jsonify({'error': 'Invalid JSON payload'}), 400
        
        test_type = data.get('test_type', 'interest')
        answers = data.get('answers', [])
        
        if not answers:
            return jsonify({'error': 'Answers are required'}), 400
        
        # Evaluate test
        results = test_service.evaluate_test(test_type, answers)
        
        # Save results
        test_result = TestResult.save_result(
            user_id=user_id,
            test_type=test_type,
            answers=answers,
            results=results['scores'],
            recommendations=results['recommendations']
        )
        
        return jsonify({
            'message': 'Test submitted successfully',
            'results': TestResult.serialize(test_result)
        }), 201
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@user_bp.route('/test/submit', methods=['OPTIONS'])
def submit_test_options():
    return ('', 204)

@user_bp.route('/test/results', methods=['GET'])
@jwt_required()
def get_test_results():
    """Get user test results"""
    try:
        user_id = get_jwt_identity()
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 20))
        
        results = TestResult.get_user_results(user_id, skip, limit)
        
        return jsonify({
            'results': [TestResult.serialize(r) for r in results],
            'total': len(results)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/test/results/latest', methods=['GET'])
@jwt_required()
def get_latest_test_result():
    """Get latest test result"""
    try:
        user_id = get_jwt_identity()
        test_type = request.args.get('type')
        
        result = TestResult.get_latest_result(user_id, test_type)
        
        if not result:
            return jsonify({'error': 'No test results found'}), 404
        
        return jsonify({
            'result': TestResult.serialize(result)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
