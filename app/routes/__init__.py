from .auth import auth_bp
from .me import me_bp

def blueprint_register(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(me_bp)