from hashlib import sha256
from flask_login import LoginManager, UserMixin
from flask_login.utils import login_user
from .database.helper import get_setting

login_manager = LoginManager()


class User(UserMixin):
    pass


def check_password(username, password):
    ADMIN_NAME = get_setting("ADMIN_NAME")
    ADMIN_PASSWORD = get_setting("ADMIN_PASSWORD")
    if (
        username == ADMIN_NAME
        and sha256(password.encode("utf-8")).hexdigest() == ADMIN_PASSWORD
    ):
        user = User()
        user.id = ADMIN_NAME
        login_user(user)
        return True
    return False


@login_manager.user_loader
def load(user_id):
    sessionUser = User()
    sessionUser.id = user_id
    return sessionUser
