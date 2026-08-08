from flask import render_template, request
from flask import redirect, url_for

from flask_login import login_user, current_user, logout_user, login_required

from app.models import User
from app.auth import auth
from app.auth.forms import RegistrationForm, LoginForm
from app.extensions import db

@auth.route("/register", methods=["GET", "POST"])
def register():

    # GET will get the register HTML file and send it to the website
    # POST will receive the data in the forms of the particular HTML file on the website,
    # in this case the data in the register form

    print("landed in register route",request.method)

    if request.method == "POST":

        print("POST DATA: ", request.form)
        form = RegistrationForm(request.form)
        # create the form object, validate the data in the form, once validated
        # create the user object with the data from the form
        # and create the user in the database, then populate the database with the
        # data from the form

        if form.validate():
            print("FORM VALIDATED",form.username)

            user = User(
                username = form.username,
                email = form.email,
                first_name = form.first_name,
                last_name = form.last_name
            )

            user.set_password(form.password)

            db.session.add(user)
            db.session.commit()

            #temporarily go to the login page, later on we will do a proper login route
            return redirect(url_for("auth.login"))

        # so it's gone from the website > python user object > SQL database

        # if the data isn't valid it will go back to the register page

        print("FORM NOT VALIDATED",form.errors)

        return render_template(
            "auth/register.html",
            form=form
        )

    # if it's not a POST request then it must be a get request, so show register page
    return render_template("auth/register.html")

@auth.route("/login", methods=["GET","POST"])
def login():
    print("landed in login route",request.method)

    if request.method == "POST":
        print("LOGIN POST DATA: ", request.form)
        form = LoginForm(request.form)

        user = form.validate()
        if user:
            #login successful
            login_user(user)

            next_page = request.args.get("next")

            if next_page:
                return redirect(next_page)

            print("LOGIN SUCCESSFUL current user is: ", current_user.is_authenticated)
            print("LOGIN SUCCESSFUL user is: ", current_user.username)

            return render_template(
                "auth/loginSuccess.html",
                form=form,user=user
            )
        return render_template(
            "auth/login.html",
            form=form
        )

    return render_template("auth/login.html")

@auth.route("/whoami")
@login_required
def whoami():

    return f"Logged in as {current_user.username}"

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return "You have logged out"
