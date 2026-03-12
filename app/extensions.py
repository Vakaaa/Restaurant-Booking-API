from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
login_manager = LoginManager()
#login_manager.login_view("auth.login")
migrate = Migrate()
csrf = CSRFProtect()
jwt = JWTManager()