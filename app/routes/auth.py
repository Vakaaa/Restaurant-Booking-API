from flask import Blueprint, request, jsonify 
from flask_jwt_extended import jwt_required, get_jwt_identity  

from app.schemas.auth_schema import RegisterSchema,LoginSchema
from app.services.auth_service import AuthService


auth_bp = Blueprint("auth",__name__)

@auth_bp.route("/register",methods=["POST"])
def register():
    data = request.get_json() or {}
    errors = RegisterSchema().validate(data)
    if errors:
        return jsonify({"errors":errors}),400
    user,error,status_code = AuthService.register(
        full_name=data["full_name"],
        email=data["email"],
        password=data["password"]
    )
    if error:
        return jsonify(error),status_code

    return jsonify({
        "message":"User saccessfully registered",
        "user":user.to_dict()
    }),status_code

@auth_bp.route("/login",methods=["POST"])
def login():
    data = request.get_json() or {}
    errors = LoginSchema().validate(data)
    if errors:
        return jsonify({"errors":errors}),400
    result,error,status_code = AuthService.login(
        email=data["email"],
        password = data["password"]
    )
    if error:
        return jsonify(error),status_code
    
    return jsonify(result),status_code

@auth_bp.route("/me",methods=["POST"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = AuthService.get_user_by_id(int(user_id))
    if not user:
        return jsonify({"error":"User not found"}),404
    return user.to_dict(),200
    