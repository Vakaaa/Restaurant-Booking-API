from marshmallow import Schema,validate,fields,ValidationError,validates

class RegisterSchema(Schema):
    full_name = fields.Str(
        required=True,
        error_messages={"required":"Full name required"},
        validate=validate.Length(min=2,error="Full name required at least 2 symbols")
    )
    email = fields.Email(
        required=True,
        error_messages={"required":"Email is required","invalid":"Invalid email format"}
    )
    password = fields.Str(
        required=True,
        error_messages={"required":"password required"},
        validate=validate.Length(min=6,error="Password required at least 6 symbols ")
    )

    @validates("full_name")
    def validate_full_name(self,value,**kwargs):
        if not value.strip():
            raise ValidationError("Full name cannot be empty")
        
    @validates("password")
    def validate_password(self,value,**kwargs):
        if not value.strip():
            raise ValidationError("Password name cannot be empty")
        
class LoginSchema(Schema):
    email = fields.Email(
        required=True,
        error_messages={"required": "Email is required", "invalid": "Invalid email format"}
    )
    password = fields.Str(
        required=True,
        error_messages={"required": "Password is required"}
    )