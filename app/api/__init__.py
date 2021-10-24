from flask import Blueprint, request
from flask_restful import Api
from .views import Status, Login, Connect, Host

api_bp = Blueprint("api", __name__)
api = Api(api_bp)


@api_bp.before_request
def check_token():
    # do simple check for token
    if request.path != "/api/login":
        token = request.headers.get("Authorization", None)
        if not (token and token.startswith("Bearer")):
            return {"status": "fail", "message": "Invalid token."}, 401



api.add_resource(Status, "/status")
api.add_resource(Login, "/login")
api.add_resource(Connect, "/connect")
api.add_resource(Host, "/host")
