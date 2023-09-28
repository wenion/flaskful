from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from flask_cors import CORS
# from flask_mail import Mail
from flask_jwt_extended import JWTManager
# from flask_jwt_extended import user_lookup_loader
from redis_om import Migrator

from app.resources.account_signup import SignupController
from app.resources.user import UserController
from app.resources.accounts import AuthController, ProfileController
from app.resources.location import LocationController
from app.resources.term import TermController
from app.resources.level import LevelController
from app.resources.class_item import ClassItemController
from app.resources.teacher import TeacherController
from app.resources.student import StudentController
from app.resources.unchecked import UncheckedController
from app.resources.class_option import ClassOptionController
from app.resources.plan_lesson import PlanLessonController
from app.models import User

# mail = Mail()
auth = HTTPBasicAuth()
jwt = JWTManager()

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.pk

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    # print("user_lookup_callback", _jwt_header)
    # print("user_lookup_callback ", jwt_data)
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
    api.add_resource(ProfileController, '/profile', '/profile/<pk>', endpoint='profile_ep')
    api.add_resource(UserController, '/user', '/user/<pk>', endpoint='user_ep')
    api.add_resource(LocationController, '/location', '/location/<pk>', endpoint='location_ep')
    api.add_resource(TermController, '/term', '/term/<pk>', endpoint='term_ep')
    api.add_resource(LevelController, '/level', '/level/<pk>', endpoint='level_ep')
    api.add_resource(ClassItemController, '/class-item', '/class-item/<pk>', endpoint='class-item_ep')
    api.add_resource(TeacherController, '/teacher', '/teacher/<pk>', endpoint='teacher_ep')
    api.add_resource(StudentController, '/student', '/student/<pk>', endpoint='student_ep')
    api.add_resource(UncheckedController, '/unchecked', '/unchecked/<pk>', endpoint='unchecked_ep')
    api.add_resource(ClassOptionController, '/class-option', '/class-option/<pk>', endpoint='class-option_ep')
    api.add_resource(PlanLessonController, '/plan-lesson', '/plan-lesson/<pk>', endpoint='plan-lesson_ep')

    jwt.init_app(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)