from flask import request, render_template, url_for, redirect
from flask_login import current_user
from ..forms import LoginForm
from ..user_helper import check_password
from . import main_bp


@main_bp.route("/", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if request.method == "GET":
        return render_template("login.html", form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            if check_password(form.username.data, form.password.data):
                print(current_user)
                return redirect(url_for("admin.dashboard_page"))
            return redirect(url_for("main.login_page"))
        else:
            return ""