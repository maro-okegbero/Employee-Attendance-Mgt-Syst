from sendbox_core.integrations.falcon_integration.falcon_middleware import *
from sendbox_core.integrations.falcon_integration.utils import register_api

from employee_attendance_mgt_syst.resources import *
from employee_attendance_mgt_syst.services import UserService

import settings
import falcon



def limit_query(query, **kwargs):
    return query.raw({})


application = falcon.API(middleware=[AuthenticateMiddleware(['/signup', '/login'], settings),
                                     RequestResponseMiddleware(domain="employee_attendance_mgt_syst"),
                                     QueryParamsMiddleware()])
users = UserResource(UserService, UserResource.serializers, limiter=limit_query)

application.add_error_handler(ObjectNotFoundException, ObjectNotFoundError.handler)
application.add_error_handler(TypeError, MissingArgumentError.handler)
application.add_error_handler(MissingArgumentException, MissingArgumentError.handler)
application.add_error_handler(ActionFailedException, ActionFailedError.handler)

register_api(application, users, '/users', '/users/{obj_id}', '/users/{obj_id}/{resource_name}')