import json
from typing import Any


dct = {"id": 1, "name": "Irina"}
print(type(dct))

json_dct = json.dumps(dct)
print(json_dct)
print(type(json_dct))

print(json.loads(json_dct))