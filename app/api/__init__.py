from flask import Blueprint, request
from flask_restful import Api
from .views import Status, Login, Connect, Host

api_bp = Blueprint("api", __name__)
api = Api(api_bp)


@api_bp.before_request
def authentication():
    print(request.path)
    print("Header auth")


api.add_resource(Status, "/status")
api.add_resource(Login, "/login")
api.add_resource(Connect, "/connect")
api.add_resource(Host, "/host")
