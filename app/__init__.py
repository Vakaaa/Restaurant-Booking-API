from flask import Flask
from .extensions import db,login_manager,migrate,jwt,ma
from .config import Config
from app.routes import auth_bp,restaurant_bp


def create_app():
    

    app = Flask(__name__)

    app.config.from_object(Config)
    

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)
    ma.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(restaurant_bp)

    with app.app_context():
        from . import models

    return app
