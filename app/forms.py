from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.core import BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired()], render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        "Password", validators=[DataRequired()], render_kw={"placeholder": "Password"}
    )
    submit = SubmitField("Login")


class AddPluginForm(FlaskForm):
    url = StringField(
        "URL", validators=[DataRequired()], render_kw={"placeholder": "URL of repo"}
    )
    submit = SubmitField("Add")


class ServerSettingForm(FlaskForm):
    server_on = BooleanField("Server On")
    admin_name = StringField(
        "Admin Name",
        validators=[DataRequired()],
        render_kw={"placeholder": "Admin Name"},
    )
    admin_password = PasswordField(
        "Admin Password",
        render_kw={"placeholder": "Admin Password"},
    )
    server_password = PasswordField(
        "Server Password",
        render_kw={"placeholder": "Server Password"},
    )
    submit = SubmitField("Update")
