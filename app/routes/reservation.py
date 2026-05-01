from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required,get_jwt_identity

from app.models.user import User
from app.services.reservation_service import ReservationService
from app.schemas.reservation_schema import ReservationSchema
from marshmallow import ValidationError


reservation_bp = Blueprint("reservation",__name__,url_prefix="/reservations")


def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(user_id)

@reservation_bp.route("",methods=["POST"])
@jwt_required()
def create_reservation():
    current_user = get_current_user()
    data = request.get_json() or {}
    try:
        validate_data = ReservationSchema().load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    reservation,error,status_code = ReservationService.create_reservation(
        user_id = current_user.id,
        table_id = validate_data["table_id"],
        guest_name = validate_data["guest_name"],
        guests_count = validate_data["guests_count"],
        reservation_start = validate_data["reservation_start"],
        reservation_end = validate_data["reservation_end"]
    )
    if error:
        return jsonify(error), status_code

    return jsonify(
        {"message": "Reservation was created successfully", "reservation": reservation.to_dict()}
    ), status_code

@reservation_bp.route("", methods=["GET"])
@jwt_required()
def get_user_reservations():
    current_user = get_current_user()
    page = request.args.get("page", default=1, type=int)
    limit = request.args.get("limit", default=10, type=int)
    result,error,status_code = ReservationService.get_reservations_by_user(
        user_id=current_user.id,
        page=page,
        limit=limit
    )
    if error:
        return jsonify(error), status_code

    return jsonify(result), status_code



