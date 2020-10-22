from marshmallow import Schema, fields


class PassengerSchema(Schema):
    # schema fields have to be the same as in the incoming request, which is why
    # they are capitalized
    Pclass = fields.Int(required=True)
    Sex = fields.Str(required=True)
    Age = fields.Int(required=False)
    SibSp = fields.Int(required=True)
    Parch = fields.Int(required=True)
    Embark = fields.Str(required=True)
    Cabin = fields.Str(required=False)

