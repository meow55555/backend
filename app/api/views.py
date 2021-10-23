from flask_restful import Resource, reqparse
from flask import request
from app.stl import add_key, get_status
from app.database.helper import add_user, check_host, get_setting, get_user, update_user


def server_on_check(msg):
    server_on = get_setting("SERVER_ON")
    if server_on:
        return {"status": "Failed", "message": msg}, 400
    else:
        return {
            "status": "Failed",
            "message": "Server does not allow new connection now.",
        }, 400


class Status(Resource):
    def get(self):
        token = request.headers["token"]
        user = get_user({"token": token})[0]
        if user:
            parser = reqparse.RequestParser()
            parser.add_argument("mode")
            args = parser.parse_args()
            mode = args["mode"]
            status = get_status(bool(mode == "verbose"))
            return status
        else:
            return server_on_check("Invalid token.")


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
            return server_on_check("Wrong password")


class Connect(Resource):
    def get(self):
        token = request.headers["token"]
        user = get_user({"token": token})[0]
        if user:
            status = get_status(user["ssh_key"])
            return status
        else:
            return server_on_check("Invalid token.")

    def post(self):
        token = request.headers["token"]
        user = get_user({"token": token})[0]
        if user:
            update_user({"token": token}, {"active": True})
        else:
            return server_on_check("Invalid token.")

    def delete(self):
        token = request.headers["token"]
        user = get_user({"token": token})[0]
        if user:
            update_user({"token": token}, {"active": False})
            return {"status": "OK"}
        else:
            return server_on_check("Invalid token.")

    def put(self):
        token = request.headers["token"]
        user = get_user({"token": token})[0]
        if user:
            update_user(
                {"token": token}, {"reconnect_times": user["reconnect_times"] + 1}
            )
            return {"status": "OK"}
        else:
            return server_on_check("Invalid token.")


class Host(Resource):
    def post(self):
        token = request.headers["token"]
        user = get_user({"token": token})[0]
        if user:
            if user["active"]:
                if not check_host():
                    update_user({"token": token}, {"role": "host"})
                    return {"status": "OK"}
                else:
                    return {
                        "status": "Failed",
                        "message": "Host is some one else now.",
                    }, 400
            else:
                return {"status": "Failed", "message": "You are not connected."}, 400
        else:
            return server_on_check("Invalid token.")

    def delete(self):
        token = request.headers["token"]
        user = get_user({"token": token})[0]
        if user:
            if user["role"] == "host":
                update_user({"token": token}, {"role": "client"})
                return {"status": "OK"}
            else:
                return {"status": "Failed", "message": "You are not host."}
        else:
            return server_on_check("Invalid token.")
