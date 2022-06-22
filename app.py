import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from apology import apology
from flask_session import Session
from tempfile import mkdtemp
import string
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
# Configure application
app = Flask(__name__)

container = []

import sqlite3

connection = sqlite3.connect('restaurant.db', check_same_thread=False)
cursor = connection.cursor()

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

cursor.execute('SELECT sqlite_version()')
print(cursor.fetchall())

@app.route("/")
def index():
    """Show portfolio of stocks"""
    return render_template("login.html")
    #user_id = session["user_id"]

@app.route("/filter", methods=["GET", "POST"])
def filter():
    if request.method == "POST":
        return render_template("restaurant.html")
    else:
        return render_template('filter.html')

@app.route("/restaurant")
def restaurant():
    return render_template("restaurant.html")

@app.route("/restaurant2")
def restaurant2():
    return render_template("restaurant2.html")

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")

@app.route('/name', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       first_name = request.form.get("fname")
       # getting input with name = lname in HTML form
       last_name = request.form.get("lname")
       return "Your name is "+ first_name + last_name
    return render_template("name.html")

@app.route('/selection', methods =["GET", "POST"])
def selection():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       fav_language = request.form.get("fav_language")
       return "Your fav language is " + fav_language
    return render_template("selection.html")

"""
@app.route('/crowdsource', methods=["GET", "POST"])
def crowdsource():
    if request.method == "POST":
        restaurant = request.form.get("restaurant")
        location = request.form.get("location")
        specialty = request.form.get("speciality")
        cursor.execute("INSERT INTO restaurant (specialty, location, name) VALUES (?, ?, ?)", specialty, location, restaurant);
        return "Thank you for your information on " + restaurant
    return render_template("crowdsource.html")
"""
""""
@app.route('/add', methods=["GET", "POST"])
def crowdsource():
    if request.method == "POST":
        restaurant = request.form.get("restaurant")
        location = request.form.get("location")
        specialty = request.form.get("specialty")
        sqlite3 = ("INSERT INTO restaurants (specialty, location, name) VALUES (?, ?, ?)")
        cursor.execute(sqlite3,(specialty, location,  restaurant))
        connection.commit()
        return "Thank you for your information on " + restaurant
        #return redirect('/')
    return render_template("crowdsourcing.html")
#Register Method
"""""

@app.route("/crowdsource", methods=["GET", "POST"])
def crowdsource():
    if request.method == "POST":
        #inputs data into the db
        return render_template('homepage.html')
    else:
        return render_template('crowdsourcing.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        if not username:
            return apology('Username is required!')
        elif not password:
            return apology('Password is required!')
        elif not confirmation:
            return apology('Confirmation is required!')

        if password != confirmation:
            return apology('Passwords do not match!')
        hash = generate_password_hash(password)
        try:
            userInfo = ("INSERT INTO users (username, hash) VALUES (?, ?)")
            cursor.execute(userInfo, (username, hash))
            connection.commit()
            print('try done')
            return redirect('/')
        except Exception as e:
            print(e)
            print(username)
            print(type(hash))
            #traceback.print_exc()
            return apology('Username has already been used.')
    else:
        return render_template("register.html")

@app.route("/personalize", methods=["GET", "POST"])
def personalize():
    if request.method == "POST":
        age = request.form.get('age')
        allergies = request.form.get('allergy')
        #custype = request.form.get('types')
        value = ("INSERT INTO user_data (agegroup, allergy) VALUES (?,?)")
        cursor.execute(value, (age, allergies))
        return redirect("homepage.html")
    else:
        return render_template("personalize.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        print(request.form.get("username"))
        print(type(request.form.get("username")))

        # Ensure username was submitteds
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        username = request.form.get("username")
        row = cursor.execute("SELECT id, hash, COUNT(*) FROM users WHERE username = ?", (username,)).fetchall()[0]

        print(request.form.get("username"))

        # Ensure username exists and password is correct
        if row[2] != 1 or not check_password_hash(row[1], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = row[0]

        # Redirect user to home page
        return render_template("homepage.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
"""
@app.route('/filter', methods=["GET", "POST"])
def filter():
    time = request.form.get('time')
    custype = request.form.get('custype')
    restype = request.form.get('restype')
    price = request.form.get('price')
    
    future developments
    allergies from user sql database (from registration)
    consider age group from user sql database (from registration)
    
    
    else:
        return render_template("filter.html")
"""









