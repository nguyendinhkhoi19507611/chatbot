"""
Career test result model
"""

from datetime import datetime
from bson import ObjectId
from app import mongo
from app.utils.serialization import to_native_types

class TestResult:
    """Model for storing career assessment test results"""
    
    @staticmethod
    def save_result(user_id, test_type, answers, results, recommendations):
        """Save test result"""
        test_data = {
            'user_id': ObjectId(user_id),
            'test_type': test_type,  # 'interest', 'skill', 'personality'
            'answers': to_native_types(answers),
            'results': to_native_types(results),
            'recommendations': to_native_types(recommendations),
            'created_at': datetime.utcnow()
        }
        
        result = mongo.db.test_results.insert_one(test_data)
        test_data['_id'] = result.inserted_id
        
        # Update user profile with latest test result
        mongo.db.users.update_one(
            {'_id': ObjectId(user_id)},
            {
                '$push': {
                    'profile.test_results': {
                        'test_id': result.inserted_id,
                        'test_type': test_type,
                        'date': datetime.utcnow()
                    }
                }
            }
        )
        
        return test_data
    
    @staticmethod
    def get_user_results(user_id, skip=0, limit=20):
        """Get user test results"""
        results = list(
            mongo.db.test_results
            .find({'user_id': ObjectId(user_id)})
            .sort('created_at', -1)
            .skip(skip)
            .limit(limit)
        )
        return results
    
    @staticmethod
    def get_latest_result(user_id, test_type=None):
        """Get latest test result for user"""
        query = {'user_id': ObjectId(user_id)}
        if test_type:
            query['test_type'] = test_type
        
        result = mongo.db.test_results.find_one(
            query,
            sort=[('created_at', -1)]
        )
        return result
    
    @staticmethod
    def serialize(test_result):
        """Serialize test result object"""
        if not test_result:
            return None
        
        return {
            'id': str(test_result['_id']),
            'user_id': str(test_result['user_id']),
            'test_type': test_result['test_type'],
            'answers': test_result['answers'],
            'results': test_result['results'],
            'recommendations': test_result['recommendations'],
            'created_at': test_result['created_at'].isoformat()
        }
