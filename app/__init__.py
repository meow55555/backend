from flask import Flask
from .database import db
from .config import configs
from .user_helper import login_manager

def create_app(env):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(configs[env])

    db.init_app(app)
    login_manager.init_app(app)
    
    # Blueprint
    from .main import main_bp
    app.register_blueprint(main_bp)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)

    from .api import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app