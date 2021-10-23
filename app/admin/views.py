from flask.templating import render_template
from flask_login import login_required
from ..database.helper import get_setting, get_user
from . import admin_bp


@login_required
@admin_bp.route("/dashboard", methods=["GET"])
def dashboard_page():
    server_status = get_setting("SERVER_ON")
    connections = get_user({"active": True})
    return render_template(
        "dashboard.html", server_status=server_status, connections=connections
    )


@login_required
@admin_bp.route("/dashboard/plugins", methods=["GET", "POST"])
def plugins_page():
    pass
