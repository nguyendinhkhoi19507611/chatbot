# 🤖 Career Chatbot - Tư vấn hướng nghiệp AI

Ứng dụng trí tuệ nhân tạo trong Chatbot tư vấn hướng nghiệp cá nhân dựa vào sở thích, sử dụng Natural Language Processing (NLP) và Machine Learning.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![React](https://img.shields.io/badge/React-18.2.0-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Latest-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Mục lục

- [Tổng quan](#tổng-quan)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Cài đặt và chạy](#cài-đặt-và-chạy)
- [Tính năng](#tính-năng)
- [API Documentation](#api-documentation)
- [Đào tạo mô hình AI](#đào-tạo-mô-hình-ai)
- [Screenshots](#screenshots)

## 🎯 Tổng quan

Career Chatbot là một ứng dụng web thông minh giúp người dùng tìm kiếm hướng nghiệp phù hợp dựa trên sở thích và năng lực cá nhân. Hệ thống sử dụng AI/ML để phân tích câu trả lời của người dùng và đưa ra các gợi ý nghề nghiệp chính xác.

### Điểm nổi bật

- 🤖 **Chatbot AI thông minh**: Sử dụng NLP để hiểu ngôn ngữ tự nhiên
- 🎯 **Đề xuất nghề nghiệp chính xác**: Machine Learning với độ chính xác cao
- 📊 **Bài test đánh giá sở thích**: Hệ thống câu hỏi khoa học
- 📈 **Theo dõi lịch sử**: Lưu trữ và phân tích quá trình tư vấn
- 🎨 **Giao diện đẹp mắt**: UI/UX hiện đại với Material-UI
- 🔐 **Bảo mật**: JWT authentication, password hashing

## 🛠️ Công nghệ sử dụng

### Backend
- **Framework**: Flask 2.3.3
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **AI/ML Libraries**:
  - TensorFlow 2.13.0
  - scikit-learn 1.3.0
  - NLTK 3.8.1
  - spaCy 3.6.1
- **NLP**: Custom chatbot với TF-IDF và cosine similarity

### Frontend
- **Framework**: React 18.2.0
- **Routing**: React Router 6.15.0
- **UI Library**: Material-UI (MUI) 5.14.5
- **HTTP Client**: Axios 1.5.0
- **Markdown**: React Markdown 8.0.7

### Machine Learning Model
- **Algorithm**: Random Forest Classifier
- **Feature Extraction**: TF-IDF Vectorizer
- **Metrics**: Accuracy, Precision, Recall, F1 Score
- **Training Data**: 15+ careers với hàng chục mẫu training

## 📁 Cấu trúc dự án

```
career-chatbot/
├── backend/                    # Flask Backend
│   ├── ai/                    # AI/ML Components
│   │   ├── career_model.py    # ML model for career recommendation
│   │   ├── chatbot_nlp.py     # NLP chatbot
│   │   ├── train_model.py     # Training script
│   │   └── models/            # Trained models (generated)
│   ├── app/
│   │   ├── __init__.py        # Flask app factory
│   │   ├── models/            # Database models
│   │   │   ├── user.py
│   │   │   ├── conversation.py
│   │   │   └── test_result.py
│   │   ├── routes/            # API routes
│   │   │   ├── auth.py
│   │   │   ├── chatbot.py
│   │   │   ├── career.py
│   │   │   ├── user.py
│   │   │   └── admin.py
│   │   └── services/          # Business logic
│   │       ├── chatbot_service.py
│   │       ├── career_service.py
│   │       └── test_service.py
│   ├── data/                  # Training data
│   │   ├── career_data.json
│   │   └── training_data.json
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
├── frontend/                   # React Frontend
│   ├── public/
│   ├── src/
│   │   ├── components/        # React components
│   │   │   └── Navbar.js
│   │   ├── pages/             # Page components
│   │   │   ├── LoginPage.js
│   │   │   ├── RegisterPage.js
│   │   │   ├── ChatPage.js
│   │   │   ├── CareersPage.js
│   │   │   ├── TestPage.js
│   │   │   ├── ProfilePage.js
│   │   │   └── AdminPage.js
│   │   ├── services/          # API services
│   │   │   └── api.js
│   │   ├── utils/             # Utilities
│   │   │   └── auth.js
│   │   ├── styles/            # CSS
│   │   │   └── index.css
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── package-lock.json
└── README.md
```

## 🚀 Cài đặt và chạy

### Yêu cầu hệ thống

- Python 3.8+
- Node.js 14+
- MongoDB 4.4+
- pip và npm

### 1. Clone repository

```bash
git clone <repository-url>
cd career-chatbot
```

### 2. Cài đặt Backend

```bash
cd backend

# Tạo virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt

# Download NLTK data (optional)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 3. Cấu hình MongoDB

Đảm bảo MongoDB đã được cài đặt và chạy:

```bash
# Khởi động MongoDB
mongod

# Hoặc với MongoDB service
sudo service mongod start
```

Tạo file `.env` trong thư mục `backend/`:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
MONGO_URI=mongodb://localhost:27017/career_chatbot
CORS_ORIGINS=http://localhost:3000
PORT=5000
```

### 4. Train AI Model

**Bước quan trọng**: Phải train model trước khi chạy backend!

```bash
cd backend
python ai/train_model.py
```

Output sẽ hiển thị:
- Training progress
- Model metrics (Accuracy, Precision, Recall, F1 Score)
- Test predictions
- Model saved to `backend/ai/models/`

### 5. Chạy Backend

```bash
cd backend
python run.py
```

Backend sẽ chạy tại: `http://localhost:5000`

### 6. Cài đặt Frontend

Mở terminal mới:

```bash
cd frontend

# Cài đặt dependencies
npm install

# Tạo file .env
echo "REACT_APP_API_URL=http://localhost:5000/api" > .env
```

### 7. Chạy Frontend

```bash
cd frontend
npm start
```

Frontend sẽ chạy tại: `http://localhost:3000`

## ✨ Tính năng

### 1. Chức năng người dùng

#### 🔐 Xác thực
- Đăng ký tài khoản mới
- Đăng nhập với username/email
- JWT authentication với auto-refresh
- Bảo mật mật khẩu với bcrypt

#### 💬 Chat với Chatbot
- Giao diện chat hiện đại
- NLP để hiểu ngôn ngữ tự nhiên (tiếng Việt)
- Tự động nhận diện intent (greeting, farewell, help, career_info...)
- Đề xuất nghề nghiệp dựa trên sở thích
- Lưu trữ lịch sử trò chuyện
- Gợi ý câu hỏi phổ biến

#### 📝 Bài test đánh giá
- 8 câu hỏi đánh giá sở thích
- Progress tracking
- Phân tích kết quả tự động
- Đề xuất top 5 nghề nghiệp phù hợp với độ tin cậy

#### 💼 Thông tin nghề nghiệp
- Danh sách 15+ nghề nghiệp
- Tìm kiếm nghề nghiệp
- Xem chi tiết: mô tả, mức lương, học vấn, kỹ năng
- Lộ trình phát triển nghề nghiệp

#### 👤 Hồ sơ cá nhân
- Xem thông tin tài khoản
- Lịch sử làm bài test
- Thống kê hoạt động

### 2. Chức năng quản trị (Admin)

#### 📊 Dashboard
- Thống kê tổng quan:
  - Tổng số người dùng
  - Người dùng hoạt động
  - Số lượng cuộc trò chuyện
  - Số lượng bài test đã làm
- Biểu đồ và metrics

#### 👥 Quản lý người dùng
- Xem danh sách người dùng
- Xem chi tiết tài khoản
- Vô hiệu hóa tài khoản

#### 💬 Theo dõi hoạt động
- Xem lịch sử trò chuyện
- Phân tích intent
- Đánh giá chất lượng phản hồi

## 📚 API Documentation

### Authentication Endpoints

#### POST `/api/auth/register`
Đăng ký tài khoản mới

**Request:**
```json
{
  "username": "user123",
  "email": "user@example.com",
  "password": "password123",
  "full_name": "Nguyen Van A"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {...},
  "access_token": "...",
  "refresh_token": "..."
}
```

#### POST `/api/auth/login`
Đăng nhập

**Request:**
```json
{
  "username": "user123",
  "password": "password123"
}
```

#### GET `/api/auth/me`
Lấy thông tin user hiện tại (requires auth)

### Chatbot Endpoints

#### POST `/api/chatbot/chat`
Gửi tin nhắn tới chatbot (requires auth)

**Request:**
```json
{
  "message": "Tôi thích lập trình và công nghệ"
}
```

**Response:**
```json
{
  "response": "Dựa trên sở thích của bạn...",
  "intent": "interests_query",
  "confidence": 0.95,
  "recommendations": [...]
}
```

#### GET `/api/chatbot/history`
Lấy lịch sử trò chuyện (requires auth)

#### DELETE `/api/chatbot/history`
Xóa lịch sử trò chuyện (requires auth)

### Career Endpoints

#### GET `/api/careers`
Lấy danh sách nghề nghiệp

#### GET `/api/careers/{id}`
Lấy chi tiết nghề nghiệp

#### GET `/api/careers/search?q={query}`
Tìm kiếm nghề nghiệp

#### POST `/api/careers/recommend`
Đề xuất nghề nghiệp (requires auth)

### User Endpoints

#### GET `/api/user/profile`
Lấy hồ sơ người dùng (requires auth)

#### PUT `/api/user/profile`
Cập nhật hồ sơ (requires auth)

#### GET `/api/user/test/questions`
Lấy câu hỏi bài test (requires auth)

#### POST `/api/user/test/submit`
Nộp bài test (requires auth)

#### GET `/api/user/test/results`
Lấy kết quả bài test (requires auth)

### Admin Endpoints

#### GET `/api/admin/users`
Lấy danh sách người dùng (requires admin)

#### GET `/api/admin/stats`
Lấy thống kê hệ thống (requires admin)

#### POST `/api/admin/users/{id}/deactivate`
Vô hiệu hóa người dùng (requires admin)

## 🧠 Đào tạo mô hình AI

### Thuật toán

Hệ thống sử dụng **Random Forest Classifier** kết hợp với **TF-IDF Vectorizer** để:

1. Trích xuất đặc trưng từ văn bản (sở thích người dùng)
2. Phân loại và đề xuất nghề nghiệp phù hợp
3. Tính toán độ tin cậy cho mỗi đề xuất

### Training Process

```bash
cd backend
python ai/train_model.py
```

**Quá trình training:**

1. Load dữ liệu từ `career_data.json` và `training_data.json`
2. Preprocessing và augmentation data
3. TF-IDF vectorization
4. Train Random Forest với 100 estimators
5. Evaluate với train/test split (80/20)
6. Lưu model, vectorizer, label encoder

### Model Metrics

Model được đánh giá bằng các metrics:

- **Accuracy**: Độ chính xác tổng thể
- **Precision**: Độ chính xác của dự đoán positive
- **Recall**: Khả năng tìm ra các positive
- **F1 Score**: Trung bình điều hòa của Precision và Recall

**Expected Performance:**
- Training Accuracy: ~95-100%
- Test Accuracy: ~85-95%
- F1 Score: ~85-95%

### Cải thiện Model

Để cải thiện độ chính xác:

1. Thêm training data vào `backend/data/training_data.json`
2. Thêm nghề nghiệp mới vào `backend/data/career_data.json`
3. Chạy lại training script
4. Theo dõi metrics và confusion matrix

### Tích hợp Model Free

Hệ thống có thể tích hợp các model pre-trained:

```python
# Trong backend/ai/chatbot_nlp.py
from transformers import pipeline

# Sentiment analysis
sentiment = pipeline("sentiment-analysis")

# Text generation
generator = pipeline("text-generation", model="gpt2")
```

## 🎨 Screenshots

### Chat Interface
Giao diện chat với AI, hiển thị đề xuất nghề nghiệp real-time

### Career Test
Bài test 8 câu hỏi với progress tracking và kết quả chi tiết

### Career Catalog
Danh sách nghề nghiệp với tìm kiếm và filter

### Admin Dashboard
Thống kê và quản lý hệ thống

## 🔧 Configuration

### Backend Configuration

File `backend/config.py`:
- Flask settings
- MongoDB URI
- JWT configuration
- CORS settings
- Model paths

### Frontend Configuration

File `frontend/.env`:
- API endpoint URL
- Environment settings

## 📊 Database Schema

### Users Collection
```javascript
{
  _id: ObjectId,
  username: String,
  email: String,
  password: String (hashed),
  full_name: String,
  role: String, // 'user' or 'admin'
  created_at: DateTime,
  updated_at: DateTime,
  is_active: Boolean,
  profile: {
    interests: Array,
    career_preferences: Array,
    test_results: Array
  }
}
```

### Conversations Collection
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  message: String,
  response: String,
  intent: String,
  recommendations: Array,
  timestamp: DateTime
}
```

### Test Results Collection
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  test_type: String,
  answers: Array,
  results: Object,
  recommendations: Array,
  created_at: DateTime
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Career Chatbot - AI-powered Career Counseling System

## 🙏 Acknowledgments

- TensorFlow & scikit-learn teams
- Flask & React communities
- Material-UI team
- MongoDB team

## 📧 Contact

For questions or support, please contact: [your-email@example.com]

---

**Lưu ý**: Đây là project học tập và nghiên cứu. Để sử dụng trong production, cần cải thiện thêm về security, scalability, và error handling.

## 🔄 Future Improvements

- [ ] Thêm nhiều nghề nghiệp hơn
- [ ] Tích hợp GPT/LLM cho chatbot thông minh hơn
- [ ] Thêm voice chat
- [ ] Mobile app (React Native)
- [ ] Recommendation system nâng cao
- [ ] A/B testing cho UI/UX
- [ ] Analytics dashboard chi tiết hơn
- [ ] Export báo cáo PDF
- [ ] Multi-language support
- [ ] Social login (Google, Facebook)
