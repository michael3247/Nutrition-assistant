import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import random
import requests



app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///app.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            flash('You need to log in first.', 'warning')
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



def apology_l(message):
    return render_template("login.html", message=message)


@app.route("/login", methods=["GET", "POST"])
def login():
    """view login page"""
    if request.method == "GET":
        # Forget any user_id
        session.clear()
        return render_template("login.html")
    
    elif request.method == "POST":
        if request.form.get("username") == "" or request.form.get("password") == "":
            return apology_l("input values")
        
        username = request.form.get("username")
        password = request.form.get("password")

        data = db.execute("SELECT * FROM users WHERE username IN (?)", username)

        if len(data) != 1 or not check_password_hash(data[0]["password"], password): 
            return apology_l("Incorrect username or password")
        
        else:
            session["user"] = data[0]["id"]
    
            return redirect("/profile")
  
def apology_s(message):
    return render_template("signup.html", message=message)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """view login page"""
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        diet = request.form.get("diet")
        gender = request.form.get("gender")
        date = datetime.now().strftime("%m/%d/%Y")

        if name == "" or username == "" or password == "" or confirm == "" or diet == "":
            return apology_s("input values")
        
        check = db.execute("SELECT * FROM users WHERE username IN (?)", username)

        if len(check) != 0 :
            return apology_s("username taken")
        elif password != confirm:
            return apology_s("confirm password correctly")
        else:
            password = generate_password_hash(password)

            db.execute("INSERT INTO users (name, username, password, diet, gender, date) VALUES(?, ?, ?, ?, ?, ?)", name, username, password, diet, gender, date)
            return render_template("login.html")
        





@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    session.clear()

    return redirect("/login")


def days_between_dates(date1, date2):
    date_format = "%m/%d/%Y"
    date1 = datetime.strptime(date1, date_format)
    date2 = datetime.strptime(date2, date_format)

    delta = date2 - date1

    num_days = delta.days

    return num_days



def next_day(date_str, no):
    date_format = "%m/%d/%Y"
    input_date = datetime.strptime(date_str, date_format)

    next_date = input_date + timedelta(days=no)

    next_date_str = next_date.strftime(date_format)

    return next_date_str





def tracker():
    last = db.execute("SELECT * FROM history WHERE person_id IN (?)", session["user"])

    if last[0]["last_seen"] != datetime.now().strftime("%m/%d/%Y"):
        
        no = days_between_dates(last[0]["last_seen"], datetime.now().strftime("%m/%d/%Y"))
        
        for i in range(no + 1):
            if i > 0:
                date = next_day(last[0]["last_seen"], i)
                glass = 0
                height = 0
                color = "red"
                db.execute("INSERT INTO tracker (person_id, date, glass, height, color) VALUES(?, ?, ?, ?, ?)", session["user"], date, glass, height, color)
    
    
                
            
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    data = db.execute("SELECT * FROM users WHERE id IN (?)", session["user"])
    history = db.execute("SELECT * FROM history")
    check = ""
    for i in history:
        if session["user"] == i["person_id"]:
            check = True
    if check == True:
        store = db.execute("SELECT * FROM history WHERE person_id IN (?)", session["user"])
        last = store[0]["store"]
        db.execute("UPDATE history SET last_seen = (?), store = (?) WHERE person_id IN (?)", last, datetime.now().strftime("%m/%d/%Y"), session["user"])
    else:
        db.execute("INSERT INTO history (person_id, last_seen, store, value) VALUES(?, ?, ?, ?)", session["user"], datetime.now().strftime("%m/%d/%Y"), datetime.now().strftime("%m/%d/%Y"), random.randint(1, 100))

    scene = db.execute("SELECT * FROM history WHERE person_id IN (?)", session["user"])
    if scene[0]["last_seen"] != datetime.now().strftime("%m/%d/%Y"):
        no = random.randint(1, 100)
        db.execute("UPDATE history SET value = (?) WHERE person_id IN (?)", no, session["user"])
    val = db.execute("SELECT * FROM history WHERE person_id IN (?)", session["user"])
    digit = val[0]["value"]
    tip = db.execute("SELECT * FROM tips WHERE id IN (?)", digit)
    tracker()
    form=""
    graph = db.execute("SELECT * FROM tracker WHERE person_id IN (?) AND date IN (?)", session["user"], datetime.now().strftime("%m/%d/%Y"))
    if graph != []:
        if graph[0]["glass"] > 1:
            form = "es"
        else:
            form = ""
    else:
        date = datetime.now().strftime("%m/%d/%Y")
        glass = 0
        height = 0
        color = "red"
        db.execute("INSERT INTO tracker (person_id, date, glass, height, color) VALUES(?, ?, ?, ?, ?)", session["user"], date, glass, height, color)


    return render_template("profile.html", tip=tip, data=data, graph=graph, form=form)

        







@app.route("/plus", methods=["GET", "POST"])
@login_required
def plus():
    track = db.execute("SELECT * FROM tracker")
    validate = False
    for i in track:
        if session["user"] == i["person_id"]:
            validate = True
    if validate == True:
        feed = db.execute("SELECT * FROM tracker WHERE person_id IN (?) AND date IN (?)", session["user"], datetime.now().strftime("%m/%d/%Y"))
        result = feed[0]["glass"] + 1
        glass = result
        height = result
        color =""
        data = db.execute("SELECT * FROM users WHERE id IN (?)", session["user"])
        
        if data[0]["gender"] == "male":
            if glass >= 12:
                color = "green"
            elif glass >= 6:
                color = "yellow"
            else:
                color = "red"
        elif data[0]["gender"] == "female":
            if glass >= 9:
                color = "green"
            elif glass >= 5:
                color = "yellow"
            else:
                color = "red"
        
        db.execute("UPDATE tracker SET glass = (?), height = (?), color = (?) WHERE person_id IN (?) AND date IN (?)", glass, height, color, session["user"], datetime.now().strftime("%m/%d/%Y"))

    elif validate == False:
        date = datetime.now().strftime("%m/%d/%Y")
        glass = 1
        height = 1
        color = "red"
        db.execute("INSERT INTO tracker (person_id, date, glass, height, color) VALUES(?, ?, ?, ?, ?)", session["user"], date, glass, height, color)

    return redirect("/profile#tracker")




@app.route("/minus", methods=["GET", "POST"])
@login_required
def minus():
    track = db.execute("SELECT * FROM tracker")
    validate = False
    for i in track:
        if session["user"] == i["person_id"]:
            validate = True
    if validate == True:
        feed = db.execute("SELECT glass FROM tracker WHERE person_id IN (?) AND date IN (?)", session["user"], datetime.now().strftime("%m/%d/%Y"))
        if feed[0]["glass"] == 0:
            result = 0
        else:
            result = feed[0]["glass"] - 1
        glass = result
        height = result
        color =""
        data = db.execute("SELECT * FROM users WHERE id IN (?)", session["user"])
        
        if data[0]["gender"] == "male":
            if glass >= 12:
                color = "green"
            elif glass >= 6:
                color = "yellow"
            else:
                color = "red"
        elif data[0]["gender"] == "female":
            if glass >= 9:
                color = "green"
            elif glass >= 5:
                color = "yellow"
            else:
                color = "red"
        
        db.execute("UPDATE tracker SET glass = (?), height = (?), color = (?) WHERE person_id IN (?) AND date IN (?)", glass, height, color, session["user"], datetime.now().strftime("%m/%d/%Y"))

    else:
        date = datetime.now().strftime("%m/%d/%Y")
        glass = 1
        height = 1
        color = "red"
        db.execute("INSERT INTO tracker (person_id, date, glass, height, color) VALUES(?, ?, ?, ?, ?)", session["user"], date, glass, height, color)

    return redirect("/profile#tracker")



    
@app.route("/track", methods=["GET", "POST"])
@login_required
def track():
    data = db.execute("SELECT * FROM users WHERE id IN (?)", session["user"])
    if data[0]["gender"] == "male":
        volume = "3000ml"
    else:
        volume = "2200ml"
    info = db.execute("SELECT * FROM tracker WHERE person_id IN (?)", session["user"])
    return render_template("track.html", data=data, volume=volume, info=info)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    data = db.execute("SELECT * FROM users WHERE id IN (?)", session["user"])
    if request.method == "GET":
        return render_template("search.html", data=data)
    elif request.method == "POST":
        app_id = 'e762609b'
        app_key = 'b4d9487a74e1b72a041c2484210af2c0'

        query = request.form.get("dish") 
        url = f"https://api.edamam.com/search?q={query}&app_id={app_id}&app_key={app_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            recipes = data.get('hits')
            data = db.execute("SELECT * FROM users WHERE id IN (?)", session["user"])
            return render_template("search.html", data=data, recipes=recipes, query=query)
        else:
            return redirect("/profile")



@app.route("/meal", methods=["GET", "POST"])
@login_required
def meal():
    data = db.execute("SELECT * FROM users WHERE id IN (?)", session["user"])
    app_id = 'e762609b'
    app_key = 'b4d9487a74e1b72a041c2484210af2c0'
    url2 = f"https://www.themealdb.com/api/json/v1/1/random.php"
    response2 = requests.get(url2)
    if data[0]["diet"] == "Non-vegetarian":
        diet = ""
    else:
        diet = data[0]["diet"]
    if response2.status_code == 200:
        data3 = response2.json()
        meal2 = data3.get('meals')
    query = diet + " " + meal2[0]["strMeal"]
    url = f"https://api.edamam.com/search?q={query}&app_id={app_id}&app_key={app_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data2 = response.json()
        meal = data2.get('hits')
        if meal == []:
            query = diet
            url = f"https://api.edamam.com/search?q={query}&app_id={app_id}&app_key={app_key}"
            response = requests.get(url)
            data2 = response.json()
            result = data2.get('hits')
        else: 
            result = meal

        return render_template("meal.html", data=data, meal=result)
    else:
        return redirect("/profile")


@app.route("/me", methods=["GET", "POST"])
@login_required
def me():
    data = db.execute("SELECT * FROM users WHERE id IN (?)", session["user"])
    return render_template("me.html", data=data)


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        db.execute("DELETE FROM users WHERE id IN (?)", session['user'])
        db.execute("DELETE FROM history WHERE person_id IN (?)", session['user'])
        db.execute("DELETE FROM tracker WHERE person_id IN (?)", session['user'])
        return redirect("/")



@app.route("/changen", methods=["GET", "POST"])
@login_required
def changen():
    if request.method == "POST":
        name = request.form.get("newn")
        if name != "":
            db.execute("UPDATE users SET name = (?) WHERE id IN (?)", name, session["user"])
            return redirect("/me")
    
        return redirect("/me")


    


if __name__ == "__main__":
    app.run()