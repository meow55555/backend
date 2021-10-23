from hashlib import sha256
from flask import request, url_for, flash, render_template, redirect
from flask_login import login_required
from werkzeug.utils import redirect
from app.forms import ServerSettingForm
from ..database.helper import get_setting, get_user, set_setting
from . import admin_bp


@admin_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard_page():
    server_status = get_setting("SERVER_ON")
    connections = get_user({})
    return render_template(
        "dashboard.html", server_status=server_status, connections=connections
    )


@admin_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings_page():
    settings = {
        "server_on": get_setting("SERVER_ON"),
        "admin_name": get_setting("ADMIN_NAME"),
    }
    form = ServerSettingForm(**settings)
    if request.method == "GET":
        return render_template("settings.html", form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            print(form.server_on.data)
            set_setting("SERVER_ON", form.server_on.data)
            set_setting("ADMIN_NAME", form.admin_name.data)
            if admin_password := form.admin_password.data:
                set_setting("ADMIN_PASSWORD", sha256(admin_password.encode("utf-8")).hexdigest())
            if server_password := form.server_password.data:
                set_setting("SERVER_PASSWORD", sha256(server_password.encode("utf-8")).hexdigest())
            return redirect(url_for("admin.settings_page"))
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")
    


@admin_bp.route("/dashboard/plugins", methods=["GET", "POST"])
@login_required
def plugins_page():
    pass
