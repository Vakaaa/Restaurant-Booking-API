from flask import Blueprint,jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity,get_jwt

me_bp = Blueprint("me",__name__)

@me_bp.get("/me")
@jwt_required
def me():
    user_id = get_jwt_identity()
    claims = get_jwt()
    return jsonify(user_id=user_id,role=claims.get("role")),200
