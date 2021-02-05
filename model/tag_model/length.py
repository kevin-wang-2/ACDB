import utils

ARGUMENT_LIST = ("length", )


def validate_arguments(args):
    if "length" not in args or not (utils.check_int(args["length"]) or utils.ARG_VEC_TABLE[float](args["length"])):
        return False
    return True


def generate_property(length):
    return {
        "length": float(length)
    }
