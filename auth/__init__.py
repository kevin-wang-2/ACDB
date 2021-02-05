import time

import model
from flask import session, request, redirect
from utils import sha256
import utils
from functools import wraps

from utils.jwt import JWT

auth_jwt_generator = JWT(("sid", "level"))


def authenticate(sid, password):
    user = model.conn.find("member", {
        "sid": sid,
        "password": sha256(password)
    })
    try:
        user = user.next()
        session["uid"] = sid
        return {
            "sid": sid,
            "level": user["level"],
            "token": auth_jwt_generator.generate({
                "sid": sid,
                "level": user["level"],
            })
        }
    except StopIteration:
        return False


def deauthenticate():
    if session.get("uid") and session.get("uid") != "":
        session["uid"] = ""
        return True
    else:
        return False


def session_validation():
    if not session.get("uid") or session.get("uid") == "":
        return False
    return model.member.search_member_by_SID(session.get("uid"))


def jwt_validation():
    req = request.headers.get("authentication")
    args = request.args.get("authentication")
    form = request.form.get("authentication")
    token = req or args or form
    if not token:
        return False
    return auth_jwt_generator.validate(token)


def user_validation():
    return session_validation() or jwt_validation()


def refresh_token():
    req = request.headers.get("authentication")
    args = request.args.get("authentication")
    form = request.form.get("authentication")
    token = req or args or form
    if token:
        data = auth_jwt_generator.validate(token)
        if data["exp"] - time.time() * 1000 < 10000:
            return {
                    "success": True,
                    "token": auth_jwt_generator.generate({
                        "sid": data["sid"],
                        "level": data["level"]
                    }),
                    "sid": data["sid"],
                    "level": data["level"]
                    }
        else:
            return {
                "success": True,
                "token": token,
                "sid": data["sid"],
                "level": data["level"]
            }
    else:
        return {"success": False, "error": 0}


def validate(level=0, login="/login"):
    def decorator(func):
        if isinstance(level, type(lambda x: x)):
            @wraps(func)
            def inner(*args, **kwargs):
                user = user_validation()
                if not user:
                    return redirect(login) if login else utils.generate_error_msg(utils.ERR_UNAUTHENTICATED)
                if level(user):
                    return redirect(login) if login else utils.generate_error_msg(utils.ERR_UNAUTHORIZED)
                else:
                    return func(*args, **kwargs)

            return inner
        else:
            @wraps(func)
            def inner(*args, **kwargs):
                user = user_validation()
                if not user:
                    return redirect(login) if login else utils.generate_error_msg(utils.ERR_UNAUTHENTICATED)
                if level > 0:
                    if user["level"] < level:
                        return redirect(login) if login else utils.generate_error_msg(utils.ERR_UNAUTHORIZED)
                    else:
                        return func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)

            return inner

    return decorator

