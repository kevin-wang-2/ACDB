from flask import Flask, send_file, request
from flask_cors import CORS
import utils
import auth
import model
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

app = Flask(__name__)

app.config["SECRET_KEY"] = config.get("web", "session_key")

cors = CORS(app, resources={r"/api/*": {"origins": "*", "supports_credentials": True}})


# Auth

@app.route("/api/login", methods=["POST"])
@utils.check_form_arguments({"username": str, "password": str})
def login(form_arguments):
    uid = form_arguments["username"]
    password = form_arguments["password"]
    success = auth.authenticate(uid, password)
    if success:
        success["success"] = True
        return success
    else:
        return {"success": False, "error": 0}


@app.route("/api/logout", methods=["GET", "DELETE"])
@auth.validate(0, False)
def logout():
    success = auth.deauthenticate()
    if success:
        return {"success": True}
    else:
        return {"success": False, "error": 0}


@app.route("/api/refresh", methods=["GET"])
@auth.validate(0, False)
def refresh_token():
    return auth.refresh_token()


# Member

@app.route("/api/member", methods=["GET"])
@auth.validate(0, False)
def list_member():
    it_members = model.member.list_member()
    return {"success": True, "data": [utils.make_serializable(member) for member in it_members]}


@app.route("/api/member", methods=["POST"])
@auth.validate(model.member.LEVEL_DEPLEADER, False)
@utils.check_form_arguments({
    "name": str,
    "sid": {"type": str, "length": 12, "re": "[0-9]+$"},
    "department": {"type": int, "min": model.member.DEPARTMENT_SOFA, "max": model.member.DEPARTMENT_SHOW}
})
def add_member(form_arguments):
    name = form_arguments["name"]
    sid = form_arguments["sid"]
    department = form_arguments["department"]
    password = config.get("member", "default_password")
    model.member.create_member(sid, name, password, int(department), model.member.LEVEL_MEMBER)
    return {"success": True}


@app.route("/api/member", methods=["DELETE"])
@auth.validate(model.member.LEVEL_LEADER, False)
@utils.check_qs_arguments({
    "sid": {"type": str, "length": 12, "re": "[0-9]+$"}
})
def retire_member(qs_arguments):
    sid = qs_arguments["sid"]
    result = model.member.retire_member(sid)
    if result.modified_count > 0:
        return {"success": True}
    else:
        return {"success": False, "error": 0}


@app.route("/api/member", methods=["PATCH"])
@auth.validate(model.member.LEVEL_LEADER, False)
@utils.check_qs_arguments({
    "sid": {"type": str, "length": 12, "re": "[0-9]+$"},
    "level": {"type": int, "min": model.member.LEVEL_MEMBER, "max": model.member.LEVEL_LEADER}
})
def promote_member(qs_arguments):
    sid = qs_arguments["sid"]
    level = int(qs_arguments["level"])
    result = model.member.promote_member(sid, level)
    if result.modified_count > 0:
        return {"success": True}
    else:
        return {"success": False, "error": 0}


# Tag

@app.route("/api/tag", methods=["GET"])
@auth.validate(0, False)
def list_tag():
    tags = model.tag.list_tag().sort("property")
    return {"success": True, "data": [utils.make_serializable(tag) for tag in tags]}


@app.route("/api/tag/<id>", methods=["GET"])
def find_tag(id):
    try:
        return {"success": True, "data": utils.make_serializable(model.tag.search_tag_by_id(id))}
    except:
        return {"success": False, "error": -1}


@app.route("/api/tag", methods=["POST"])
@auth.validate(0, False)
@model.tag_model.validate_tag_request
def add_tag(tag_category, tag_name, tag_property):
    model.tag.create_tag(tag_name, tag_category, **tag_property)
    return {"success": True}


@app.route("/api/tag", methods=["DELETE"])
@auth.validate(model.member.LEVEL_DEPLEADER, False)
@utils.check_qs_arguments({
    "id": str
})
def del_tag(qs_arguments):
    model.tag.delete_tad(qs_arguments["id"])
    return {"success": True}


# Stock

@app.route("/api/stock", methods=["POST"])
@auth.validate(0, False)
@model.stock.validate_stock_request
def add_stock(name, slots, rent):
    model.stock.create_stock(name, slots, rent)
    return {"success": True}


@app.route("/api/stock", methods=["GET"])
def list_stock():
    stock = model.stock.list_stock()
    return {"success": True, "data": [utils.make_serializable(tag) for tag in stock]}


# Static

@app.route("/")
def index():
    return send_file("templates/index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
