# 🚀 Career Chatbot - Hướng dẫn cài đặt chi tiết

## Bước 1: Cài đặt môi trường

### 1.1. Cài đặt Python 3.8+

**Windows:**
- Download từ [python.org](https://www.python.org/downloads/)
- Chọn "Add Python to PATH" khi cài đặt

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Mac (với Homebrew)
brew install python3
```

### 1.2. Cài đặt Node.js 14+

**Windows:**
- Download từ [nodejs.org](https://nodejs.org/)

**Linux:**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Mac:**
```bash
brew install node
```

### 1.3. Cài đặt MongoDB

**Windows:**
- Download MongoDB Community Server từ [mongodb.com](https://www.mongodb.com/try/download/community)
- Cài đặt và chạy như service

**Linux:**
```bash
# Ubuntu/Debian
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

**Mac:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

Kiểm tra MongoDB đã chạy:
```bash
mongo --version
mongosh  # hoặc mongo
```

## Bước 2: Clone và Setup Project

### 2.1. Clone repository

```bash
git clone <repository-url>
cd career-chatbot
```

### 2.2. Setup Backend

```bash
cd backend

# Tạo virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Cài đặt dependencies
pip install -r requirements.txt

# Download NLTK data (optional nhưng khuyến khích)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

### 2.3. Cấu hình Backend

Tạo file `.env` trong thư mục `backend/`:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=my-super-secret-key-change-this-in-production
JWT_SECRET_KEY=my-jwt-secret-key-change-this-too
MONGO_URI=mongodb://localhost:27017/career_chatbot
CORS_ORIGINS=http://localhost:3000
PORT=5000
```

**⚠️ Quan trọng**: Thay đổi `SECRET_KEY` và `JWT_SECRET_KEY` trong production!

### 2.4. Setup Database

```bash
cd backend
python setup_db.py
```

Output sẽ hiển thị:
- Collections đã được tạo
- Indexes đã được tạo
- Admin user: `admin` / `admin123`
- Test user: `testuser` / `test123`

## Bước 3: Train AI Model

**🚨 BẮT BUỘC**: Phải train model trước khi chạy backend!

```bash
cd backend
python ai/train_model.py
```

Quá trình này sẽ:
1. Load 15+ nghề nghiệp và training data
2. Train Random Forest model
3. Evaluate với metrics (Accuracy, F1, Precision, Recall)
4. Lưu model vào `backend/ai/models/`

**Expected Output:**
```
╔══════════════════════════════════════════════════════════╗
║   CAREER CHATBOT - AI MODEL TRAINING SCRIPT             ║
║   Ứng dụng AI trong Chatbot tư vấn hướng nghiệp         ║
╚══════════════════════════════════════════════════════════╝

Loading data...
Loaded 33 training samples

Training set size: 26
Test set size: 7

Vectorizing text data...
Training Random Forest model...
Evaluating model...

MODEL EVALUATION RESULTS
Training Accuracy:   0.9615 (96.15%)
Test Accuracy:       0.8571 (85.71%)
Precision (weighted): 0.8571 (85.71%)
Recall (weighted):    0.8571 (85.71%)
F1 Score (weighted):  0.8571 (85.71%)

✅ Training completed successfully!
```

Nếu có lỗi:
- Kiểm tra Python version >= 3.8
- Kiểm tra tất cả dependencies đã được cài
- Xem log để debug

## Bước 4: Chạy Backend

```bash
cd backend

# Đảm bảo virtual environment đã được activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Run server
python run.py
```

**Output:**
```
============================================================
🚀 Career Chatbot Backend Server
============================================================
Server running on: http://localhost:5000
Health check: http://localhost:5000/health
Environment: development
============================================================

✓ AI model loaded successfully
✓ Loaded 15 careers
```

Kiểm tra backend đang chạy:
```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy",
  "message": "Career Chatbot API is running"
}
```

## Bước 5: Setup Frontend

Mở terminal mới (giữ backend đang chạy):

```bash
cd frontend

# Cài đặt dependencies
npm install

# Hoặc nếu có lỗi, thử:
npm install --legacy-peer-deps
```

### 5.1. Cấu hình Frontend

Tạo file `.env` trong thư mục `frontend/`:

```env
REACT_APP_API_URL=http://localhost:5000/api
```

## Bước 6: Chạy Frontend

```bash
cd frontend
npm start
```

Browser sẽ tự động mở `http://localhost:3000`

**Output:**
```
Compiled successfully!

You can now view career-chatbot-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

## Bước 7: Test Application

### 7.1. Login với Admin

1. Mở `http://localhost:3000`
2. Login với:
   - Username: `admin`
   - Password: `admin123`
3. Explore admin dashboard

### 7.2. Test Chatbot

1. Đi tới trang Chat
2. Thử các câu như:
   - "Xin chào"
   - "Tôi thích lập trình và công nghệ"
   - "Tôi muốn làm việc trong lĩnh vực sáng tạo"
   - "Cho tôi biết về nghề kỹ sư phần mềm"

### 7.3. Test Career Assessment

1. Đi tới trang "Bài test"
2. Trả lời 8 câu hỏi
3. Xem kết quả và đề xuất nghề nghiệp

### 7.4. Browse Careers

1. Đi tới trang "Nghề nghiệp"
2. Xem danh sách 15+ nghề nghiệp
3. Search và view details

## Troubleshooting

### Backend không khởi động

**Problem**: `ModuleNotFoundError`
```bash
# Solution:
cd backend
pip install -r requirements.txt
```

**Problem**: `MongoDB connection error`
```bash
# Solution: Kiểm tra MongoDB đang chạy
# Windows:
net start MongoDB

# Linux:
sudo systemctl start mongod

# Mac:
brew services start mongodb-community
```

**Problem**: `Model not found`
```bash
# Solution: Train model
cd backend
python ai/train_model.py
```

### Frontend không khởi động

**Problem**: `npm install` fails
```bash
# Solution:
npm install --legacy-peer-deps
# hoặc
npm cache clean --force
npm install
```

**Problem**: API calls fail (CORS error)
```bash
# Solution: Kiểm tra .env file
# Frontend .env:
REACT_APP_API_URL=http://localhost:5000/api

# Backend .env:
CORS_ORIGINS=http://localhost:3000
```

### Database issues

**Problem**: Collections not created
```bash
# Solution:
cd backend
python setup_db.py
```

**Problem**: Cannot login
```bash
# Solution: Reset database
mongosh
use career_chatbot
db.users.deleteMany({})
exit

cd backend
python setup_db.py
```

## Development Tips

### Hot Reload

- Backend: Tự động reload khi code thay đổi (Flask debug mode)
- Frontend: Tự động reload với React hot reload

### Debug Mode

Backend debug:
```python
# run.py
app.run(host='0.0.0.0', port=5000, debug=True)
```

Frontend debug:
- Mở Developer Tools (F12)
- Check Console và Network tab

### MongoDB GUI

Sử dụng MongoDB Compass để xem database:
- Download: https://www.mongodb.com/try/download/compass
- Connect to: `mongodb://localhost:27017`
- Database: `career_chatbot`

### API Testing

Sử dụng Postman hoặc curl:

```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Chat (với token)
curl -X POST http://localhost:5000/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message":"Tôi thích lập trình"}'
```

## Production Deployment

### Backend (Flask)

Sử dụng Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Frontend (React)

Build production:
```bash
cd frontend
npm run build
```

Serve với Nginx hoặc deploy lên Vercel, Netlify

### Database

Sử dụng MongoDB Atlas cho cloud database:
- https://www.mongodb.com/cloud/atlas
- Update `MONGO_URI` trong `.env`

## Next Steps

1. ✅ Thay đổi admin password
2. ✅ Thêm nhiều training data
3. ✅ Customize career data
4. ✅ Improve NLP responses
5. ✅ Add more features

## Support

Nếu gặp vấn đề:
1. Check logs trong terminal
2. Xem MongoDB logs
3. Check browser console
4. Read error messages carefully
5. Google the error
6. Ask for help

## Resources

- Flask: https://flask.palletsprojects.com/
- React: https://react.dev/
- MongoDB: https://www.mongodb.com/docs/
- scikit-learn: https://scikit-learn.org/
- Material-UI: https://mui.com/

---

**Good luck with your Career Chatbot! 🚀**
