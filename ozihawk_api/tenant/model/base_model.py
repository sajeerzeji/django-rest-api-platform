import json


class BaseModel():
    def toJSON(self):
        jsonResponse = {}
        try:
            dump = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
            if dump is not None:
                res = json.loads(dump)
                if res is not None:
                    res = {k: v for k, v in res.items() if v is not None}
                    jsonResponse = res
            return jsonResponse
        except Exception as ex:
            return jsonResponse