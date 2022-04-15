from flask import Flask, render_template, request, redirect
import re
import sqlite3 as sql

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


@app.route("/validation", methods=["POST"])
def validation():

    # Validate name
    name = request.form.get("name")
    if not name:
        return render_template("result.html", message="Missing name")

    # Validate surname
    surname = request.form.get("surname")
    if not surname:
        return render_template("result.html", message="Missing surname")

    # Validate email
    email=request.form.get("email")
    if not (re.search(regex,email)):
        return render_template("result.html", message="Not valid email")

    birthdate=request.form.get("birthdate")

    # Check new customer & new email, if OK, record
    try:
        with sql.connect("database.db") as con:
            con.execute("CREATE TABLE IF NOT EXISTS contacts (id INTEGER, name TEXT NOT NULL, surname TEXT NOT NULL, email TEXT NOT NULL, birthdate DATE, PRIMARY KEY (id))")
            cur=con.cursor()
            cur.execute("SELECT * FROM contacts WHERE (name=? AND surname=?) OR email=?", (name, surname, email))
            if cur.fetchone() is None:
                cur.execute("INSERT INTO contacts (name, surname, email, birthdate) VALUES (?,?,?,?)", (name, surname, email, birthdate))
                con.commit()
                return render_template("result.html", message="Success")
            else:
                con.rollback()
                return render_template("result.html", message="Already exists")
    except:
        return render_template("result.html", message="something went wrong")
    finally:
        con.close()



@app.route("/find_name", methods=["POST"])
def get_by_name():
    # Validate name
    name = request.form.get("name")
    if not name:
        return render_template("result.html", message="Missing name")
    # Validate surname
    surname = request.form.get("surname")
    if not surname:
        return render_template("result.html", message="Missing surname")

    # Try if contact exists in list
    try:
        con=sql.connect("database.db")
        con.row_factory = sql.Row

        cur=con.cursor()
        cur.execute("SELECT * FROM contacts WHERE name=? AND surname=?", (name, surname))

        rows = cur.fetchall()
        if len(rows)==0: return render_template("result.html", message="Name not found")
        else:return render_template("list.html",rows=rows)

    except:
        con.rollback()
        return render_template("result.html", message="Something went wrong")
    finally:
        con.close()

@app.route("/find_email", methods=["POST"])
def find_email():
    # Validate email
    email=request.form.get("email")
    if not (re.search(regex,email)):
        return render_template("result.html", message="Not valid email")


    # Try if contact exists in list

    try:
        con=sql.connect("database.db")
        con.row_factory = sql.Row
        cur=con.cursor()
        cur.execute("SELECT * FROM contacts WHERE email = ?", [email])

        rows = cur.fetchall()
        if len(rows)==0: return render_template("result.html", message="Customer email not found")
        else:return render_template("list.html",rows=rows)

    except:
        con.rollback()
        return render_template("result.html", message="Something went wrong")
    finally:
        con.close()


@app.route("/get_all_customers")
def get_all_customers():
    try:
        con=sql.connect("database.db")
        con.row_factory = sql.Row

        cur=con.cursor()
        cur.execute("SELECT * FROM contacts")

        rows = cur.fetchall()
        return render_template("list.html",rows=rows)

    except:
        con.rollback()
        return render_template("result.html", message="Not found")
    finally:
        con.close()    
    