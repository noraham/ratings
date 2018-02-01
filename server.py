"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/register")
def register_form():
    """Show register form."""

    return render_template("register_form.html")

@app.route("/register_process", methods=["POST"])
def form_register():
    """Check user input"""

    email = request.form.get("user_email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")

    tricky_user = User.query.filter_by(email=email).first()

    if not tricky_user:
        new_user = User(email=email, password=password, age=age, zipcode=zipcode)
        db.session.add(new_user)
        db.session.commit()
        flash('Successfully Registered!')
        return redirect("/")
    else:
        flash('User already exists. Please log in.')
        return redirect("/")

@app.route("/login")
def login_form():
    """Show login form."""

    return render_template("login_form.html")

@app.route("/login_process", methods=["POST"])
def login():
    """Check login input"""

    email = request.form.get("user_email")
    password = request.form.get("password")
    # saved_password = User.query.filter_by(email=email, password=password).first()
    real_user = User.query.filter_by(email=email).first()
    

    if not real_user:
        flash('User does not exist. Please register.')
        return redirect("/")
    else:
        saved_password = real_user.password
        user_id = real_user.user_id
        if password == saved_password:
            session["user_id"] = user_id
            flash('Successful login!')
            return redirect("/users/{}".format(user_id))
        else:
            flash('password incorrect')
            return redirect("/login")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
