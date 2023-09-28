import flask_restful
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_current_user
from enum import IntEnum


class Permission(IntEnum):
    # MANAGER = 0
    # ADMIN = 1
    # NORMAL = 2
    # MINIMUM = 3
    LEVEL1 = 0
    LEVEL2 = 1
    LEVEL3 = 2
    LEVEL4 = 3


class RoleType(IntEnum):
    OTHER = 0
    TEACHER = 1
    STUDENT = 2


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            id = get_jwt_identity()
            print("claims", claims, id, get_current_user())
            # print("claims 222", Permission.ROOT)
            # if claims["is_administrator"]:
            if True:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Admins only!"), 403

        return decorator

    return wrapper


# @jwt_required()
def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # current_user = get_jwt_identity()
        claims = get_jwt()

        # print("wrapper 1", claims)
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        # print("wrapper 2")

        # acct = basic_authentication()  # custom account lookup function
        acct = True #basic_authentication()  # custom account lookup function

        # print("wrapper 3")

        if acct:
            return func(*args, **kwargs)

        # print("wrapper 4")

        flask_restful.abort(401)
    return wrapper