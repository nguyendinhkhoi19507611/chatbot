"""
User model and database operations
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from app import mongo

class User:
    """User model"""
    
    @staticmethod
    def create_user(username, email, password, full_name=None):
        """Create a new user"""
        user_data = {
            'username': username,
            'email': email,
            'password': generate_password_hash(password),
            'full_name': full_name,
            'role': 'user',  # 'user' or 'admin'
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'is_active': True,
            'profile': {
                'interests': [],
                'career_preferences': [],
                'test_results': []
            }
        }
        
        result = mongo.db.users.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        return user_data
    
    @staticmethod
    def find_by_username(username):
        """Find user by username"""
        return mongo.db.users.find_one({'username': username})
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        return mongo.db.users.find_one({'email': email})
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        return mongo.db.users.find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def verify_password(user, password):
        """Verify user password"""
        return check_password_hash(user['password'], password)
    
    @staticmethod
    def update_profile(user_id, profile_data):
        """Update user profile"""
        update_data = {
            'updated_at': datetime.utcnow()
        }
        
        if 'interests' in profile_data:
            update_data['profile.interests'] = profile_data['interests']
        if 'career_preferences' in profile_data:
            update_data['profile.career_preferences'] = profile_data['career_preferences']
        
        mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
        
        return User.find_by_id(user_id)
    
    @staticmethod
    def get_all_users(skip=0, limit=20):
        """Get all users (for admin)"""
        users = list(mongo.db.users.find().skip(skip).limit(limit))
        return users
    
    @staticmethod
    def serialize(user):
        """Serialize user object"""
        if not user:
            return None
        
        return {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email'],
            'full_name': user.get('full_name'),
            'role': user.get('role', 'user'),
            'created_at': user['created_at'].isoformat() if user.get('created_at') else None,
            'profile': user.get('profile', {})
        }
