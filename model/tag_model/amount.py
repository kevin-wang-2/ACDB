import utils

ARGUMENT_LIST = ("amount", )


def validate_arguments(args):
    if "amount" not in args or not utils.check_int(args["amount"]):
        return False
    return True


def generate_property(amount):
    return {
        "amount": float(amount)
    }
