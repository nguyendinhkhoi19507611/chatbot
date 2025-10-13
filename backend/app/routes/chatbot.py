"""
Chatbot API routes
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.conversation import Conversation
from app.services.chatbot_service import ChatbotService

chatbot_bp = Blueprint('chatbot', __name__)

# Initialize chatbot service
chatbot_service = ChatbotService()

@chatbot_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    """Handle chat message"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        message = data.get('message', '').strip()
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Process message
        result = chatbot_service.process_message(user_id, message)
        
        # Save conversation
        Conversation.create_message(
            user_id=user_id,
            message=message,
            response=result['response'],
            intent=result.get('intent'),
            recommendations=result.get('recommendations')
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    """Get conversation history"""
    try:
        user_id = get_jwt_identity()
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 50))
        
        conversations = Conversation.get_user_history(user_id, skip, limit)
        
        return jsonify({
            'conversations': [Conversation.serialize(c) for c in conversations],
            'total': len(conversations)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/history', methods=['DELETE'])
@jwt_required()
def delete_history():
    """Delete conversation history"""
    try:
        user_id = get_jwt_identity()
        deleted_count = Conversation.delete_user_history(user_id)
        
        return jsonify({
            'message': 'History deleted successfully',
            'deleted_count': deleted_count
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chatbot_bp.route('/suggestions', methods=['GET'])
def get_suggestions():
    """Get conversation starter suggestions"""
    try:
        suggestions = chatbot_service.get_suggestions()
        
        return jsonify({
            'suggestions': suggestions
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
