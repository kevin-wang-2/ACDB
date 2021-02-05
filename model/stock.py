from flask import request
from model.conn import conn
from bson import ObjectId
from functools import wraps
import utils


def to_object_id(arr):
    slots = []
    for slot in arr:
        cur = []
        for tag in slot:
            cur.append(ObjectId(tag))
        slots.append(cur)
    return slots


def create_stock(name, slots, rent):
    slots = to_object_id(slots)
    conn.insert("stock", {
        "name": name,
        "slots": slots,
        "rent": rent
    })


def list_stock():
    return conn.find("stock", {})


def validate_stock_request(func):
    @wraps(func)
    def inner(*args, **kwargs):
        name = utils.request.form.get("name")
        if not utils.check_str(name):
            return utils.generate_error_msg(utils.ERR_INVALID_ARGUMENTS, "name")

        rent = utils.request.form.get("rent")
        if not utils.check_re_generator(utils.RE_BOOL)(rent):
            return utils.generate_error_msg(utils.ERR_INVALID_ARGUMENTS, "rent")

        form = request.form.to_dict()
        slots = []
        for key in form:
            if key[0:6] == "slots[":
                first = int(key[6:key.find("][")])
                while len(slots) <= first:
                    slots.append([])
                slots[first].append(form[key])

        return func(name=name, slots=slots, rent=(rent == "true" or rent == "True"), *args, **kwargs)

    return inner
