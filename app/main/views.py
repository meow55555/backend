from flask import request, render_template, url_for, redirect, flash
from flask_login import current_user
from ..database.helper import init_db
from ..forms import LoginForm
from ..user_helper import check_password
from . import main_bp


@main_bp.before_app_first_request
def init():
    init_db()


@main_bp.route("/", methods=["GET", "POST"])
def login_page():
    if current_user.is_active:
        return redirect(url_for("admin.dashboard_page"))
    form = LoginForm()
    if request.method == "GET":
        return render_template("login.html", form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            if check_password(form.username.data, form.password.data):
                return redirect(url_for("admin.dashboard_page"))
            else:
                flash("Wrong username or password", category="alert")
                return redirect(url_for("main.login_page"))
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")
