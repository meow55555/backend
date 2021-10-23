from hashlib import sha256
from .models import db, Users, Settings
from config import ADMIN_NAME, ADMIN_PASSWORD, SERVER_PASSWORD


def init_db():
    db.create_all()
    set_setting("ADMIN_NAME", ADMIN_NAME)
    set_setting("ADMIN_PASSWORD", ADMIN_PASSWORD)
    set_setting("SERVER_PASS", SERVER_PASSWORD)
    set_setting("SERVER_ON", True)


def set_setting(name, value):
    setting = Settings.query.filter_by(name=name)
    if setting.first():
        setting.update({"value": value})
    else:
        setting = Settings(name, value)
        db.session.add(setting)
    db.session.commit()
    return True


def get_setting(name):
    setting = Settings.query.filter_by(name=name).first()
    return setting.value


def get_user(filter):
    users = Users.query.filter_by(**filter).all()
    return [
        {
            "ip": user.ip,
            "token": user.token,
            "ssh_key": user.ssh_key,
            "reconnect_times": user.reconnect_times,
            "connect_time": user.connect_time,
            "role": user.role,
            "active": user.active,
        }
        for user in users
    ]


def add_user(ssh_key):
    user = Users.query.filter_by(
        ssh_key=sha256(ssh_key.encode("utf-8")).hexdigest()
    ).first()
    if user:
        token = Users.generate_token()
        update_user(
            {"ssh_key": sha256(ssh_key.encode("utf-8")).hexdigest()}, {"token": token}
        )
        return token
    else:
        user = Users(ssh_key)
        db.session.add(user)
        db.session.commit()
        return user.token


def update_user(filter, data):
    users = Users.query.filter_by(**filter)
    users.update(data)
    db.session.commit()

def check_host():
    users = Users.query.filter_by(role="host").all()
    return bool(users)