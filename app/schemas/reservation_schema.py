from marshmallow import Schema,validate,fields,ValidationError

class ReservationSchema(Schema):
    table_id = fields.Int(
        required=True,
        error_messages={"required":"Table ID is required"},
        validate=validate.Range(min=1,error="Table ID must be greater than 0")
    )
    guest_name = fields.Str(
        required=True,
        error_messages={"required":"Guest name is required"},
        validate=validate.Length(min=2,error="Guest name must be at least 2 characters long")
    )
    guests_count = fields.Int(
        required=True,
        error_messages={"required":"Guests count is required"},
        validate=validate.Range(min=1,error="Guests count must be greater than 0")
    )
    reservation_start = fields.DateTime(
        required=True,
        error_messages={"required":"Reservation start time is required","invalid":"Invalid datetime format"}
    )
    reservation_end = fields.DateTime(
        required=True,
        error_messages={"required":"Reservation end time is required","invalid":"Invalid datetime format"}
    )