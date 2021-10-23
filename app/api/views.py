from flask_restful import Resource, reqparse
from flask import request
from app.stl import add_key, get_status
from app.database.helper import add_user, get_setting, get_user, update_user


class Status(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("mode")
        args = parser.parse_args()
        mode = args["mode"]
        if mode == "verbose":
            return "Verbose status"
        return "Status"


class Login(Resource):
    def post(self):
        data = request.get_json(force=True)
        password = data["password"]
        key = data["key"]
        if password == get_setting("SERVER_PASS"):
            token = add_user(key)
            add_key(key)
            return {"status": "OK", "token": token}
        else:
            return {"status": "Failed", "message": "Wrong password"}


class Connect(Resource):
    def get(self):
        server_on = get_setting("SERVER_ON")
        token = request.headers["token"]
        user = get_user({"token": token})[0]
        if user:
            status = get_status(user["ssh_key"])
            return status
        else:
            if server_on:
                return {"status": "Failed", "message": "Invalid token."}, 401
            else:
                return {
                    "status": "Failed",
                    "message": "Server does not allow new connection now.",
                }, 400

    def delete(self):
        token = request.headers["token"]
        user = get_user({"token": token})[0]
        if user:
            update_user({"token": token}, {"active": False})
            return {"status": "OK"}
        else:
            return {"status": "Failed", "message": "Invalid token."}, 401

    def put(self):
        token = request.headers["token"]
        user = get_user({"token": token})[0]
        if user:
            update_user(
                {"token": token}, {"reconnect_times": user["reconnect_times"] + 1}
            )
            return {"status": "OK"}
        else:
            return {"status": "Fail", "message": "Invalid token."}, 401


class Host(Resource):
    def post(self):
        return "Be the host"

    def delete(self):
        return "Retire from the host"
