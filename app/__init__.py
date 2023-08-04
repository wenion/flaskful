from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from flask_cors import CORS
# from flask_mail import Mail
from flask_jwt_extended import JWTManager
# from flask_jwt_extended import user_lookup_loader
from redis_om import Migrator

from resources.account_signup import SignupController
from resources.accounts import AuthController
from resources.location import LocationController
from resources.level import LevelController
from models import User

# mail = Mail()
auth = HTTPBasicAuth()
jwt = JWTManager()

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.pk

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    pk = jwt_data["sub"]
    return User.get(pk)

def create_app():
    app = Flask(__name__)
    app.config["JWT_TOKEN_LOCATION"] = ["headers",]
    app.config["JWT_SECRET_KEY"] = "super-secret"
    
    CORS(app)
    Migrator().run()
    # mail.init_app(app)
    api = Api(app)
    api.add_resource(SignupController, '/signup')
    api.add_resource(AuthController, '/login')
    api.add_resource(LocationController, '/location', '/location/<pk>', endpoint='location_ep')
    api.add_resource(LevelController, '/level', '/level/<pk>', endpoint='level_ep')

    jwt.init_app(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)