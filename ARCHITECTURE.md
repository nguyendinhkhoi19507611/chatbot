# 🏗️ Career Chatbot - System Architecture

## System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                            │
│                                                                    │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌────────┐│
│  │  Login  │  │Register │  │  Chat   │  │ Careers │  │ Profile││
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └────────┘│
│  ┌─────────┐  ┌──────────────────────────────────────┐          │
│  │  Test   │  │         Admin Dashboard               │          │
│  └─────────┘  └──────────────────────────────────────┘          │
│                                                                    │
│                     React 18 + Material-UI                        │
└────────────────────────────┬───────────────────────────────────┘
                             │
                             │ REST API (Axios)
                             │ JWT Authentication
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                        BACKEND SERVER                             │
│                                                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    Flask Application                         │ │
│  │                                                               │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │ │
│  │  │   Auth   │  │ Chatbot  │  │ Careers  │  │   Admin    │  │ │
│  │  │  Routes  │  │  Routes  │  │  Routes  │  │   Routes   │  │ │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └─────┬──────┘  │ │
│  │       │             │             │              │          │ │
│  │  ┌────┴──────────────┴──────────────┴──────────────┴─────┐  │ │
│  │  │                Service Layer                           │  │ │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │  │ │
│  │  │  │ Chatbot  │  │ Career   │  │   Test   │            │  │ │
│  │  │  │ Service  │  │ Service  │  │ Service  │            │  │ │
│  │  │  └────┬─────┘  └────┬─────┘  └────┬─────┘            │  │ │
│  │  └───────┼──────────────┼──────────────┼─────────────────┘  │ │
│  └──────────┼──────────────┼──────────────┼────────────────────┘ │
│             │              │              │                       │
│    ┌────────▼──────┐  ┌────▼────────┐  ┌─▼────────────────┐    │
│    │   AI/ML       │  │  Database   │  │   Models         │    │
│    │   Module      │  │  Operations │  │   (MongoDB)      │    │
│    │               │  │             │  │                  │    │
│    │ ┌───────────┐ │  │ ┌─────────┐ │  │ ┌──────────────┐ │    │
│    │ │ Career    │ │  │ │  User   │ │  │ │ User Model   │ │    │
│    │ │ Model     │ │  │ │  CRUD   │ │  │ └──────────────┘ │    │
│    │ │ (ML)      │ │  │ └─────────┘ │  │ ┌──────────────┐ │    │
│    │ └───────────┘ │  │ ┌─────────┐ │  │ │ Conversation │ │    │
│    │               │  │ │  Conv   │ │  │ │ Model        │ │    │
│    │ ┌───────────┐ │  │ │  CRUD   │ │  │ └──────────────┘ │    │
│    │ │ Chatbot   │ │  │ └─────────┘ │  │ ┌──────────────┐ │    │
│    │ │ NLP       │ │  │ ┌─────────┐ │  │ │ Test Result  │ │    │
│    │ │           │ │  │ │  Test   │ │  │ │ Model        │ │    │
│    │ └───────────┘ │  │ │  CRUD   │ │  │ └──────────────┘ │    │
│    └───────────────┘  │ └─────────┘ │  └──────────────────┘    │
│                       └─────────────┘                           │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │    MongoDB      │
                   │                 │
                   │  ┌───────────┐  │
                   │  │   users   │  │
                   │  ├───────────┤  │
                   │  │conversations│
                   │  ├───────────┤  │
                   │  │test_results│ │
                   │  └───────────┘  │
                   └─────────────────┘
```

## Component Details

### Frontend Architecture

```
frontend/src/
│
├── pages/
│   ├── LoginPage.js         → Login form + validation
│   ├── RegisterPage.js      → Registration form
│   ├── ChatPage.js          → Chat interface with AI
│   ├── CareersPage.js       → Career catalog + search
│   ├── TestPage.js          → Assessment test flow
│   ├── ProfilePage.js       → User profile + stats
│   └── AdminPage.js         → Admin dashboard
│
├── components/
│   └── Navbar.js            → Navigation bar
│
├── services/
│   └── api.js               → API client (Axios)
│                             - Auth interceptor
│                             - Token refresh
│                             - Error handling
│
├── utils/
│   └── auth.js              → Auth utilities
│                             - Token management
│                             - JWT decode
│                             - User session
│
└── App.js                   → Routing + Theme
```

### Backend Architecture

```
backend/
│
├── ai/
│   ├── career_model.py      → ML Model
│   │                         - RandomForestClassifier
│   │                         - TF-IDF Vectorizer
│   │                         - Training & Evaluation
│   │
│   ├── chatbot_nlp.py       → NLP Chatbot
│   │                         - Intent detection
│   │                         - Interest extraction
│   │                         - Response generation
│   │
│   ├── train_model.py       → Training script
│   │                         - Data loading
│   │                         - Model training
│   │                         - Metrics calculation
│   │
│   └── models/              → Saved models
│       ├── career_model.pkl
│       ├── vectorizer.pkl
│       └── label_encoder.pkl
│
├── app/
│   ├── __init__.py          → App factory
│   │                         - Extensions init
│   │                         - Blueprint registration
│   │
│   ├── models/              → Database models
│   │   ├── user.py
│   │   ├── conversation.py
│   │   └── test_result.py
│   │
│   ├── routes/              → API endpoints
│   │   ├── auth.py          → /api/auth/*
│   │   ├── chatbot.py       → /api/chatbot/*
│   │   ├── career.py        → /api/careers/*
│   │   ├── user.py          → /api/user/*
│   │   └── admin.py         → /api/admin/*
│   │
│   └── services/            → Business logic
│       ├── chatbot_service.py
│       ├── career_service.py
│       └── test_service.py
│
├── data/
│   ├── career_data.json     → Career information
│   └── training_data.json   → Training samples
│
├── config.py                → Configuration
└── run.py                   → Application entry
```

## Data Flow

### 1. User Authentication Flow

```
User Input (Login Form)
         │
         ▼
  Frontend Validation
         │
         ▼
  POST /api/auth/login
         │
         ▼
  Backend Auth Route
         │
         ├─→ Find User in DB
         ├─→ Verify Password (bcrypt)
         └─→ Generate JWT Tokens
         │
         ▼
  Return tokens + user data
         │
         ▼
  Store in localStorage
         │
         ▼
  Redirect to Chat Page
```

### 2. Chat Conversation Flow

```
User Message
      │
      ▼
POST /api/chatbot/chat
      │
      ▼
Chatbot Service
      ├─→ NLP Processing
      │   ├─→ Intent Detection
      │   ├─→ Interest Extraction
      │   └─→ Response Generation
      │
      ├─→ AI Model Prediction
      │   ├─→ TF-IDF Vectorization
      │   ├─→ Random Forest Predict
      │   └─→ Get Top 3 Careers
      │
      └─→ Save Conversation to DB
      │
      ▼
Return response + recommendations
      │
      ▼
Display in Chat UI
```

### 3. Career Test Flow

```
Load Questions
      │
      ▼
User Answers Questions (8 questions)
      │
      ▼
POST /api/user/test/submit
      │
      ▼
Test Service
      ├─→ Extract Interests from Answers
      ├─→ Count Interest Frequency
      ├─→ Create Interest Text
      │
      ├─→ AI Model Prediction
      │   └─→ Get Top 5 Careers
      │
      └─→ Save Results to DB
      │
      ▼
Return recommendations
      │
      ▼
Display Results Page
```

### 4. Admin Dashboard Flow

```
Admin Login
      │
      ▼
Check Admin Role (JWT)
      │
      ▼
GET /api/admin/stats
      │
      ├─→ Count Users
      ├─→ Count Active Users
      ├─→ Count Conversations
      └─→ Count Tests
      │
      ▼
GET /api/admin/users
      │
      └─→ List All Users
      │
      ▼
Display Dashboard
```

## Security Architecture

```
┌─────────────────────────────────────────┐
│         Security Layers                  │
├─────────────────────────────────────────┤
│                                          │
│  1. Frontend                             │
│     ├─→ Input Validation                │
│     ├─→ Protected Routes                │
│     └─→ Token Storage (localStorage)    │
│                                          │
│  2. Network                              │
│     ├─→ HTTPS (Production)              │
│     ├─→ CORS Policy                     │
│     └─→ JWT Bearer Token                │
│                                          │
│  3. Backend                              │
│     ├─→ JWT Verification                │
│     ├─→ Route Protection                │
│     ├─→ Role-based Access (RBAC)        │
│     └─→ Input Sanitization              │
│                                          │
│  4. Database                             │
│     ├─→ Password Hashing (bcrypt)       │
│     ├─→ Indexed Queries                 │
│     └─→ Data Validation                 │
│                                          │
└─────────────────────────────────────────┘
```

## ML Model Architecture

```
┌─────────────────────────────────────────┐
│      Career Recommendation Model         │
├─────────────────────────────────────────┤
│                                          │
│  Input: User text (interests)            │
│           │                              │
│           ▼                              │
│  ┌──────────────────┐                   │
│  │  Preprocessing   │                   │
│  │  - Lowercase     │                   │
│  │  - Remove punct  │                   │
│  └────────┬─────────┘                   │
│           │                              │
│           ▼                              │
│  ┌──────────────────┐                   │
│  │ TF-IDF Vectorizer│                   │
│  │ - max_features=100│                  │
│  │ - ngram_range=(1,2)│                 │
│  └────────┬─────────┘                   │
│           │                              │
│           ▼                              │
│  ┌──────────────────┐                   │
│  │ Random Forest    │                   │
│  │ - n_estimators=100│                  │
│  │ - max_depth=10   │                   │
│  └────────┬─────────┘                   │
│           │                              │
│           ▼                              │
│  ┌──────────────────┐                   │
│  │ Predict Proba    │                   │
│  │ - Get confidence │                   │
│  │ - Top N careers  │                   │
│  └────────┬─────────┘                   │
│           │                              │
│           ▼                              │
│  Output: Career recommendations          │
│         + Confidence scores              │
│                                          │
└─────────────────────────────────────────┘
```

## Database Schema

```
┌────────────────────────────────────────────┐
│              USERS                          │
├────────────────────────────────────────────┤
│ _id: ObjectId (PK)                         │
│ username: String (unique, indexed)         │
│ email: String (unique, indexed)            │
│ password: String (hashed)                  │
│ full_name: String                          │
│ role: String (user/admin)                  │
│ created_at: DateTime                       │
│ updated_at: DateTime                       │
│ is_active: Boolean                         │
│ profile: {                                 │
│   interests: Array                         │
│   career_preferences: Array                │
│   test_results: Array                      │
│ }                                          │
└────────────────────────────────────────────┘
          │
          │ 1:N
          │
          ▼
┌────────────────────────────────────────────┐
│          CONVERSATIONS                      │
├────────────────────────────────────────────┤
│ _id: ObjectId (PK)                         │
│ user_id: ObjectId (FK, indexed)            │
│ message: String                            │
│ response: String                           │
│ intent: String                             │
│ recommendations: Array                     │
│ timestamp: DateTime (indexed)              │
└────────────────────────────────────────────┘

┌────────────────────────────────────────────┐
│          TEST_RESULTS                       │
├────────────────────────────────────────────┤
│ _id: ObjectId (PK)                         │
│ user_id: ObjectId (FK, indexed)            │
│ test_type: String                          │
│ answers: Array                             │
│ results: Object                            │
│ recommendations: Array                     │
│ created_at: DateTime                       │
└────────────────────────────────────────────┘
```

## Deployment Architecture

### Development

```
┌──────────────┐     ┌──────────────┐
│   Frontend   │     │   Backend    │
│  localhost   │────▶│  localhost   │
│   :3000      │     │    :5000     │
└──────────────┘     └───────┬──────┘
                             │
                             ▼
                     ┌──────────────┐
                     │   MongoDB    │
                     │  localhost   │
                     │   :27017     │
                     └──────────────┘
```

### Production (Recommended)

```
┌──────────────────────┐
│   Domain/CDN         │
│   (Vercel/Netlify)   │
│   Frontend Build     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Load Balancer      │
│   (Nginx)            │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Backend Server     │
│   (Gunicorn+Flask)   │
│   Multiple Workers   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   MongoDB Atlas      │
│   (Cloud Database)   │
└──────────────────────┘
```

## Technology Stack Diagram

```
┌─────────────────────────────────────────────────────┐
│                    FRONTEND                          │
│  ┌────────────────────────────────────────────┐    │
│  │  React 18.2 + React Router 6.15           │    │
│  ├────────────────────────────────────────────┤    │
│  │  Material-UI 5.14 (Components)            │    │
│  ├────────────────────────────────────────────┤    │
│  │  Axios 1.5 (HTTP Client)                  │    │
│  ├────────────────────────────────────────────┤    │
│  │  JWT Decode (Auth)                        │    │
│  └────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                    BACKEND                           │
│  ┌────────────────────────────────────────────┐    │
│  │  Flask 2.3.3 (Web Framework)              │    │
│  ├────────────────────────────────────────────┤    │
│  │  Flask-JWT-Extended (Auth)                │    │
│  ├────────────────────────────────────────────┤    │
│  │  Flask-PyMongo (Database)                 │    │
│  ├────────────────────────────────────────────┤    │
│  │  Flask-CORS (API)                         │    │
│  └────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                    AI/ML                             │
│  ┌────────────────────────────────────────────┐    │
│  │  scikit-learn 1.3 (ML)                    │    │
│  ├────────────────────────────────────────────┤    │
│  │  TensorFlow 2.13 (Deep Learning)          │    │
│  ├────────────────────────────────────────────┤    │
│  │  NLTK 3.8 (NLP)                           │    │
│  ├────────────────────────────────────────────┤    │
│  │  NumPy + Pandas (Data Processing)         │    │
│  └────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                   DATABASE                           │
│  ┌────────────────────────────────────────────┐    │
│  │  MongoDB 4.4+ (NoSQL)                     │    │
│  ├────────────────────────────────────────────┤    │
│  │  PyMongo (Driver)                         │    │
│  └────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

---

This architecture enables:
- ✅ Scalability
- ✅ Maintainability  
- ✅ Security
- ✅ Performance
- ✅ Testability
