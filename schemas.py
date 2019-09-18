import re

from marshmallow import Schema, fields, validates, ValidationError, post_load
from pymodm.errors import DoesNotExist

from models import User


class SignUpSchema(Schema):
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
    role = fields.String()
    password = fields.String(required=True,
                             error_messages={"required": {"message": "password is required", "code": 400}})
    employee = fields.Boolean(required=True, default=True)

    admin = fields.Boolean(required=False)

    @post_load()
    def email_to_lowercase(self, data):
        """

        :param data: The email parsed in from the email field by Marshmallow
        :return: data in lower case
        """
        data['email'] = data['email'].lower().strip()
        return data


class SignInSchema(Schema):
    email = fields.String(required=True,
                          error_messages={"required": {"message": "username is required", "code": 400}})
    password = fields.String()
    error = fields.String()

    @post_load()
    def email_to_lowercase(self, data):
        """

        :param data: The email parsed in from the email field by Marshmallow
        :return: data in lower case
        """
        data['email'] = data['email'].lower().strip()
        return data

    @post_load()
    def email_to_lowercase(self, data):
        """

        :param data: The email parsed in from the email field by Marshmallow
        :return: data in lower case
        """
        data['email'] = data['email'].lower().strip()
        return data

    @validates('email')
    def is_email_valid(self, value):
        """
        :param value: The email parsed in from the email field by Marshmallow
        :return:
        """
        try:
            print(value)
            v = re.escape(value)
            v = r"%s" % v
            v = re.compile(v, re.IGNORECASE)
            user = User.objects.raw({"email": v}).count()
            if user < 1:
                raise ValidationError('No User with that email!')
        except DoesNotExist:
            raise ValidationError('No User with that email!')


class SignInResponseSchema(Schema):
    error = fields.String()
    auth = fields.String()


class SignOutSchema(Schema):
    email = fields.String(required=True,
                          error_messages={"required": {"message": "email is required", "code": 400}})
    purpose_of_visit = fields.String()

    @post_load()
    def email_to_lowercase(self, data):
        """

        :param data: The email parsed in from the email field by Marshmallow
        :return: data in lower case
        """
        data['email'] = data['email'].lower().strip()
        print (data)
        return data

    @validates('email')
    def is_email_valid(self, value):
        """
        :param value: The email parsed in from the email field by Marshmallow
        :return:
        """
        try:
            print(value)
            v = re.escape(value)
            v = r"%s" % v
            v = re.compile(v, re.IGNORECASE)
            User.objects.get({"email": v})
        except DoesNotExist:
            raise ValidationError('No User with that email!')


class SignOutResponseSchema(Schema):
    status = fields.String()
    description = fields.String()


class AdminViewSchema(Schema):
    email = fields.String()
    password = fields.String()

    @post_load()
    def email_to_lowercase(self, data):
        """

        :param data: The email parsed in from the email field by Marshmallow
        :return: data in lower case
        """
        data['email'] = data['email'].lower().strip()
        print (data)
        return data

    @validates('email')
    def is_email_valid(self, value):
        """
        :param value: The email parsed in from the email field by Marshmallow
        :return:
        """

        if value == "sendbox@admin.ng":
            pass
        else:
            raise ValidationError('Invalid Admin Email!!, After 3 attempts the SendBox CIA will invade your present '
                                  'Location!!')

    @validates('password')
    def is_password_valid(self, value):
        """
        :param value: The email parsed in from the email field by Marshmallow
        :return:
        """

        if value == "send23678":
            pass
        else:
            raise ValidationError('Invalid Admin Password!!, After 3 attempts the SendBox CIA will invade your present '
                                  'Location!!')

    # @validates('password')
    #  def is_email_valid(self, value):
    #     """
    #     :param value: The password parsed in from the email field by Marshmallow
    #     :return:
    #     """
    #     print(value)
    #     v = re.escape(value)
    #     v = r"%s" % v
    #     v = re.compile(v, re.IGNORECASE)
    #     if v == "send23678":
    #         pass
    #     else:
    #         raise ValidationError('Invalid Admin Password!! After 3 trials the SendBox CIA will invade your present '
    #                               'Location!!')


class AdminViewResponseSchema(Schema):

    email = fields.String()
    firstname = fields.String()
    lastname = fields.String()
    phonenumber = fields.String()
    address = fields.String()
    role = fields.String()
    employee = fields.Boolean()
    timestamps = fields.Field()
    error = fields.String()


class UpdateInfoSchema(Schema):
    _id = fields.String()
    firstname = fields.String()
    lastname = fields.String()
    phonenumber = fields.String()
    address = fields.String()
    snooze = fields.String()


class UpdatedInfoSchema(Schema):
    _id = fields.String()
    firstname = fields.String()
    lastname = fields.String()
    phonenumber = fields.String()
    address = fields.String()
    role = fields.String()
    timestamps = fields.Field()
    error = fields.String()
    status = fields.String()
    description = fields.String()

