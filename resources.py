from falcon.status_codes import HTTP_501
from sendbox_core.integrations.falcon_integration.errors import BaseError
from sendbox_core.integrations.falcon_integration.falcon_restful import BaseResource

from employee_attendance_mgt_syst.models import User
from schemas import SignUpSchema, SignOutSchema, SignInSchema, SignInResponseSchema, SignOutResponseSchema, \
    AdminViewSchema, AdminViewResponseSchema, UpdatedInfoSchema, UpdateInfoSchema
from falcon import HTTP_METHOD_NOT_ALLOWED, HTTP_NOT_IMPLEMENTED


class Signup(BaseResource):
    serializers = {
        "default": SignUpSchema,
        "response": SignUpSchema
    }

    def on_get(self, req, res, obj_id=None, resource_name=None):

        raise Exception(HTTP_NOT_IMPLEMENTED)

    def save(self, data, user_context, req):
        """

        :param data:
        :param user_context:
        :param req:
        :return: Fresh object created
        """

        return self.service_class.register_user(**data)


class SignIn(BaseResource):
    serializers = {
        "default": SignInSchema,
        "response": SignInResponseSchema,
        # "update": UpdateInfoSchema,
        # "update_response": UpdatedInfoSchema
    }

    def on_get(self, req, res, obj_id=None, resource_name=None):
        raise BaseError(HTTP_501, dict(message="Http_Method_Not_implemented", name="Are you a Scammer?!"))

    def save(self, data, user_context, req):
        """
        :param data:
        :param user_context:
        :param req:
        :return:
        """


        return self.service_class.login_user(**data)


class SignOut(BaseResource):
    serializers = {
        "default": SignOutSchema,
        "response": SignOutResponseSchema
    }

    def on_get(self, req, res, obj_id=None, resource_name=None):
        raise BaseException(HTTP_METHOD_NOT_ALLOWED)

    def save(self, data, user_context, req):
        """
        :param data:
        :param user_context:
        :param req:
        :return:
        """

        return self.service_class.logout_user(**data)




class UserResource(BaseResource):
    """
    The user resource to manage communication to all users
    """
    serializers = {
        "default": UpdateInfoSchema,
        "response": UpdatedInfoSchema
    }

    def snooze(self, obj_id, data, user_context, req):
        """

        :param obj_id:
        :param data:
        :param user_context:
        :param req:
        :return:
        """
        return self.service_class.snooze(obj_id, **data)

        pass

    def limit_query(self, query, **kwargs):
        """limit the results of a query to what want the user to see"""

        user_context = kwargs.get("user_context")
        req = kwargs.get("req")
        profile_id = user_context.get("profile", {}).get("id")
        print user_context, profile_id, "this is the check"
        raw_query = {'_id': profile_id} if profile_id else {}
        return query.raw(raw_query)


