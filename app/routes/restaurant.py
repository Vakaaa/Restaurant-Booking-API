from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schemas.restaurant_schema import RestaurantSchema
from marshmallow import ValidationError

from app.models.user import User
from app.services.restaurant_service import RestaurantService


restaurant_bp = Blueprint("restaurant",__name__,url_prefix="/restaurants")


def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)


def admin_required():
    current_user = get_current_user()
    if not current_user or current_user.role != "admin":
        return None,{"error":"Forbidden"},403
    return current_user,None,None


@restaurant_bp.route("",methods=["POST"])
@jwt_required()
def create_restaurant():
    current_user,error,status_code = admin_required()
    if error:
        return jsonify(error),status_code
    data = request.get_json() or {}
    try:
        validate_data = RestaurantSchema().load(data)
    except ValidationError as err:
        return jsonify({"errors":err.messages}),400
    restaurant,error,status_code = RestaurantService.create_restaurant(
        name = validate_data["name"],
        address = validate_data["address"],
        open_time = validate_data["open_time"],
        close_time = validate_data["close_time"],
        phone = validate_data.get("phone"),
        description= validate_data.get("description")
    )
    if error:
        return jsonify(error),status_code

    return jsonify(
        {"message":"Restaurant was created seccessfully","restaurant":restaurant.to_dict()}
    ),201

@restaurant_bp.route("",methods=["GET"])
def get_all_restaurants():
    page = request.args.get("page",default=1,type=int)
    limit = request.args.get("limit",default=10,type=int)
    if page is None or  limit is None:
        return jsonify({"error":"Page and limit must be integers"}),400
    result,error,status_code = RestaurantService.get_all_restaurants(
        page = page,
        limit = limit
    )
    if error:
        return jsonify(error),status_code
    return jsonify(result),status_code

@restaurant_bp.route("<int:restaurant_id>",methods=["GET"])
def get_restaurant(restaurant_id:int):
    restaurant,error,status_code = RestaurantService.get_restaurant(restaurant_id=restaurant_id)
    if error:
        return jsonify(error),status_code
    return jsonify({"restaurant":restaurant.to_dict()}),status_code







    


