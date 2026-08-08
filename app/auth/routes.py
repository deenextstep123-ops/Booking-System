from flask import render_template, request
from flask import redirect, url_for

from flask_login import login_user, logout_user, login_required

from app.models import User
from app.auth import auth
from app.auth.forms import RegistrationForm, LoginForm
from app.extensions import db

from urllib.parse import urlsplit

@auth.route("/register", methods=["GET", "POST"])
def register():

    # GET will get the register HTML file and send it to the website
    # POST will receive the data in the forms of the particular HTML file on the website,
    # in this case the data in the register form


    if request.method == "POST":

        form = RegistrationForm(request.form)
        # create the form object, validate the data in the form, once validated
        # create the user object with the data from the form
        # and create the user in the database, then populate the database with the
        # data from the form

        if form.validate():

            # PyCharm thinks there's unexpected arguments, it's wrong, noinspection ignores it for the next line so
            # the error doesn't keep popping up
            #noinspection PyArgumentList
            user = User(
                username = form.username,
                email = form.email,
                first_name = form.first_name,
                last_name = form.last_name
            )

            user.set_password(form.password)

            db.session.add(user)
            db.session.commit()


            return redirect(url_for("auth.login"))

        # so it's gone from the website > python user object > SQL database

        # if the data isn't valid it will go back to the register page


        return render_template(
            "auth/register.html",
            form=form
        )

    # if it's not a POST request then it must be a get request, so show register page
    return render_template("auth/register.html")

@auth.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        form = LoginForm(request.form)

        user = form.validate()
        if user:
            #login successful
            login_user(user)

            next_page = request.args.get("next")

            if next_page:
                parsed_url = urlsplit(next_page)

                if (
                        not parsed_url.scheme
                        and not parsed_url.netloc
                        and parsed_url.path.startswith("/")
                ):
                    return redirect(next_page)


            return redirect(url_for("main.dashboard"))

        return render_template(
            "auth/login.html",
            form=form
        )

    return render_template("auth/login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
