from resources import SignIn, SignupEmployee, SignupGuest, SignOut
from waitress import serve
import falcon


app = falcon.API()

# Resources represented by long-lived class instances
SignIn = SignIn()
SignUp_Employee = SignupEmployee()
SignUp_Guest = SignupGuest()
Sign_Out = SignOut()


#  routes will handle all requests to  '/login', '/signup_employee', '/signup_guest' and '/sign_out' URL path
app.add_route('/login', SignIn)
app.add_route('/signup_employee', SignUp_Employee)
app.add_route('/signup_guest', SignUp_Guest)
app.add_route('/sign_out', Sign_Out)






if __name__ == "__main__":
    # httpd = simple_server.make_server('localhost', 8000, app)
    # print("srever running on ", httpd.server_address)
    # httpd.serve_forever()
    serve(app, listen="*:8000")
