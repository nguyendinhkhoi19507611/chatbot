"""
Check if all requirements are met before running the app
"""
import os
import sys

print("="*60)
print("CAREER CHATBOT - SETUP CHECKER")
print("="*60)

# Check 1: Python version
print("\n1. Checking Python version...")
if sys.version_info >= (3, 8):
    print(f"   ✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
else:
    print(f"   ❌ Python version too old. Need 3.8+")

# Check 2: Required packages
print("\n2. Checking required packages...")
required_packages = ['flask', 'pymongo', 'sklearn', 'nltk', 'flask_cors', 'flask_jwt_extended']
for package in required_packages:
    try:
        __import__(package)
        print(f"   ✅ {package}")
    except ImportError:
        print(f"   ❌ {package} not installed")

# Check 3: MongoDB connection
print("\n3. Checking MongoDB connection...")
try:
    from pymongo import MongoClient
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
    client.admin.command('ping')
    print("   ✅ MongoDB is running and accessible")
    client.close()
except Exception as e:
    print(f"   ❌ MongoDB connection failed: {str(e)}")
    print("   📌 Make sure MongoDB is running!")
    print("   📌 Windows: net start MongoDB")
    print("   📌 Linux: sudo systemctl start mongod")
    print("   📌 Mac: brew services start mongodb-community")

# Check 4: AI Model files
print("\n4. Checking AI model files...")
model_dir = os.path.join(os.path.dirname(__file__), 'ai', 'models')
model_files = ['career_model.pkl', 'vectorizer.pkl', 'label_encoder.pkl']
all_models_exist = True
for file in model_files:
    file_path = os.path.join(model_dir, file)
    if os.path.exists(file_path):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} not found")
        all_models_exist = False

if not all_models_exist:
    print("\n   📌 Run: python ai/train_model.py")

# Check 5: Data files
print("\n5. Checking data files...")
data_files = [
    os.path.join('data', 'career_data.json'),
    os.path.join('data', 'training_data.json')
]
for file in data_files:
    file_path = os.path.join(os.path.dirname(__file__), file)
    if os.path.exists(file_path):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} not found")

# Check 6: Environment file
print("\n6. Checking configuration...")
env_file = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(env_file):
    print("   ✅ .env file exists")
else:
    print("   ⚠️  .env file not found (using defaults)")

print("\n" + "="*60)
print("Setup check complete!")
print("="*60)
print("\nIf all checks pass, you can run:")
print("  python run.py")
print("\n" + "="*60)
