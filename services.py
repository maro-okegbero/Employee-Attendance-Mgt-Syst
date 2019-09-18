from sendbox_core.base.exceptions import ObjectNotFoundException
from sendbox_core.services.odm import ServiceFactory
from .models import User
from .utils import append_timestamp, update_timestamp
from pymodm.errors import DoesNotExist

BaseUserService = ServiceFactory.create_service(User)


class UserService(BaseUserService):
    """
    :argument
        BaseUserService{object} --- Base SignUp service to wrap generic behaviour
    """

    @classmethod
    def register_user(cls, **kwargs):
        """

        :param kwargs:
        :return:
             {employee_attendance_mgt_syst.models..Users} -- Newly Created User Object.
        """

        email = kwargs.pop("email", None)
        firstname = kwargs.pop("firstname", None)
        lastname = kwargs.pop("lastname", None)
        phonenumber = kwargs.pop("phonenumber", None)
        address = kwargs.pop("address", None)
        employee = kwargs.pop("employee", None)
        role = kwargs.pop("role", None)
        password = kwargs.pop("password", None)
        admin = kwargs.pop("admin", None)
        user = cls.create(email=email, firstname=firstname, lastname=lastname, phonenumber=phonenumber,
                          address=address, employee=employee, role=role, password=password, admin=admin)
        user.set_auth()
        user.created()
        return user

    @classmethod
    def login_user(cls, **kwargs):
        """

        :param kwargs:
        :return:
            {employee_attendance_mgt_syst.models..Users} -- The updated user object with a login time appended.
        """
        # clean the arguments and set the email and password
        email = kwargs.pop("email")
        password = kwargs.pop("password")

        # check if the email is registered
        try:
            is_email_registered = cls.find_one({"email": email})
            is_email_registered.set_auth()
            print(is_email_registered)
            # determines  if the User with the email is an employee or not and performs actions on the object
            if not is_email_registered.employee:  # Guest
                user = is_email_registered
                guest = append_timestamp(user)
                return guest
            elif is_email_registered.admin:
                all_users = User.objects.all()
                return list(all_users)

            else:  # employee
                user = is_email_registered
                if password == user.password:
                    employee = append_timestamp(user)
                    return employee
                else:
                    error_result = {'error': 'The password is incorrect'}
                    return error_result

        except ObjectNotFoundException:
            user_404 = {'error': 'No user with that email'}
            return user_404

    @classmethod
    def logout_user(cls, **kwargs):  # updates logout time and pov(if user is a guest) to the last appended timestamp
        """

                :param kwargs:
                :return:
                    {employee_attendance_mgt_syst.models.Users} -- The updated user object with a logout time and pov  updated.
                """
        #  cleans the arguments and set the email and pov
        email = kwargs.pop("email")
        purpose_of_visit = kwargs.pop("purpose_of_visit")
        success = {'status': '200 Success Baby!',
                   'description': 'You are Logged out. Peace!'}

        try:

            user = cls.get(email)
            if not user.employee:
                update_timestamp(user, pov=purpose_of_visit)
                return success
            else:
                update_timestamp(user)
                return success
        except ValueError:
            return {'status': '40Error',
                    'description': 'Value error bro. Fix it!'}



    @classmethod
    def snooze(cls, obj_id, **kwargs):
        """

        :param obj_id:
        :param kwargs:
        :return:
        """

        try:
            user = cls.get(obj_id)
            user_timestamps = user.timestamps
            print(type(user_timestamps))
            lastentry_of_user_timestamps = len(user_timestamps) - 1
            print(lastentry_of_user_timestamps)
            snooze = kwargs.pop("snooze", None)
            print(snooze)
            m = user_timestamps[lastentry_of_user_timestamps]
            print(m,'=============================>')
            user_timestamps[lastentry_of_user_timestamps].update(break_time=snooze)
            user.save()
            u = user_timestamps
            print(u,'========================mmmmmmmmmm============>')
            print (user,'UUUUUUUUUUUUUUUUUSerRRRRRRRRR')
            success = {'status': 'Success',
                       'description': 'Your break_time was successfully recorded'}
            return success

        except DoesNotExist:
            return {'status': 'Failed',
                    'description': 'This email does not exist'}
