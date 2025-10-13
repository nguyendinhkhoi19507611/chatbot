"""
Setup database with initial data
Creates admin user and indexes
"""

from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime

def setup_database():
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['career_chatbot']
    
    print("Setting up Career Chatbot Database...")
    print("=" * 60)
    
    # Create collections
    collections = ['users', 'conversations', 'test_results']
    for collection in collections:
        if collection not in db.list_collection_names():
            db.create_collection(collection)
            print(f"✓ Created collection: {collection}")
        else:
            print(f"✓ Collection already exists: {collection}")
    
    # Create indexes
    print("\nCreating indexes...")
    db.users.create_index('username', unique=True)
    db.users.create_index('email', unique=True)
    db.conversations.create_index('user_id')
    db.conversations.create_index('timestamp')
    db.test_results.create_index('user_id')
    print("✓ Indexes created")
    
    # Create admin user if not exists
    print("\nChecking admin user...")
    admin = db.users.find_one({'username': 'admin'})
    
    if not admin:
        admin_data = {
            'username': 'admin',
            'email': 'admin@careerchatbot.com',
            'password': generate_password_hash('admin123'),
            'full_name': 'Administrator',
            'role': 'admin',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'is_active': True,
            'profile': {
                'interests': [],
                'career_preferences': [],
                'test_results': []
            }
        }
        db.users.insert_one(admin_data)
        print("✓ Admin user created")
        print("  Username: admin")
        print("  Password: admin123")
        print("  ⚠ PLEASE CHANGE THE PASSWORD AFTER FIRST LOGIN!")
    else:
        print("✓ Admin user already exists")
    
    # Create test user if not exists
    print("\nChecking test user...")
    test_user = db.users.find_one({'username': 'testuser'})
    
    if not test_user:
        user_data = {
            'username': 'testuser',
            'email': 'test@careerchatbot.com',
            'password': generate_password_hash('test123'),
            'full_name': 'Test User',
            'role': 'user',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'is_active': True,
            'profile': {
                'interests': [],
                'career_preferences': [],
                'test_results': []
            }
        }
        db.users.insert_one(user_data)
        print("✓ Test user created")
        print("  Username: testuser")
        print("  Password: test123")
    else:
        print("✓ Test user already exists")
    
    print("\n" + "=" * 60)
    print("Database setup completed successfully!")
    print("=" * 60)
    
    # Display stats
    print("\nDatabase Statistics:")
    print(f"  Users: {db.users.count_documents({})}")
    print(f"  Conversations: {db.conversations.count_documents({})}")
    print(f"  Test Results: {db.test_results.count_documents({})}")
    
    client.close()

if __name__ == '__main__':
    try:
        setup_database()
    except Exception as e:
        print(f"\n❌ Error setting up database: {str(e)}")
        import traceback
        traceback.print_exc()
