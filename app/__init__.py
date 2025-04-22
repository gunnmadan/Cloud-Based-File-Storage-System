from flask import Flask
from .config import Config
from .extensions import db, login_manager  

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

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

