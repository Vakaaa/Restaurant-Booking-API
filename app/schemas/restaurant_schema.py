from marshmallow import Schema,validate,fields,ValidationError,validates

class RestaurantSchema(Schema):
    name = fields.Str(
        required=True,
        error_messages={"required":"Restaurant name is required"},
        validate = validate.Length(min=2,error = "Restaurant name required at least 2 symbols")
    )
    address = fields.Str(
        required=True,
        error_messages={"required":"Restaurant address is required"},
    )
    phone = fields.Str(required=False,allow_none=True)
    description = fields.Str(required=False,allow_none=True)

    open_time = fields.Time(
        required=True,
        error_messages={"required":"Open time is required","invalid":"Invalid time format"}
    )

    close_time = fields.Time(
        required=True,
        error_messages={"required":"Close time is required","invalid":"Invalid time format"}
    )
    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Restaurant name cannot be empty")
    @validates("address")
    def validate_address(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Restaurant address cannot be empty")



