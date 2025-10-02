from flask import Flask
from dotenv import load_dotenv
import os

def create_app():
    """Create and configure the Flask application."""
    load_dotenv()  # Load environment variables from .env file

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Import and register the blueprint
    from . import routes
    app.register_blueprint(routes.main_bp)

    return app