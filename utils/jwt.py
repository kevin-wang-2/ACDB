import hmac
import configparser
import base64
import time
import json

config = configparser.ConfigParser()
config.read("config.ini")

HEADER = {
    "typ": "JWT",
    "alg": "HS256"
}


class SnowFlake:
    def __init__(self, data_id):
        self.start = int(time.mktime(time.strptime('2018-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")))
        self.last = int(time.time())
        self.countID = 0
        self.dataID = data_id  # 数据ID，这个自定义或是映射

    def get_id(self):
        # 时间差部分
        now = int(time.time())
        temp = now - self.start
        if len(str(temp)) < 9:  # 时间差不够9位的在前面补0
            length = len(str(temp))
            s = "0" * (9 - length)
            temp = s + str(temp)
        if now == self.last:
            self.countID += 1  # 同一时间差，序列号自增
        else:
            self.countID = 0  # 不同时间差，序列号重新置为0
            self.last = now
        # 标识ID部分
        if len(str(self.dataID)) < 2:
            length = len(str(self.dataID))
            s = "0" * (2 - length)
            self.dataID = s + str(self.dataID)
        # 自增序列号部分
        if self.countID == 99999:  # 序列号自增5位满了，睡眠一秒钟
            time.sleep(1)
        count_id_data = str(self.countID)
        if len(count_id_data) < 5:  # 序列号不够5位的在前面补0
            length = len(count_id_data)
            s = "0" * (5 - length)
            count_id_data = s + count_id_data
        sf_id = str(temp) + str(self.dataID) + count_id_data
        return sf_id


MACHINE = 0


class JWT:
    def __init__(self, payload_key):
        global MACHINE
        self.payload_key = payload_key
        self.secret = config.get("JWT", "secret")
        self.iss = config.get("JWT", "iss")
        self.expire = int(config.get("JWT", "expire"))
        self.sf_generator = SnowFlake(MACHINE)
        MACHINE += 1

    def generate(self, data):
        assert (tuple(data.keys()) == tuple(self.payload_key))
        payload = {
            "iss": self.iss,
            "exp": int(time.time() * 1000) + self.expire,
            "iat": int(time.time() * 1000),
            "jti": self.sf_generator.get_id()
        }
        for key in data:
            payload[key] = data[key]

        header_str = base64.b64encode(json.dumps(HEADER).encode("utf-8")).decode("utf-8")
        payload_str = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")

        h = hmac.new(self.secret.encode("utf-8"), (header_str + "." + payload_str).encode("utf-8"), digestmod='SHA256')
        signature = base64.b64encode(h.digest())

        return header_str + "." + payload_str + "." + signature.decode("utf-8")

    def validate(self, token):
        [header_str, payload_str, signature] = token.split(".")
        header_str_calculated = base64.b64encode(json.dumps(HEADER).encode("utf-8")).decode("utf-8")
        if header_str_calculated != header_str:
            return False
        h = hmac.new(self.secret.encode("utf-8"), (header_str + "." + payload_str).encode("utf-8"), digestmod='SHA256')
        signature_calculated = base64.b64encode(h.digest())
        if signature_calculated != signature.encode("utf-8"):
            return False
        data = json.loads(base64.b64decode(payload_str.encode("utf-8")).decode("utf-8"))
        if data["exp"] > time.time() * 10000:
            return False
        else:
            return data
