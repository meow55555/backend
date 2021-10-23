from flask import Blueprint
from flask_restful import Api
from .views import Status, Login, Connect, Host

api_bp = Blueprint("api", __name__)
api = Api(api_bp)


@api_bp.before_app_request
def authentication():
    print("Header auth")


api.add_resource(Status, "/api/status")
api.add_resource(Login, "/api/login")
api.add_resource(Connect, "/api/connect")
api.add_resource(Host, "/api/host")
