import hashlib
import re
from functools import wraps
from flask import request

SALT = b"12345"


def sha256(text):
    sha = hashlib.sha256()
    sha.update(text.encode("utf-8") + SALT)
    return sha.hexdigest()


# ERROR CODES
ERR_INVALID_ARGUMENTS = -1
ERR_UNAUTHENTICATED = -400
ERR_UNAUTHORIZED = -401

ERR_MSG = {
    ERR_INVALID_ARGUMENTS: "Invalid Arguments(%s)",
    ERR_UNAUTHENTICATED: "Unauthenticated",
    ERR_UNAUTHORIZED: "Unauthorized"
}


def generate_error_msg(error, *args):
    return {"success": False, "error": error, "message": ERR_MSG[error] % args}


ARG_EXIST = -1
ARG_INT = 0
ARG_FLOAT = 1
ARG_STRING = 2
ARG_BOOL = 3

ARG_VEC_TABLE = {}

RE_INT = re.compile(r"[0-9]+$")
RE_FLOAT = re.compile(r"[0-9]+\.?[0-9]+$")
RE_BOOL = re.compile("([tT]rue|[fF]alse)$")


def check_argument_validity(argument, argument_type, **args):
    if argument_type in ARG_VEC_TABLE:
        return ARG_VEC_TABLE[argument_type](argument, **args)
    else:
        return False


def check_existence(argument, **args):
    return argument is not None


def check_re_generator(expr):
    def check_re(argument, **args):
        if not check_existence(argument):
            return False
        return expr.match(argument) is not None
    return check_re


def check_int(argument, **args):
    if not check_existence(argument):
        return False
    if RE_INT.match(argument) is None:
        return False
    argument = int(argument)
    if "min" in args and argument < args["min"]:
        return False
    if "max" in args and argument > args["max"]:
        return False
    return True


def check_str(argument, **args):
    if not check_existence(argument):
        return False
    if "re" in args and not re.match(args["re"], argument):
        return False
    if "length" in args and len(argument) != args["length"]:
        return False
    return True


ARG_VEC_TABLE[ARG_EXIST] = check_existence
ARG_VEC_TABLE[ARG_INT] = check_int
ARG_VEC_TABLE[int] = ARG_VEC_TABLE[ARG_INT]
ARG_VEC_TABLE[ARG_FLOAT] = check_re_generator(RE_FLOAT)
ARG_VEC_TABLE[float] = ARG_VEC_TABLE[ARG_FLOAT]
ARG_VEC_TABLE[ARG_STRING] = check_str
ARG_VEC_TABLE[str] = check_str
ARG_VEC_TABLE[ARG_BOOL] = check_re_generator(RE_BOOL)
ARG_VEC_TABLE[bool] = ARG_VEC_TABLE[ARG_BOOL]


def check_form_arguments(argument_dict):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = {}
            for key in argument_dict:
                val = request.form.get(key)
                condition = argument_dict[key]
                if isinstance(condition, dict):
                    if not check_argument_validity(val, condition["type"], **condition):
                        return generate_error_msg(ERR_INVALID_ARGUMENTS, key)
                    else:
                        result[key] = val
                else:
                    if not check_argument_validity(val, condition):
                        return generate_error_msg(ERR_INVALID_ARGUMENTS, key)
                    else:
                        result[key] = val
            return func(form_arguments=result, *args, **kwargs)
        return inner
    return decorator


def check_qs_arguments(argument_dict):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = {}
            for key in argument_dict:
                val = request.args.get(key)
                condition = argument_dict[key]
                if isinstance(condition, dict):
                    if not check_argument_validity(val, condition["type"], **condition):
                        return generate_error_msg(ERR_INVALID_ARGUMENTS, key)
                    else:
                        result[key] = val
                else:
                    if not check_argument_validity(val, condition):
                        return generate_error_msg(ERR_INVALID_ARGUMENTS, key)
                    else:
                        result[key] = val
            return func(qs_arguments=result, *args, **kwargs)
        return inner
    return decorator


def check_arguments(form=None, qs=None):
    if qs is None:
        qs = {}
    if form is None:
        form = {}

    def decorator(func):
        @wraps(func)
        @check_form_arguments(form)
        @check_qs_arguments(qs)
        def inner(*args, **kwargs):
            return func(form_arguments=kwargs["form_arguments"], qs_arguments=kwargs["qs_arguments"], *args, **kwargs)
        return inner
    return decorator


def make_serializable(obj):
    if isinstance(obj, list):
        result = []
        for item in obj:
            result.append(make_serializable(item))
        return result
    elif isinstance(obj, dict):
        result = {}
        for key in obj:
            result[make_serializable(key)] = make_serializable(obj[key])
        return result
    elif isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, bool) or isinstance(obj, str):
        return obj
    else:
        return str(obj)
