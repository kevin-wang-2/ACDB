import utils

ARGUMENT_LIST = ("socket", )


SOCKET_TYPE_MIN = 0
SOCKET_TYPE_MAX = 100


def validate_arguments(args):
    if "socket" not in args or not utils.check_int(args["socket"]) or\
            int(args["socket"]) < SOCKET_TYPE_MIN or int(args["socket"]) > SOCKET_TYPE_MAX:
        return False
    return True


def generate_property(socket):
    return {
        "socket": socket
    }
