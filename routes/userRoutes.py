import hashlib
from flask import render_template, session, redirect, request, flash
from repositories.permissions import find_permissions_by_role
from repositories.users import *
from utils import is_logged
from . import routes

'''
FILE WITH ROUTES ABOUT LOGIN, REGISTER AND LOGOUT USERS FROM WEB PAGE
'''


@routes.route('/')
def index():
    if not is_logged():
        return redirect("/login")
    return redirect("/home")


@routes.route('/logout', methods=["GET"])
def logout():
    session["username"] = None
    session["role"] = None
    session["access"] = None
    session["remove"] = None
    session["read"] = None
    session["write"] = None
    return redirect("/login")


@routes.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form
        username = form.get("username")
        password = form.get("password")
        # Check data
        if username is None:
            flash("Nombre de usuario no definido")
        elif password is None:
            flash("Contraseña no definida")
        else:
            password_hashed = hashlib.sha256(password.encode()).hexdigest()
            result = find_user_password(username, password_hashed)
            if result:
                # Get user info
                username, role = result
                permissions = find_permissions_by_role(role)
                session["username"] = username
                session["role"] = role
                session["access"] = permissions["access"]
                session["read"] = permissions["read"]
                session["write"] = permissions["write"]
                session["remove"] = permissions["remove"]
                return redirect("/home")
            else:
                flash("Los datos introducidos son incorrectos.")
    return render_template("login.html")


@routes.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form = request.form
        username = form.get("username")
        password1 = form.get("password1")
        password2 = form.get("password2")
        role = form.get("role")
        # Check data
        if username is None:
            flash("Nombre de usuario no definido")
        elif password1 is None or password2 is None:
            flash("Contraseña no definida")
        elif role is None:
            flash("Rol no definido")
        elif password1 != password2:
            flash("Las contraseñas no coinciden")
        elif check_user_exists(username):
            flash("Usuario ya existe")
        else:
            # Create user
            password_hashed = hashlib.sha256(password1.encode()).hexdigest()
            inserted = create_new_user(username, password_hashed, role)
            # Register Success
            if inserted:
                permissions = find_permissions_by_role(role)
                session["username"] = username
                session["role"] = role
                session["role"] = role
                session["access"] = permissions["access"]
                session["read"] = permissions["read"]
                session["write"] = permissions["write"]
                session["remove"] = permissions["remove"]
                return redirect("/home")
            # Error inserting the values
            else:
                flash("Error interno: No se ha podido crear el usuario. Por favor, vuelve a intentarlo.")
    return render_template("register.html")
