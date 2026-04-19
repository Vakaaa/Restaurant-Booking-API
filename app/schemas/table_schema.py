from marshmallow import Schema,validate,fields,ValidationError,validates,validates_schema

class TableSchema(Schema):
    table_number = fields.Int(
        required=True,
        error_messages={"required":"Table number is required"},
        validate=validate.Range(min=1,error="Table number must be greater than 0")
    )
    seats = fields.Int(
        required=True,
        error_messages={"required":"Seats number is required"},
        validate=validate.Range(min=1,error="Seats number must be greater than 0")
    )
    is_active = fields.Boolean(required=False, load_default=True)
    @validates("table_number")
    def validate_table_number(self,value,**kwargs):
        if value <= 0:
            raise ValidationError("Table number must be greater than 0")

    @validates("seats")
    def validate_seats(self,value,**kwargs):
        if value <= 0:
            raise ValidationError("Seats number must be greater than 0")
    
    
class TableUpdateSchema(Schema):
    table_number = fields.Int(
        required=False,
        validate=validate.Range(min=1,error="Table number must be greater than 0")
    )
    seats = fields.Int(
        required=False,
        validate=validate.Range(min=1,error="Seats number must be greater than 0")
    )
    is_active = fields.Boolean(required=False)
    @validates("table_number")
    def validate_table_number(self,value,**kwargs):
        if value <= 0:
            raise ValidationError("Table number must be greater than 0")

    @validates("seats")
    def validate_seats(self,value,**kwargs):
        if value <= 0:
            raise ValidationError("Seats number must be greater than 0")
    
    @validates_schema
    def validate_not_empty(self, data, **kwargs):
        if not data:
            raise ValidationError("At least one field must be provided for update")
