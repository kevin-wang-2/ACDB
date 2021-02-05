from model.conn import conn
from bson import ObjectId
from utils import sha256

# DEPARTMENT
DEPARTMENT_SOFA = 0
DEPARTMENT_TECH = 1
DEPARTMENT_CONT = 2
DEPARTMENT_PROP = 3
DEPARTMENT_MEDIA = 4
DEPARTMENT_SHOW = 5

# LEVEL
LEVEL_RETIRE = 0
LEVEL_MEMBER = 1
LEVEL_DEPLEADER = 2
LEVEL_LEADER = 3
LEVEL_ADMIN = 4


def create_member(sid, name, password, department, level):
    result = conn.insert("member", {
        "sid": sid,
        "name": name,
        "password": sha256(password),
        "department": department,
        "level": level
    })
    return result.inserted_id


def search_member_by_ID(_id):
    return conn.find("member", {
        "_id": ObjectId(_id)
    }).next()


def search_member_by_SID(sid):
    return conn.find("member", {
        "sid": sid
    }).next()


def search_member_by_name(name):
    return conn.find("member", {
        "name": name
    })


def list_member():
    return conn.find("member", {})


def retire_member(sid):
    return conn.update({
        "sid": ObjectId(sid)
    }, {
        "$set": {
            "level": LEVEL_RETIRE
        }
    })


def promote_member(sid, level):
    return conn.update({
        "sid": ObjectId(sid)
    }, {
        "$set": {
            "level": level
        }
    })
