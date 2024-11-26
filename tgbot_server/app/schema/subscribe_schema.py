from pydantic import model_validator
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

from app.schema.base_schema import BaseSchema


class BaseConfig(BaseSchema):
    uuid: str
    address: str
    inbound_name: str
    email: str


class VlessConfig(BaseConfig):
    port: int
    flow: str
    fingerprint: str
    public_key: str
    security: str
    sid: str
    sni: str
    spider_path: str
    connection_type: str

    @model_validator(mode="before")
    @classmethod
    def check_fields_not_empty(cls, values):
        required_fields = [
            'uuid', 'address', 'port', 'flow', 'fingerprint', "public_key",
            'security', 'sid', 'sni', 'spider_path', 'connection_type', 'inbound_name', 'email'
        ]
        for field in required_fields:
            if not values.get(field):
                raise ValueError(f"Field {field} cannot be empty!")
        return values

    @classmethod
    def from_url(cls, url: str):
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        fragment = parsed_url.fragment.split("-")

        return cls(
            uuid=parsed_url.username,
            address=parsed_url.hostname,
            port=parsed_url.port,
            flow=query_params.get("flow")[0],
            fingerprint=query_params.get("fp")[0],
            public_key=query_params.get("pbk")[0],
            security=query_params.get("security")[0],
            sid=query_params.get("sid")[0],
            sni=query_params.get("sni")[0],
            spider_path=query_params.get("spx")[0],
            connection_type=query_params.get("type")[0],
            inbound_name=fragment[0],
            email=fragment[1]
        )

    def to_url(self) -> str:
        query_params = {
            "flow": self.flow,
            "fp": self.fingerprint,
            "pbk": self.public_key,
            "security": self.security,
            "sid": self.sid,
            "sni": self.sni,
            "spx": self.spider_path,
            "type": self.connection_type
        }

        # query_params = {k: v for k, v in query_params.items() if v}

        url = urlunparse((
            "vless",
            f"{self.uuid}@{self.address}:{self.port}",
            "",
            "",
            urlencode(query_params),
            f"{self.inbound_name}-{self.email}"
        ))

        return url


class ConnectSchema(BaseSchema):
    connect_url: str
    uuid: str
    email: str
    inbound_name: str

    @model_validator(mode="before")
    @classmethod
    def check_fields_not_empty(cls, values):
        required_fields = ['connect_url', 'uuid', 'inbound_name', 'email']
        for field in required_fields:
            if not values.get(field):
                raise ValueError(f"Field {field} cannot be empty!")
        return values

    @classmethod
    def from_url(cls, url: str):
        parsed_url = urlparse(url)
        fragment = parsed_url.fragment.split("-")

        return cls(
            connect_url=url,
            uuid=parsed_url.username,
            inbound_name=fragment[0],
            email=fragment[-1]
        )
