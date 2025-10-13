"""
Career information service
"""

import json
import os
from ai.career_model import CareerRecommendationModel
from ai.hybrid_recommender import HybridCareerRecommender

class CareerService:
    def __init__(self):
        self.careers = []
        self.model = CareerRecommendationModel()
        self.hybrid = None
        self.load_careers()
        self.load_model()
    
    def load_careers(self):
        """Load career data"""
        try:
            career_file = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                '..', 'data', 'career_data.json'
            )
            
            with open(career_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.careers = data['careers']
                print(f"✓ Loaded {len(self.careers)} careers")
        except Exception as e:
            print(f"⚠ Warning: Could not load career data: {str(e)}")
    
    def load_model(self):
        """Load trained AI model"""
        try:
            model_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                '..', 'ai', 'models'
            )
            if os.path.exists(os.path.join(model_path, 'career_model.pkl')):
                self.model.load_model(model_path)
            # Initialize hybrid recommender with classic model as a component
            try:
                career_data_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)), '..', 'data', 'career_data.json'
                )
                self.hybrid = HybridCareerRecommender(career_data_path=career_data_path, classic_model=self.model)
            except Exception as e:
                print(f"⚠ Warning: Could not initialize hybrid recommender: {str(e)}")
        except Exception as e:
            print(f"⚠ Warning: Could not load AI model: {str(e)}")
    
    def get_all_careers(self, skip=0, limit=50):
        """Get all careers with pagination"""
        return self.careers[skip:skip+limit]
    
    def get_career_by_id(self, career_id):
        """Get career by ID"""
        for career in self.careers:
            if career['id'] == career_id:
                return career
        return None
    
    def search_careers(self, query):
        """Search careers by keyword"""
        query_lower = query.lower()
        results = []
        
        for career in self.careers:
            # Search in name, description, and interests
            searchable = (
                career['name'].lower() + ' ' +
                career['description'].lower() + ' ' +
                ' '.join(career['interests'])
            )
            
            if query_lower in searchable:
                results.append(career)
        
        return results
    
    def get_recommendations(self, interests_text):
        """Get career recommendations based on interests"""
        try:
            if self.hybrid is not None:
                recommendations = self.hybrid.recommend(interests_text, top_n=5)
            else:
                recommendations = self.model.predict(interests_text, top_n=5)
            return recommendations
        except Exception as e:
            print(f"Error getting recommendations: {str(e)}")
            # Fallback: return random careers
            return self.careers[:5]
