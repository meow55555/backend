from hashlib import sha256
from os import urandom
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String, nullable=False)
    ssh_key = db.Column(db.String, unique=True, nullable=False)
    token = db.Column(db.String, unique=True, nullable=False)
    reconnect_times = db.Column(db.Integer, default=0)
    connect_time = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    role = db.Column(db.String, nullable=False, default="client") # host or client
    active = db.Column(db.Boolean, default=False)

    @staticmethod
    def generate_token():
        return urandom(32)

    def __init__(self, ssh_key):
        self.ssh_key = sha256(ssh_key.encode("utf-8")).hexdigest()
        self.token = self.generate_token()


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    value = db.Column(db.String, nullable=False)

    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value
