"""
Chatbot service for handling conversations
"""

import os
from ai.chatbot_nlp import CareerChatbot
from ai.career_model import CareerRecommendationModel
from ai.hybrid_recommender import HybridCareerRecommender
from app.services.llm_service import generate_gemini_reply

class ChatbotService:
    def __init__(self):
        self.chatbot = CareerChatbot()
        self.model = CareerRecommendationModel()
        self.hybrid = None
        self.load_model()
    
    def load_model(self):
        """Load trained AI model"""
        try:
            model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'ai', 'models')
            if os.path.exists(os.path.join(model_path, 'career_model.pkl')):
                self.model.load_model(model_path)
                print("✓ AI model loaded successfully")
            else:
                print("⚠ Warning: AI model not found. Please train the model first.")
            # Initialize hybrid recommender
            try:
                career_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'data', 'career_data.json')
                self.hybrid = HybridCareerRecommender(career_data_path=career_data_path, classic_model=self.model)
            except Exception as e:
                print(f"⚠ Warning: Could not initialize hybrid recommender: {str(e)}")
        except Exception as e:
            print(f"⚠ Warning: Could not load AI model: {str(e)}")
    
    def process_message(self, user_id, message):
        """Process user message and generate response"""
        # Try Gemini first for natural response
        llm_text = generate_gemini_reply(message)
        chatbot_result = self.chatbot.generate_response(message)
        
        response_data = {
            'response': llm_text or chatbot_result['response'],
            'intent': chatbot_result['intent'],
            'confidence': chatbot_result['confidence']
        }
        
        # If interests detected, get career recommendations
        if chatbot_result['requires_career_recommendation']:
            interests_text = message
            if chatbot_result['extracted_interests']:
                interests_text += ' ' + ' '.join(chatbot_result['extracted_interests'])
            
            try:
                if self.hybrid is not None:
                    recommendations = self.hybrid.recommend(interests_text, top_n=3)
                else:
                    recommendations = self.model.predict(interests_text, top_n=3)
                response_data['recommendations'] = recommendations
                
                # If Gemini responded, append recommendations; else fully format
                if llm_text:
                    response_data['response'] = llm_text + "\n\n" + self.chatbot.format_career_recommendation(recommendations)
                else:
                    response_data['response'] = self.chatbot.format_career_recommendation(recommendations)
                
            except Exception as e:
                print(f"Error getting recommendations: {str(e)}")
                response_data['response'] += "\n\n(Lưu ý: Hệ thống AI đang được cập nhật)"
        
        return response_data
    
    def get_suggestions(self):
        """Get conversation starter suggestions"""
        return self.chatbot.get_conversation_starters()
