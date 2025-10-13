"""
Run Flask application
"""

import os
from app import create_app

# Create app
app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("\n" + "="*60)
    print("🚀 Career Chatbot Backend Server")
    print("="*60)
    print(f"Server running on: http://localhost:{port}")
    print(f"Health check: http://localhost:{port}/health")
    print(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=True)
