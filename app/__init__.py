from flask import Flask
<<<<<<< HEAD
from .config import Config
from .extensions import db, login_manager  
=======
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
>>>>>>> miracle/main

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
<<<<<<< HEAD

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/")

    from .files import files as files_blueprint
    app.register_blueprint(files_blueprint, url_prefix="/files")

    return app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

=======
    
    from .auth import auth as auth_blueprint
    from .files import files as files_blueprint
    
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(files_blueprint)
    
    return app
>>>>>>> miracle/main
