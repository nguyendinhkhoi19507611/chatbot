"""
Career test service
"""

from ai.career_model import CareerRecommendationModel
import os

class TestService:
    def __init__(self):
        self.model = CareerRecommendationModel()
        self.load_model()
        self.questions = self.load_questions()
    
    def load_model(self):
        """Load trained AI model"""
        try:
            model_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), 
                '..', 'ai', 'models'
            )
            if os.path.exists(os.path.join(model_path, 'career_model.pkl')):
                self.model.load_model(model_path)
        except Exception as e:
            print(f"⚠ Warning: Could not load AI model: {str(e)}")
    
    def load_questions(self):
        """Load test questions"""
        return {
            'interest': [
                {
                    'id': 1,
                    'question': 'Bạn thích làm gì nhất trong thời gian rảnh?',
                    'options': [
                        {'value': 'coding', 'label': 'Lập trình và xây dựng phần mềm', 'interests': ['công nghệ', 'lập trình']},
                        {'value': 'design', 'label': 'Thiết kế và sáng tạo nghệ thuật', 'interests': ['nghệ thuật', 'sáng tạo']},
                        {'value': 'help', 'label': 'Giúp đỡ và chăm sóc người khác', 'interests': ['giúp đỡ người khác', 'chăm sóc']},
                        {'value': 'business', 'label': 'Kinh doanh và marketing', 'interests': ['kinh doanh', 'marketing']}
                    ]
                },
                {
                    'id': 2,
                    'question': 'Bạn thích làm việc với điều gì nhất?',
                    'options': [
                        {'value': 'computer', 'label': 'Máy tính và công nghệ', 'interests': ['công nghệ', 'lập trình']},
                        {'value': 'people', 'label': 'Con người và giao tiếp', 'interests': ['giao tiếp', 'giúp đỡ người khác']},
                        {'value': 'numbers', 'label': 'Số liệu và phân tích', 'interests': ['số học', 'phân tích', 'dữ liệu']},
                        {'value': 'creative', 'label': 'Sáng tạo và nghệ thuật', 'interests': ['sáng tạo', 'nghệ thuật']}
                    ]
                },
                {
                    'id': 3,
                    'question': 'Môn học nào bạn thích nhất ở trường?',
                    'options': [
                        {'value': 'math', 'label': 'Toán học', 'interests': ['toán học', 'logic']},
                        {'value': 'art', 'label': 'Mỹ thuật', 'interests': ['nghệ thuật', 'sáng tạo']},
                        {'value': 'science', 'label': 'Khoa học', 'interests': ['khoa học', 'nghiên cứu']},
                        {'value': 'literature', 'label': 'Ngữ văn', 'interests': ['viết lách', 'giao tiếp']}
                    ]
                },
                {
                    'id': 4,
                    'question': 'Bạn muốn làm việc ở môi trường nào?',
                    'options': [
                        {'value': 'office', 'label': 'Văn phòng', 'interests': ['công việc văn phòng']},
                        {'value': 'outdoor', 'label': 'Ngoài trời', 'interests': ['thực tế', 'năng động']},
                        {'value': 'remote', 'label': 'Làm việc từ xa', 'interests': ['công nghệ', 'độc lập']},
                        {'value': 'studio', 'label': 'Studio sáng tạo', 'interests': ['sáng tạo', 'nghệ thuật']}
                    ]
                },
                {
                    'id': 5,
                    'question': 'Kỹ năng nào bạn tự tin nhất?',
                    'options': [
                        {'value': 'technical', 'label': 'Kỹ thuật và công nghệ', 'interests': ['công nghệ', 'kỹ thuật']},
                        {'value': 'communication', 'label': 'Giao tiếp và thuyết phục', 'interests': ['giao tiếp', 'thuyết phục']},
                        {'value': 'creative', 'label': 'Sáng tạo và thiết kế', 'interests': ['sáng tạo', 'thiết kế']},
                        {'value': 'analytical', 'label': 'Phân tích và logic', 'interests': ['phân tích', 'logic']}
                    ]
                },
                {
                    'id': 6,
                    'question': 'Bạn thích học điều gì mới?',
                    'options': [
                        {'value': 'programming', 'label': 'Ngôn ngữ lập trình mới', 'interests': ['lập trình', 'công nghệ']},
                        {'value': 'language', 'label': 'Ngoại ngữ mới', 'interests': ['giao tiếp', 'học tập']},
                        {'value': 'art', 'label': 'Kỹ thuật nghệ thuật mới', 'interests': ['nghệ thuật', 'sáng tạo']},
                        {'value': 'science', 'label': 'Kiến thức khoa học mới', 'interests': ['khoa học', 'nghiên cứu']}
                    ]
                },
                {
                    'id': 7,
                    'question': 'Mục tiêu nghề nghiệp của bạn là gì?',
                    'options': [
                        {'value': 'innovation', 'label': 'Sáng tạo và đổi mới', 'interests': ['sáng tạo', 'công nghệ']},
                        {'value': 'helping', 'label': 'Giúp đỡ cộng đồng', 'interests': ['giúp đỡ người khác', 'xã hội']},
                        {'value': 'wealth', 'label': 'Kiếm nhiều tiền', 'interests': ['kinh doanh', 'tài chính']},
                        {'value': 'expression', 'label': 'Thể hiện bản thân', 'interests': ['sáng tạo', 'nghệ thuật']}
                    ]
                },
                {
                    'id': 8,
                    'question': 'Bạn thích làm việc như thế nào?',
                    'options': [
                        {'value': 'team', 'label': 'Làm việc nhóm', 'interests': ['teamwork', 'giao tiếp']},
                        {'value': 'independent', 'label': 'Làm việc độc lập', 'interests': ['độc lập', 'tự chủ']},
                        {'value': 'leading', 'label': 'Lãnh đạo người khác', 'interests': ['lãnh đạo', 'quản lý']},
                        {'value': 'supporting', 'label': 'Hỗ trợ người khác', 'interests': ['giúp đỡ người khác', 'hỗ trợ']}
                    ]
                }
            ]
        }
    
    def get_questions(self, test_type='interest'):
        """Get test questions by type"""
        return self.questions.get(test_type, [])
    
    def evaluate_test(self, test_type, answers):
        """Evaluate test and return results"""
        # Collect all interests from answers
        interest_counts = {}
        all_interests = []
        
        questions = self.questions.get(test_type, [])
        
        for answer in answers:
            question_id = answer.get('question_id')
            selected_value = answer.get('value')
            
            # Find the question and option
            question = next((q for q in questions if q['id'] == question_id), None)
            if question:
                option = next((o for o in question['options'] if o['value'] == selected_value), None)
                if option and 'interests' in option:
                    for interest in option['interests']:
                        all_interests.append(interest)
                        interest_counts[interest] = interest_counts.get(interest, 0) + 1
        
        # Sort interests by frequency
        sorted_interests = sorted(interest_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Create interest text for recommendation
        interests_text = ' '.join(all_interests)
        
        # Get career recommendations
        try:
            recommendations = self.model.predict(interests_text, top_n=5)
        except:
            recommendations = []
        
        return {
            'scores': {
                'interests': sorted_interests[:5],  # Top 5 interests
                'interest_counts': {str(k): int(v) for k, v in interest_counts.items()}
            },
            'recommendations': recommendations
        }
