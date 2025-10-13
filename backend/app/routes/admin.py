"""
Admin routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.models.conversation import Conversation
from app import mongo
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(fn):
    """Decorator to require admin role"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user or user.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        return fn(*args, **kwargs)
    
    return wrapper

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users"""
    try:
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 50))
        
        users = User.get_all_users(skip, limit)
        total = mongo.db.users.count_documents({})
        
        return jsonify({
            'users': [User.serialize(u) for u in users],
            'total': total
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    """Get user by ID"""
    try:
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': User.serialize(user)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<user_id>/deactivate', methods=['POST'])
@admin_required
def deactivate_user(user_id):
    """Deactivate user account"""
    try:
        from bson import ObjectId
        result = mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'is_active': False}}
        )
        
        if result.modified_count == 0:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'message': 'User deactivated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
    """Get system statistics"""
    try:
        total_users = mongo.db.users.count_documents({})
        total_conversations = mongo.db.conversations.count_documents({})
        total_tests = mongo.db.test_results.count_documents({})
        
        # Active users (logged in last 30 days)
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        active_users = mongo.db.conversations.distinct(
            'user_id',
            {'timestamp': {'$gte': thirty_days_ago}}
        )
        
        return jsonify({
            'stats': {
                'total_users': total_users,
                'active_users': len(active_users),
                'total_conversations': total_conversations,
                'total_tests': total_tests
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/conversations/recent', methods=['GET'])
@admin_required
def get_recent_conversations():
    """Get recent conversations across all users"""
    try:
        limit = int(request.args.get('limit', 100))
        
        conversations = list(
            mongo.db.conversations
            .find()
            .sort('timestamp', -1)
            .limit(limit)
        )
        
        return jsonify({
            'conversations': [Conversation.serialize(c) for c in conversations],
            'total': len(conversations)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
