from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    from .auth import auth as auth_blueprint
    from .files import files as files_blueprint
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(files_blueprint)
    
    return app

    from .files import files as files_blueprint
    app.register_blueprint(files_blueprint, url_prefix="/files")

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/")

    return app

     
