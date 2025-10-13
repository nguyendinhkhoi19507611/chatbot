"""
Conversation history model
"""

from datetime import datetime
from bson import ObjectId
from app import mongo

class Conversation:
    """Conversation model for storing chat history"""
    
    @staticmethod
    def create_message(user_id, message, response, intent=None, recommendations=None):
        """Save a conversation message"""
        conversation_data = {
            'user_id': ObjectId(user_id),
            'message': message,
            'response': response,
            'intent': intent,
            'recommendations': recommendations,
            'timestamp': datetime.utcnow()
        }
        
        result = mongo.db.conversations.insert_one(conversation_data)
        conversation_data['_id'] = result.inserted_id
        return conversation_data
    
    @staticmethod
    def get_user_history(user_id, skip=0, limit=50):
        """Get user conversation history"""
        conversations = list(
            mongo.db.conversations
            .find({'user_id': ObjectId(user_id)})
            .sort('timestamp', -1)
            .skip(skip)
            .limit(limit)
        )
        return conversations
    
    @staticmethod
    def get_recent_conversations(user_id, limit=10):
        """Get recent conversations for context"""
        return Conversation.get_user_history(user_id, skip=0, limit=limit)
    
    @staticmethod
    def delete_user_history(user_id):
        """Delete all conversations for a user"""
        result = mongo.db.conversations.delete_many({'user_id': ObjectId(user_id)})
        return result.deleted_count
    
    @staticmethod
    def serialize(conversation):
        """Serialize conversation object"""
        if not conversation:
            return None
        
        return {
            'id': str(conversation['_id']),
            'user_id': str(conversation['user_id']),
            'message': conversation['message'],
            'response': conversation['response'],
            'intent': conversation.get('intent'),
            'recommendations': conversation.get('recommendations'),
            'timestamp': conversation['timestamp'].isoformat()
        }
