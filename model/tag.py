from model.conn import conn
import bson

# TAG_CATEGORY

TAG_CATEGORY_ATTRIBUTE = 0  # 属性
TAG_CATEGORY_LENGTH = 1  # 长度
TAG_CATEGORY_SOCKET = 2  # 接口
TAG_CATEGORY_POSITION = 0xff  # 位置


def create_tag(name, category, **props):
    result = conn.insert("tag", {
        "name": name,
        "category": category,
        "property": props
    })
    return result.inserted_id


def search_tag_by_name(name):
    return conn.find("tag", {
        "name": name
    })


def search_tag_by_property(category, **props):
    cc_props = {}
    for key in props:
        cc_props["property." + key] = props[key]
    cc_props["category"] = category
    return conn.find("tag", cc_props)


def search_tag_by_id(id):
    _id = bson.ObjectId(id)
    return conn.find("tag", {
        "_id": _id
    }).next()


def list_tag():
    return conn.find("tag", {})


def delete_tad(_id):
    return conn.delete("tag", {
        "_id": bson.ObjectId(_id)
    })
