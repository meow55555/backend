from hashlib import sha256
from flask_login import LoginManager, UserMixin
from flask_login.utils import login_user
from config import ADMIN_NAME, ADMIN_PASSWORD

login_manager = LoginManager()

class User(UserMixin):
    pass

def check_password(username, password):
    if username == ADMIN_NAME and sha256(password.encode("utf-8")).hexdigest() == ADMIN_PASSWORD:
        user = User()
        user.id = ADMIN_NAME
        login_user(user)
        return True
    return False


@login_manager.user_loader
def load(user_id):
    user_id = int(user_id)
    sessionUser = User()
    sessionUser.id = user_id
    return sessionUser
