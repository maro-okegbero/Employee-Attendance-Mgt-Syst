import falcon
import json
from models import User, TimeStamp
from datetime import datetime
from marshmallow import ValidationError
from schemas import GuestSchema, EmployeeSchema, SignOutSchema, SignInSchema



class SignIn(object):  # Resource for logging users into the system

    def myconverter(self, o):
        print(o)
        if isinstance(o, datetime):
            return o.__str__()
    @classmethod
    def login(cls, email=None, password=None):
        arrival_time = datetime.now()
        arrival_day = arrival_time.strftime("%d %B, %Y")
        try:
            login_user = User.objects.get({"_id": email})
            if not login_user.employee:
                login_user.timestamps.append({'date': arrival_day, 'login_time': arrival_time})
                login_user.save()
                guest_output = login_user.to_son().to_dict()
                return guest_output
            else:
                if password == login_user.password:
                    login_user.timestamps.append({'date': arrival_day, 'login_time': arrival_time})
                    login_user.save()
                    employee_output = login_user.to_son().to_dict()
                    return employee_output
                else:
                    error_result = {'error_result': 'The password is incorrect'}
                    return error_result
        except User.DoesNotExist:
            no_user = {'Error_Result': 'No user with that email'}
            return no_user

    def on_post(self, req, resp):  # responder
        resp.status = falcon.HTTP_200
        data = json.loads(req.stream.read())
        input_data = SignInSchema
        try:
            data = input_data().load(data=data)
            output = self.login(**data)
            print(type(output), '==============================================================')
            resp.body = json.dumps(output, default=self.myconverter)
        except ValidationError as err:
            print(err, "======================>")

            raise falcon.HTTPError("409", title="Validation Error", description=str(err))


class SignupEmployee(object):  # Resource for registering employees into the database
    def myconverter(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()
    @classmethod
    def signup(cls, email=None, firstname=None, lastname=None, phonenumber=None, address=None, employee=None, role=None,
               password=None, **kwargs):
        new_user = User(email, firstname, lastname, phonenumber, address, employee, role, password).save()
        your_user = new_user.to_son().to_dict()
        return your_user

    def on_post(self, req, resp):  # responder
        resp.status = falcon.HTTP_200
        data = json.loads(req.stream.read())
        user = EmployeeSchema
        try:
            data = user().load(data=data)
            output = self.signup(**data, employee=True)
            resp.body = json.dumps(output, default=self.myconverter)
        except ValidationError as err:
            print(err, "======================>")
            raise falcon.HTTPError("409", title="Validation Error", description=str(err))


class SignupGuest(object):  # Resource for registering guests into the database

    def myconverter(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    @classmethod
    def signup(cls, email=None, firstname=None, lastname=None, phonenumber=None, address=None, employee=None, role=None,
               password=None, **kwargs):

        new_user = User(email, firstname, lastname, phonenumber, address, employee, role, password).save()
        your_user = new_user.to_son().to_dict()
        return your_user

    def on_post(self, req, resp):  # responder
        resp.status = falcon.HTTP_200
        data = json.loads(req.stream.read())
        user = GuestSchema
        try:
            data = user().load(data=data)
            output = self.signup(**data, employee=False)
            resp.body = json.dumps(output)
        except ValidationError as err:
            print(err)
            raise falcon.HTTPError('409 ', title="Validation Failed", description=str(err))


class SignOut(object):  # Resource for logging users out of the system
    @classmethod
    def logout(cls, pov=None, email=None):
        try:
            departure_time = datetime.now()
            arrival_day = departure_time.strftime("%d %B, %Y")
            user = User.objects.get({"_id": email})
            if not user.employee:
                # user.timestamps.append({'date': arrival_day, 'logout_time': departure_time})
                user_timestamps = user.timestamps
                lastentry_of_user_timestamps = len(user_timestamps) - 1
                user_timestamps[lastentry_of_user_timestamps].update(logout_time=departure_time, purpose_of_visit=pov)
                user.save()
                return {'status': '200 Success Baby!',
                        'description': 'You are Logged out. Peace!'}
            else:
                user_timestamps = user.timestamps
                lastentry_of_user_timestamps = len(user_timestamps) - 1
                user_timestamps[lastentry_of_user_timestamps].update(logout_time=departure_time)
                user.save()
        except ValueError:
            return {'status': '40Error',
                    'description': 'Value error bro. Fix it!'}

    def on_post(self, req, resp):  # responder
        resp.status = falcon.HTTP_200
        data = json.loads(req.stream.read())
        input_data = SignOutSchema
        try:
            data = input_data().load(data=data)
            log_you_out = self.logout(**data)
            resp.body = json.dumps(log_you_out)
        except ValidationError as err:
            print(err)
            raise falcon.HTTPError('409 ', title="Validation Failed", description=str(err))
