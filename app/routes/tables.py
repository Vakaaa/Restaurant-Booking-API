from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required, get_jwt_identity

from marshmallow import ValidationError
from app.schemas.table_schema import TableSchema,TableUpdateSchema
from app.models.user import User
from app.services.table_service import TableService

tables_bp = Blueprint("tables", __name__, url_prefix="/restaurants/<int:restaurant_id>/tables")

def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)


def admin_required():
    current_user = get_current_user()
    if not current_user or current_user.role != "admin":
        return None,{"error":"Forbidden"},403
    return current_user,None,None

@tables_bp.route("", methods=["POST"])
@jwt_required()
def create_table(restaurant_id):
    current_user,error,status_code = admin_required()
    if error:
        return jsonify(error), status_code
    data = request.get_json() or {}
    try:
        validate_data = TableSchema().load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    table,error,status_code = TableService.create_table(
        restaurant_id=restaurant_id,
        table_number=validate_data["table_number"],
        seats=validate_data["seats"],
        is_active=validate_data.get("is_active", True)
    )
    if error:
        return jsonify(error), status_code

    return jsonify(
        {"message": "Table was created successfully", "table": table.to_dict()}
    ), 201

@tables_bp.route("", methods=["GET"])
def get_tables(restaurant_id):
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    if page is None or limit is None:
        return jsonify({"error": "Page and limit must be integers"}), 400
    result,error,status_code = TableService.get_tables_by_restaurant(
        restaurant_id=restaurant_id,
        page=page,
        limit=limit
    )
    if error:
        return jsonify(error), status_code

    return jsonify(result), status_code

@tables_bp.route("/<int:table_id>", methods=["PATCH"])
@jwt_required()
def update_table(restaurant_id, table_id):
    current_user,error,status_code = admin_required()
    if error:
        return jsonify(error), status_code
    data = request.get_json() or {}
    try:
        validate_data = TableUpdateSchema().load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    table,error,status_code = TableService.update_table(
        table_id=table_id,
        restaurant_id=restaurant_id,
        data = validate_data
    )
    if error:
        return jsonify(error), status_code

    return jsonify(
        {"message": "Table was updated successfully", "table": table.to_dict()}
    ), 200

@tables_bp.route("/<int:table_id>", methods=["DELETE"])
@jwt_required()
def delete_table(restaurant_id, table_id):
    current_user,error,status_code = admin_required()
    if error:
        return jsonify(error), status_code
    error,status_code = TableService.delete_table(
        restaurant_id=restaurant_id,
        table_id=table_id
    )
    if error:
        return jsonify(error), status_code

    return jsonify({"message": "Table was deleted successfully"}), 200










