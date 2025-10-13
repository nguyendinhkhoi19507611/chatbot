"""
NLP-based Chatbot for Career Counseling
Handles natural language conversations with users
"""

import json
import re
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Tuple

try:
    from transformers import pipeline
    _zshot_intent = pipeline(
        "zero-shot-classification",
        model="joeddav/xlm-roberta-large-xnli"
    )
except Exception:
    _zshot_intent = None

class CareerChatbot:
    def __init__(self):
        self.responses = self.load_responses()
        self.intents = self.load_intents()
        self.vectorizer = TfidfVectorizer()
        self.intent_patterns = []
        self.intent_tags = []
        self.prepare_intent_matching()
        
    def load_responses(self):
        """Load chatbot response templates"""
        return {
            'greeting': [
                "Xin chào! Tôi là trợ lý tư vấn nghề nghiệp. Tôi có thể giúp gì cho bạn?",
                "Chào bạn! Tôi ở đây để giúp bạn tìm kiếm hướng đi nghề nghiệp phù hợp. Bạn muốn tìm hiểu về điều gì?",
                "Xin chào! Rất vui được hỗ trợ bạn trong việc lựa chọn nghề nghiệp. Hãy cho tôi biết sở thích của bạn nhé!"
            ],
            'farewell': [
                "Chúc bạn thành công trên con đường sự nghiệp! Hẹn gặp lại!",
                "Rất vui được hỗ trợ bạn. Chúc bạn tìm được nghề nghiệp phù hợp!",
                "Tạm biệt! Nếu cần tư vấn thêm, đừng ngại quay lại nhé!"
            ],
            'thanks': [
                "Rất vui được giúp đỡ bạn!",
                "Không có gì! Đó là nhiệm vụ của tôi.",
                "Cảm ơn bạn! Chúc bạn may mắn!"
            ],
            'help': [
                "Tôi có thể giúp bạn:\n- Tìm nghề nghiệp phù hợp với sở thích\n- Cung cấp thông tin chi tiết về các ngành nghề\n- Gợi ý lộ trình phát triển sự nghiệp\n- Thực hiện bài test đánh giá sở thích",
                "Bạn có thể hỏi tôi về:\n✓ Các ngành nghề phù hợp với sở thích của bạn\n✓ Thông tin về lương, học vấn cần thiết\n✓ Lộ trình phát triển nghề nghiệp\n✓ Làm bài test để tìm nghề phù hợp"
            ],
            'interests_query': [
                "Hãy cho tôi biết bạn thích làm gì? Sở thích của bạn là gì?",
                "Bạn có thể kể cho tôi nghe về những điều bạn đam mê không?",
                "Những hoạt động nào khiến bạn cảm thấy hứng thú nhất?"
            ],
            'career_info': [
                "Đây là thông tin về nghề này:",
                "Để trở thành {career}, bạn cần:",
                "Nghề {career} có những đặc điểm sau:"
            ],
            'unknown': [
                "Xin lỗi, tôi chưa hiểu rõ câu hỏi của bạn. Bạn có thể nói rõ hơn không?",
                "Tôi chưa nắm bắt được ý bạn. Bạn muốn hỏi về nghề nghiệp nào?",
                "Hmm, câu hỏi khá thú vị nhưng tôi cần thêm thông tin. Bạn có thể mô tả cụ thể hơn không?"
            ],
            'test_prompt': [
                "Bạn muốn làm bài test đánh giá sở thích để tìm nghề phù hợp không?",
                "Tôi có thể giúp bạn làm một bài test nhanh để tìm ra nghề nghiệp phù hợp. Bạn có muốn thử không?",
                "Chúng ta có thể bắt đầu với một bài đánh giá sở thích. Bạn có 5 phút không?"
            ]
        }
    
    def load_intents(self):
        """Load intent patterns for classification"""
        return {
            'greeting': [
                'xin chào', 'hello', 'hi', 'chào', 'helo', 'hey'
            ],
            'farewell': [
                'tạm biệt', 'bye', 'goodbye', 'hẹn gặp lại', 'cảm ơn tạm biệt'
            ],
            'thanks': [
                'cảm ơn', 'thanks', 'thank you', 'cám ơn', 'thanks bạn'
            ],
            'help': [
                'giúp đỡ', 'help', 'hướng dẫn', 'làm sao', 'giúp tôi', 'trợ giúp'
            ],
            'interests_query': [
                'sở thích', 'thích', 'đam mê', 'yêu thích', 'interests', 'hobby'
            ],
            'career_info': [
                'nghề', 'ngành', 'career', 'job', 'công việc', 'nghề nghiệp', 'lương'
            ],
            'test_prompt': [
                'test', 'bài test', 'đánh giá', 'kiểm tra', 'assessment'
            ]
        }
    
    def prepare_intent_matching(self):
        """Prepare patterns for intent matching"""
        for intent, patterns in self.intents.items():
            for pattern in patterns:
                self.intent_patterns.append(pattern)
                self.intent_tags.append(intent)
        
        if self.intent_patterns:
            self.vectorizer.fit(self.intent_patterns)
    
    def preprocess_text(self, text):
        """Preprocess user input"""
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        return text.strip()
    
    def detect_intent(self, user_input) -> Tuple[str, float]:
        """Detect user intent using pattern matching"""
        user_input = self.preprocess_text(user_input)
        
        # Simple keyword matching first
        for intent, patterns in self.intents.items():
            for pattern in patterns:
                if pattern in user_input:
                    return intent, 1.0
        
        # If no direct match, try zero-shot classifier first
        if _zshot_intent is not None:
            try:
                intents = list(self.intents.keys())
                res = _zshot_intent(user_input, candidate_labels=intents, hypothesis_template="Đây là ý định {}.")
                if res and res['labels'] and res['scores']:
                    if res['scores'][0] >= 0.50:  # confident threshold
                        return res['labels'][0], float(res['scores'][0])
            except Exception:
                pass

        # If still no match, use TF-IDF similarity
        if self.intent_patterns:
            user_vec = self.vectorizer.transform([user_input])
            pattern_vecs = self.vectorizer.transform(self.intent_patterns)
            similarities = cosine_similarity(user_vec, pattern_vecs)[0]
            
            max_sim_idx = np.argmax(similarities)
            max_similarity = similarities[max_sim_idx]
            
            if max_similarity > 0.3:  # Threshold
                return self.intent_tags[max_sim_idx], float(max_similarity)
        
        return 'unknown', 0.0
    
    def extract_interests(self, user_input):
        """Extract interest keywords from user input"""
        interest_keywords = [
            'lập trình', 'code', 'công nghệ', 'nghệ thuật', 'vẽ', 'thiết kế',
            'y học', 'bác sĩ', 'chăm sóc', 'giáo dục', 'dạy học', 'tài chính',
            'kế toán', 'marketing', 'kinh doanh', 'xây dựng', 'kiến trúc',
            'viết lách', 'báo chí', 'dữ liệu', 'phân tích', 'nấu ăn', 'ẩm thực',
            'luật', 'nhiếp ảnh', 'chụp ảnh', 'tâm lý', 'âm nhạc', 'thể thao'
        ]
        
        found_interests = []
        user_input_lower = user_input.lower()
        
        for keyword in interest_keywords:
            if keyword in user_input_lower:
                found_interests.append(keyword)
        
        return found_interests
    
    def generate_response(self, user_input, context=None):
        """Generate chatbot response"""
        # Detect intent
        intent, confidence = self.detect_intent(user_input)
        
        # Generate response based on intent
        if intent in self.responses:
            response = random.choice(self.responses[intent])
        else:
            response = random.choice(self.responses['unknown'])
        
        # Extract interests if present
        interests = self.extract_interests(user_input)
        
        return {
            'response': response,
            'intent': intent,
            'confidence': confidence,
            'extracted_interests': interests,
            'requires_career_recommendation': len(interests) > 0 or intent == 'interests_query'
        }
    
    def format_career_recommendation(self, recommendations):
        """Format career recommendations into natural language"""
        if not recommendations:
            return "Tôi chưa tìm được nghề phù hợp. Bạn có thể cho tôi biết thêm về sở thích của bạn không?"
        
        response = "Dựa trên sở thích của bạn, tôi gợi ý những nghề nghiệp sau:\n\n"
        
        for i, rec in enumerate(recommendations, 1):
            response += f"{i}. **{rec['career_name']}** (Độ phù hợp: {rec['confidence']*100:.0f}%)\n"
            response += f"   📝 {rec['description']}\n"
            response += f"   💰 Mức lương: {rec['salary_range']}\n"
            response += f"   🎓 Học vấn: {rec['education']}\n"
            if i < len(recommendations):
                response += "\n"
        
        response += "\nBạn muốn tìm hiểu chi tiết về nghề nào?"
        
        return response
    
    def get_conversation_starters(self):
        """Get suggested conversation starters"""
        return [
            "Tôi thích lập trình và công nghệ",
            "Tôi muốn làm việc trong lĩnh vực sáng tạo",
            "Cho tôi làm bài test đánh giá sở thích",
            "Tôi muốn tìm hiểu về các ngành nghề"
        ]


if __name__ == '__main__':
    # Test chatbot
    chatbot = CareerChatbot()
    
    print("Testing Chatbot NLP...")
    print("=" * 60)
    
    test_inputs = [
        "Xin chào",
        "Tôi thích lập trình và công nghệ",
        "Cho tôi biết về nghề kỹ sư phần mềm",
        "Cảm ơn bạn",
        "Tạm biệt"
    ]
    
    for user_input in test_inputs:
        print(f"\nUser: {user_input}")
        result = chatbot.generate_response(user_input)
        print(f"Bot: {result['response']}")
        print(f"Intent: {result['intent']} (confidence: {result['confidence']:.2f})")
        if result['extracted_interests']:
            print(f"Interests found: {result['extracted_interests']}")
