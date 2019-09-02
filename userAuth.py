'''from models import User, TimeStamp
from datetime import datetime
from random import randint
import json


def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()


def signup(email=None, firstname=None, lastname=None,phonenumber=None, address=None, employee=None, role=None,
           password=None, **kwargs):

    new_user = User(email, firstname, lastname, phonenumber, address, employee, role, password).save()
    your_user = new_user.to_son().to_dict()
    return your_user


def login(email=None, password=None):
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


def logout(pov=None, email=None):
    try:
        departure_time = datetime.now()
        arrival_day = departure_time.strftime("%d %B, %Y")
        user = User.objects.get({"_id": email})
        if not user.employee:
        #user.timestamps.append({'date': arrival_day, 'logout_time': departure_time})
            user_timestamps = user.timestamps
            lastentry_of_user_timestamps = len(user_timestamps)-1
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





    # creates a list with all the Employee's email and password to check for validation with
    emails = []
    login_passwords = []
    quotes = ['The only difference between a good day and a bad day is your attitude!',
              'If you fail to plan, then you plan to fail',
              'The mind is everything. What you think you become', 'Either you run the day, or the day runs you',
              '“I can’t do it” never yet accomplished anything; “I will try” has performed wonders',
              'Nothing is impossible, the word itself says, “I am possible!”']
    for staff in Employee.objects.all():
        staff_email = staff.email
        staff_password = staff.password
        emails.append(staff_email)
        login_passwords.append(staff_password)
    print(login_passwords, '\n')
    print(emails, '\n')
    index_quotes = randint(1, 5)
    
    if theEmail in emails and password in login_passwords:
        index_theEmail = emails.index(theEmail)
        index_password = login_passwords.index(password)
        if index_password == index_theEmail:
            aD = datetime.now()
            day = aD.strftime("%d %B, %Y")
            atime = aD.time()
            pday = aD.strftime('%H : %M: %S %p')
            print('You are Logged in!', theEmail, 'Your Arrival Time is {} \n'.format(pday))
            print('  \n')
            print("Welcome to work today ", theEmail, ' .\n Always remember', quotes[index_quotes],
                  '\n Have a productive day!')
            lD = datetime.now()
            day = lD.strftime("%d %B, %Y")
            ltime = lD.time()
            cday = lD.strftime('%H : %M : %S %p')
            print('  \n')
            print('  \n')
            print('You are Logged out! Your departure time is {} \n'.format(cday))

            theEmployee = Employee.objects.get({"_id": theEmail})
            theEmployee.timestamps.append({'date': day, 'login_time': aD})
            theEmployee.save()
            your_user = theEmployee.to_son().to_dict()
            return your_user
        else:
            return None
    else:
        return None
    '''
