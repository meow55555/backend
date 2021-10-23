from flask.templating import render_template
from flask_login import login_required
from ..database.helper import get_setting, get_user
from . import admin_bp


@admin_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard_page():
    server_status = get_setting("SERVER_ON")
    connections = get_user()
    return render_template(
        "dashboard.html", server_status=server_status, connections=connections
    )


@admin_bp.route("/dashboard/plugins", methods=["GET", "POST"])
@login_required
def plugins_page():
    pass
