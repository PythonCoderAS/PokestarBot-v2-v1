import dataclasses
import json
from typing import Union, Any


@dataclasses.dataclass(frozen=True)
class Response:
    name: str
    message: str
    code: int
    extra: dict = dataclasses.field(default_factory=dict)

    def to_json(self):
        return {
            "type": self.name,
            "code": self.code,
            "message": self.message,
            "extra": self.extra,
        }


class ResponseSerializer(json.JSONEncoder):
    def default(self, o: Union[Response, Any]) -> dict:
        if isinstance(o, Response):
            return o.to_json()
        return super().default(o)
