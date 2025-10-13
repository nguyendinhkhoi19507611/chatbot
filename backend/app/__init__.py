"""
Flask Application Factory
"""

from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from config import config

# Initialize extensions
mongo = PyMongo()
jwt = JWTManager()

def create_app(config_name='default'):
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    CORS(
        app,
        resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        expose_headers=["Content-Type", "Authorization"]
    )
    mongo.init_app(app)
    jwt.init_app(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.chatbot import chatbot_bp
    from app.routes.career import career_bp
    from app.routes.user import user_bp
    from app.routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')
    app.register_blueprint(career_bp, url_prefix='/api/careers')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    # Health check route
    @app.route('/health')
    def health_check():
        try:
            # Check MongoDB connection
            mongo.db.command('ping')
            return {'status': 'healthy', 'message': 'Career Chatbot API is running', 'database': 'connected'}
        except Exception as e:
            return {'status': 'unhealthy', 'message': str(e), 'database': 'disconnected'}, 500
    
    return app
