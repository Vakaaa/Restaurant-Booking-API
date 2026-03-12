from .auth import auth_bp


def blueprint_register(app):
    app.register_blueprint(auth_bp) 