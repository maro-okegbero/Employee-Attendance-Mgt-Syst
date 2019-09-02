from marshmallow import Schema, fields


class GuestSchema(Schema):
    email = fields.String(required=True,
                          error_messages={"required": {"message": "The email is required", "code": 400}})
    firstname = fields.String(required=True,
                               error_messages={"required": {"message": "first_name required", "code": 400}})
    lastname = fields.String(required=True,
                              error_messages={"required": {"message": "last_name required", "code": 400}})
    phonenumber = fields.String(required=True,
                                 error_messages={"required": {"message": "phone_number is required", "code": 400}})
    address = fields.String(required=True,
                            error_messages={"required": {"message": "address is required", "code": 400}})


class EmployeeSchema(Schema):
    email = fields.String(required=True,
                          error_messages={"required": {"message": "email is required", "code": 400}})
    firstname = fields.String(required=True,
                               error_messages={"required": {"message": "last name is required", "code": 400}})
    lastname = fields.String(required=True,
                              error_messages={"required": {"message": "last name required", "code": 400}})
    phonenumber = fields.String(required=True,
                                 error_messages={"required": {"message": "phone number required", "code": 400}})
    address = fields.String(required=True,
                            error_messages={"required": {"message": "address is required", "code": 400}})
    role = fields.String(required=True,
                         error_messages={"required": {"message": "role is required", "code": 400}})
    password = fields.String(required=True,
                             error_messages={"required": {"message": "password is required", "code": 400}})


class SignInSchema(Schema):
    email = fields.String(required=True,
                             error_messages={"required": {"message": "username is required", "code": 400}})
    password = fields.String()


class SignOutSchema(Schema):
    email = fields.String(required=True,
                          error_messages={"required": {"message": "email is required", "code": 400}})
    pov = fields.String()
