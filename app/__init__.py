from flask import Flask
from .extensions import db,login_manager,migrate,csrf,jwt
from .config import Config
from .routes import blueprint_register

def create_app():
    

    app = Flask(__name__)

    app.config.from_object(Config)
    

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)
    csrf.init_app(app)
    jwt.init_app(app)

    blueprint_register(app)

    with app.app_context():
        from . import models

    return app
