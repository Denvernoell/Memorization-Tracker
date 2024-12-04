import sys

sys.path.append("..")
import arrow

from fasthtml.common import *
from fapp import app, rt
from shared.fh.tables import *
from shared.fh.utils import *
import polars as pl
from datetime import date
import shared.database as db


@rt("/signup")
def get():
    return db.signup_get()


@rt("/signup")
def post(login: db.Login, sess):
    return db.signup_post(login, sess)


@rt("/login")
def get():
    return db.login_get()


@rt("/login")
def post(login: db.Login, sess):
    return db.login_post(login, sess)


@rt("/logout")
def logout(sess):
    return db.logout(sess)


@rt("/protected")
def protected(auth):
    print(f"Accessing protected page. Auth: {auth}")
    return Titled(
        "Protected Page",
        P(f"Welcome, {auth}!"),
        A("Back", href="/"),
        P(),
        A("Logout", href="/logout"),
    )


@rt("/")
def home(sess):
    if db.is_authenticated(sess):
        user = sess["user"]
        print(f"User: {user}")
        return Titled(
            "Dashboard",
            P(f"Welcome, {user}!"),
            P("You are logged in. View a protected page below."),
            A("Protected Page", href="/protected"),
            P(),
            P("Logout here:"),
            A("Logout", href="/logout"),
        )

    else:
        return Titled("Home", H1("Welcome to the App"), A("Login", href="/login"))


# @rt("/login", methods=["GET", "POST"])
# def login_home(params: dict, request: Request):
#     if request.method == "POST":
#         # Handle login logic here

#         print(params)
#         # username = request.form.get("username")
#         # password = request.form.get("password")
#         # Authenticate user
#         # try:
#         #     database.
#         # ...authentication logic...
#         return P(
#             f"Login successful for {username} with {password}! Redirecting to dashboard..."
#         )
#         # return redirect("/dashboard")
#     return Titled(
#         "Login",
#         Form(
#             cls="form-control",
#             hx_post="/login",
#         )(
#             Input(name="username", type="text", placeholder="Username"),
#             Input(name="password", type="password", placeholder="Password"),
#             Button(
#                 "Login",
#                 type="submit",
#             ),
#         ),
#     )


# @rt("/dashboard", methods=["GET"])
# def dashboard():
#     return Titled(
#         "Dashboard",
#         H2("Create Terms"),
#         Link("/terms", "Go to Terms"),
#         H2("Take Tests"),
#         Link("/tests", "Go to Tests"),
#     )
