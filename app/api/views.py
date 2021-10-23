from flask_restful import Resource, reqparse


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
        return "Login"


class Connect(Resource):
    def get(self):
        return "Get connection status"

    def delete(self):
        return "Disconnect"

    def put(self):
        return "Reconnect"


class Host(Resource):
    def post(self):
        return "Be the host"

    def delete(self):
        return "Retire from the host"
