from hashlib import sha256
import re
import threading
from os import listdir, system
from flask import request, url_for, flash, render_template, redirect
from flask_login import login_required
from werkzeug.utils import redirect
from app.forms import AddPluginForm, ServerSettingForm
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
                set_setting(
                    "ADMIN_PASSWORD", sha256(admin_password.encode("utf-8")).hexdigest()
                )
            if server_password := form.server_password.data:
                set_setting(
                    "SERVER_PASSWORD",
                    sha256(server_password.encode("utf-8")).hexdigest(),
                )
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")
        return redirect(url_for("admin.settings_page"))


@admin_bp.route("/dashboard/plugins", methods=["GET"])
@login_required
def plugins_page():
    plugins = listdir("plugins")
    return render_template("plugins.html", plugins=plugins)


@admin_bp.route("/dashboard/plugins/add", methods=["GET", "POST"])
@login_required
def add_plugin_page():
    form = AddPluginForm()
    if request.method == "GET":
        return render_template("add_plugin.html", form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            directory = re.sub(r"\.git$", "", form.url.data.split("/")[-1])
            if system(f"git clone {form.url.data} plugins/{directory}") == 0:
                return redirect(f"/dashboard/plugins/install/{directory}")
            else:
                flash("Something went wrong, please try again.", category="alert")
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")
        return redirect(url_for("admin.add_plugin_page"))


@admin_bp.route("/dashboard/plugins/install/<directory>", methods=["GET", "POST"])
@login_required
def install_plugin_page(directory):
    if request.method == "GET":
        try:
            f = open(f"plugins/{directory}/config.py")
        except FileNotFoundError:
            flash("The plugin is not found, you can try to add it.", category="alert")
            return redirect(url_for("admin.add_plugin_page"))
        else:
            configs = []
            line = f.readline()
            while line:
                configs.append(line.replace(" ", "").split("=")[0])
                line = f.readline()
            f.close()
            return render_template(
                "install_plugin.html", directory=directory, configs=configs
            )
    if request.method == "POST":
        try:
            f = open(f"plugins/{directory}/config.py", "w")
        except FileNotFoundError:
            flash("The plugin is not found, you can try to add it.", category="alert")
            return redirect(url_for("admin.add_plugin_page"))
        else:
            # write config
            for k, v in request.form.items():
                f.write(f'{k} = "{v}"\n')
            f.close()
            # run bot
            # the system will not work when debug reloader is on
            def run_bot():
                while True:
                    system(f"python plugins/{directory}/bot.py")

            bot_thread = threading.Thread(target=run_bot)
            bot_thread.setDaemon(True)
            bot_thread.start()
            return redirect(url_for("admin.plugins_page"))
