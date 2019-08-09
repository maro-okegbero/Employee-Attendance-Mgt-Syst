from models import Employee, TimeStamp
from datetime import datetime
from random import randint
import os

def signup():
    """Sets up the account of new employees"""
    clear = lambda: os.system('cls')
    clear()
    print("****************Sign Up :) ****************\n")
    firstname = input("Enter First Name: ")
    # print("maro=====================")
    lastname = input('Enter Last Name: ')
    # print()
    nickname = input('Enter Your Nickname: ')
    # print()
    email = input('Enter Your Email: ')
    # print()
    signup_password = input('Enter Your Unique Password: ')
    # print()
    role = input('Enter Your Role : ')

    nickname = Employee(email, firstname, lastname, role, signup_password).save()
    # After sign up login() is called
    login()

def login():
    """This function handles logging in. it checks user input against a the list of stored values in the database
    """

    print("***************Welcome to Sendbox's Staff Attendance Tracking System (version 1.1)***************\n")

    status = input('Are you a new employee?(y/n): ')
    # creates a list with all the Employee's email and password to check for validation with
    emails = []
    login_passwords = []
    firstNames = []
    lastNames = []
    quotes = ['The only difference between a good day and a bad day is your attitude!','If you fail to plan, then you plan to fail',
              'The mind is everything. What you think you become','Either you run the day, or the day runs you','“I can’t do it” never yet accomplished anything; “I will try” has performed wonders',
              'Nothing is impossible, the word itself says, “I am possible!”']
    for staff in Employee.objects.all():
        staff_email = staff.email
        staff_password = staff.password
        staff_firstname = staff.first_name
        staff_lastname = staff.last_name
        emails.append(staff_email)
        login_passwords.append(staff_password)
        firstNames.append(staff_firstname)
        lastNames.append(staff_lastname)
    print(login_passwords,'\n')
    print(emails,'\n')

    if status == 'y':
        # signup function is called to sign employees in
        signup()
    else:
        print('Enter Your Login Details To Sign In \n', )
        theEmail = input('Email:  ')
        if theEmail in emails:
            print('Correct!\n')
        else:
            print('wrong email!! \n')
        indexE = emails.index(theEmail)
        password = input('Password: ')
        indexP = login_passwords.index(password)
        if password in login_passwords and indexE == indexP:
            print('Correct!\n')
        else:
            print('wrong password!')
        theFname = firstNames[indexE]
        theLname = lastNames[indexE]

        # Login validation
        index_quotes = randint(1,6)
        if theEmail in emails and password in login_passwords and indexE == indexP:
            aD = datetime.now()
            day = aD.strftime("%d %B, %Y")
            atime = aD.time()
            pday = aD.strftime('%H : %M: %S %p')
            print('********** SUCCESS***********\n')
            print('  \n')
            print('You are Logged in!', theEmail, 'Your Arrival Time is {} \n'.format(pday))
            print('  \n')
            print("Welcome to work today ", theFname, ' ', theLname, ' .\n Always remember', quotes[index_quotes],'\n Have a productive day!'   )

            logout = input('Are you ready to log out?(y): ')
            if logout == 'y' or logout != 'y':
                lD = datetime.now()
                day = lD.strftime("%d %B, %Y")
                ltime = lD.time()
                cday = lD.strftime('%H : %M : %S %p')
                print('  \n')
                print('  \n')
                print('You are Logged out! Your departure time is {} \n'.format(cday))

                theEmployee = Employee.objects.get({"_id": theEmail})
                theEmployee.timestamps.append({'date':day, 'login_time':aD, 'logout_time':lD})
                theEmployee.save()
        else:
            print('Wrong Email or Password \n')
            # recursive function
            login()
