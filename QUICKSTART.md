# ⚡ Quick Start Guide - Career Chatbot

Hướng dẫn nhanh để chạy Career Chatbot trong 5 phút!

## Prerequisites

- ✅ Python 3.8+ đã cài đặt
- ✅ Node.js 14+ đã cài đặt  
- ✅ MongoDB đang chạy

## Quick Commands

### 1️⃣ Backend Setup (Terminal 1)

```bash
# Clone và đi vào thư mục
cd career-chatbot/backend

# Setup Python environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Setup database
python setup_db.py

# Train AI model (REQUIRED!)
python ai/train_model.py

# Run backend
python run.py
```

**Backend running at**: `http://localhost:5000` ✅

### 2️⃣ Frontend Setup (Terminal 2)

```bash
# Đi vào thư mục frontend
cd career-chatbot/frontend

# Install dependencies
npm install

# Run frontend
npm start
```

**Frontend running at**: `http://localhost:3000` ✅

## 🎉 Test the App

### Login Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Test User:**
- Username: `testuser`
- Password: `test123`

### Try These Features

1. **💬 Chat with AI**
   - Go to Chat page
   - Try: "Tôi thích lập trình và công nghệ"
   - See career recommendations!

2. **📝 Take Career Test**
   - Go to Test page
   - Answer 8 questions
   - Get personalized career suggestions

3. **💼 Browse Careers**
   - Go to Careers page
   - Search and explore 15+ careers

4. **🛠️ Admin Dashboard** (login as admin)
   - View statistics
   - Manage users
   - Monitor conversations

## Common Issues

### Backend won't start?
```bash
# Make sure MongoDB is running
# Windows: 
net start MongoDB

# Check if model is trained
ls backend/ai/models/  # Should see .pkl files
```

### Frontend won't start?
```bash
# Try clean install
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Can't login?
```bash
# Reset database
cd backend
python setup_db.py
```

## What's Next?

✅ Explore all features
✅ Add more career data in `backend/data/career_data.json`
✅ Improve training with more samples
✅ Customize UI/UX
✅ Deploy to production

## Need Help?

📖 Read full documentation: [README.md](README.md)
📖 Detailed setup guide: [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

**Happy coding! 🚀**
