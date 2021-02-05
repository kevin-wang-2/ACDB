from functools import wraps
import model

import model.tag_model.length as length
import model.tag_model.socket as sock
import utils

GENERATOR_VEC_TABLE = {

}

VALIDATOR_VEC_TABLE = {

}

GENERATOR_ARGUMENT_TABLE = {

}


def generate_property(property_type, **args):
    return GENERATOR_VEC_TABLE[property_type](**args)


def check_model_arguments(property_type):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = {}
            for key in GENERATOR_ARGUMENT_TABLE[property_type]:
                val = utils.request.form.get(key)
                if val is None:
                    return utils.generate_error_msg(utils.ERR_INVALID_ARGUMENTS, key)
                result[key] = val
            if not VALIDATOR_VEC_TABLE[property_type](result):
                return utils.generate_error_msg(utils.ERR_INVALID_ARGUMENTS, "model")
            else:
                return func(model_arguments=result, *args, **kwargs)

        return inner

    return decorator


def add_generator(property_type, module):
    GENERATOR_VEC_TABLE[property_type] = module.generate_property
    VALIDATOR_VEC_TABLE[property_type] = module.validate_arguments
    GENERATOR_ARGUMENT_TABLE[property_type] = module.ARGUMENT_LIST


add_generator(model.tag.TAG_CATEGORY_LENGTH, length)
add_generator(model.tag.TAG_CATEGORY_SOCKET, sock)


def validate_tag_request(func):
    @wraps(func)
    def inner(*args, **kwargs):
        tag_category = utils.request.form.get("category")
        if not utils.check_int(tag_category):
            return utils.generate_error_msg(utils.ERR_INVALID_ARGUMENTS, "category")

        tag_name = utils.request.form.get("name")
        if not utils.check_str(tag_name):
            return utils.generate_error_msg(utils.ERR_INVALID_ARGUMENTS, "name")

        def curry(model_arguments, *args_in, **kwargs_in):
            return func(tag_category=int(tag_category), tag_name=tag_name,
                        tag_property=generate_property(int(tag_category), **model_arguments), *args_in, **kwargs_in)

        return check_model_arguments(int(tag_category))(curry)(*args, **kwargs)

    return inner
