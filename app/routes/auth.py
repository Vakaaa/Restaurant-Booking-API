from flask import Blueprint,request,jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from models.user import User


auth_bp = Blueprint("auth",__name__,url_prefix="/auth")


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = request.get("email")
    password = request.get("password")

    if not email or not password:
        return jsonify({"msg":"email and password required"}),400
    
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash,password):
        return jsonify({"msg":"bad credentials"}),401
    

    acces_token = create_access_token(identity=user.id,additional_claims={"role":user.role})
    return jsonify(acces_token=acces_token),200