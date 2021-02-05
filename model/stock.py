from model.conn import conn
from bson import ObjectId


def to_object_id(arr):
    slots = []
    for slot in arr:
        cur = []
        for tag in slot:
            cur.append(ObjectId(tag))
        slots.append(cur)
    return slots


def create_stock(name, slots):
    slots = to_object_id(slots)
    conn.insert("stock", {
        "name": name,
        "slots": slots
    })
