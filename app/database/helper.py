from .models import db, Users, Settings
from config import ADMIN_NAME, ADMIN_PASSWORD, SERVER_PASSWORD


def init_db():
    db.create_all()
    set_setting("ADMIN_NAME", ADMIN_NAME)
    set_setting("ADMIN_PASSWORD", ADMIN_PASSWORD)
    set_setting("SERVER_PASS", SERVER_PASSWORD)
    set_setting("SERVER_ON", True)


def set_setting(name, value):
    try:
        setting = Settings.query.filter_by(name=name)
        if setting.first():
            setting.update({"value": value})
        else:
            setting = Settings(name, value)
            db.session.add(setting)
        db.session.commit()
        return True
    except:
        return False


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
            "active": user.active,
            "reconnect_times": user.reconnect_times,
        }
        for user in users
    ]
