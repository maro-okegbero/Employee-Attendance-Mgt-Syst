from sendbox_core.integrations.falcon_integration.falcon_middleware import *
from sendbox_core.integrations.falcon_integration.utils import register_api

from employee_attendance_mgt_syst.resources import *
from employee_attendance_mgt_syst.services import UserService

import settings
import falcon




application = falcon.API(middleware=[AuthenticateMiddleware(['/signup', '/login'], settings),
                                     RequestResponseMiddleware(domain="employee_attendance_mgt_syst"),
                                     QueryParamsMiddleware()])



# Resources represented by long-lived class instances
# SignIn = SignIn()
register = Signup(UserService, Signup.serializers)
login = SignIn(UserService, SignIn.serializers)
logout = SignOut(UserService, SignOut.serializers)
users = UserResource(UserService, UserResource.serializers)
# adminPage = AdminView(UserService, AdminView.serializers)

# application.add_route('/login', SignIn)
# application.add_error_handler(ObjectNotFoundException, ObjectNotFoundError.handler)
# application.add_error_handler(TypeError, MissingArgumentError.handler)
# application.add_error_handler(MissingArgumentException, MissingArgumentError.handler)
# application.add_error_handler(ActionFailedException, ActionFailedError.handler)
# # application.add_route('/signup', register)
# application.add_route('/logout', logout)
# application.add_route('/AdminPage', adminPage)
register_api(application, register, '/signup')
register_api(application, logout, '/logout')
# register_api(application, adminPage, '/AdminPage')
register_api(application, login, '/login', '/login/{obj_id}/{resource_name}')
register_api(application, users, '/users', '/users/{obj_id}', '/users/{obj_id}/{resource_name}')