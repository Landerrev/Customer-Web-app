from flask import Flask, render_template, request, redirect
import re

app = Flask(__name__)

# Email verification function
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
def check(email):

    if(re.search(regex,email)):
        print("Valid Email")
    else:
        print("Invalid Email")

# All available actions
ACTIONS=[
    "Create Customer",
    "Get Customer",
    "Update Customer",
    "Delete Customer",
    "Get all Customers"
]

# Main page
@app.route('/')
def index():
    return render_template("index.html", actions=ACTIONS)

# Redirecting to choosen action
@app.route("/action", methods=["POST"])
def register():
    nextdir=request.form.get("action")
    if nextdir in ACTIONS:
        nextdir="/"+ nextdir.lower().replace(" ", "_")
        return redirect (nextdir)
    else:
        return redirect ("/")

class Customer:
    def __init__(self, name, surname, email, birthday):
        self.name=name
        self.surname=surname
        self.email=email
        self.birthday=birthday
    
    def compare_name(self, name, surname):
        if self.name==name and self.surname==surname: return True
        else: return False

    def compare_email(self, email):
        if self.email==email: return True
        else: return False

    def print (self):
        row= [self.name,self.surname, self.email, self.birthday]
        return row

    def update(self, name, surname, email, birthday):
        self.name=name
        self.surname=surname
        self.email=email
        self.birthday=birthday


    



@app.route("/create_customer")
def create_customer():
    return render_template("create_customer.html")

@app.route("/get_customer")
def get_customer():
    return render_template("get_customer.html", message="Get Customer")

@app.route("/update_customer")
def update_customer():
    return render_template("get_customer.html", message="Update Customer")

@app.route("/delete_customer")
def delete_customer():
    return render_template("get_customer.html", message="Delete Customer")