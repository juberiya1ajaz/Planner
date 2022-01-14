from re import DEBUG
from cs50 import SQL
from flask import Flask, redirect,url_for, render_template, request, session, flash
from flask_session import Session
from tempfile import mkdtemp
from sqlalchemy.sql.expression import select
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import login_required


# Configure application
app = Flask(__name__)


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///planner.db")

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/home")
@login_required
def home():
    user_id=session["user_id"]
    print(user_id)
    task = db.execute("SELECT * FROM task WHERE user_id = ?" , user_id )
    print(task)
    return render_template("home.html", task=task)
    

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("contact.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    
    """Log user in"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return "must provide username"
        elif not request.form.get("password"):
            return "must provide password"
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return ("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        user = db.execute("SELECT username FROM users WHERE id = ?",session["user_id"] )
        session["username"] = user[0]["username"]

        # Redirect user to home page
        return render_template("home.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
       
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")      

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password=request.form.get("password")
        c_password=request.form.get("confirmation")
        #show apology if some error was occured
        if not username:
            return "must provide username"
        elif not password or not  c_password :
            return"must provide password" 
    
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        if len(rows) >= 1:
            return ("username already exists" , 400)
        # Start session
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",username=request.form.get("username"),
                             hash=generate_password_hash(request.form.get("password")))

        rows = db.execute("SELECT id FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["id"]
        user = db.execute("SELECT username FROM users WHERE id = ?",session["user_id"] )
        session["username"] = user[0]["username"]
        
        return redirect("/home")
    else:
        return render_template("register.html")

@app.route("/delete" , methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        user_id=session["user_id"]
        if not request.form.get("username"):
            return "must provide username"
        elif not  request.form.get("password"):
            return"must provide password" 
        db.execute('DELETE FROM users WHERE id = ?', (user_id))
        session.clear()
        return redirect("/")
    else:
        return render_template("delete.html")

   
@app.route("/task", methods=["GET", "POST"])  
@login_required
def  task():
    if request.method == "POST":
       #  Add the user's entry into the database
        user_id=session["user_id"]
        subject = request.form.get("sub")
        day = request.form.get("day")
        month = request.form.get("month")
        task = request.form.get("task")
        date = request.form.get("date")
        priority = request.form.get("priority")
        db.execute("INSERT INTO task (subject,day,month,task,date,priority,type,user_id) VALUES(?, ?, ?,?,?,? ,?,?)", 
        subject,day,month,task,date,priority,"add",user_id)
        return render_template("home.html")

    else:
        return render_template("task.html")

        
@app.route('/delete/<string:task>', methods = ['GET'])

def delete_task(task):
    db.execute("DELETE FROM task WHERE task=%s", (task))
    return redirect(url_for("index"))
 

        
    
if __name__=="__main__":
    app.run(debug=True)