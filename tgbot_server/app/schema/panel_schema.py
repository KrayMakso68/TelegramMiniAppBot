from py3xui import Client

from app.schema.base_schema import BaseSchema


class ClientSchema(Client, BaseSchema):
    """Represents a client in the XUI API.

        Attributes:
            email (str): The email of the client. Required.
            enable (bool): Whether the client is enabled. Required.
            id (int | str): The ID of the client. Required.
            inbound_id (int | None): The ID of the inbound connection. Optional.
            up (int): The upload speed of the client. Optional.
            down (int): The download speed of the client. Optional.
            expiry_time (int): The expiry time of the client. Optional.
            total (int): The total amount of data transferred by the client. Optional.
            reset (int): The time at which the client's data was last reset. Optional.
            flow (str): The flow of the client. Optional.
            limit_ip (int): The limit of IPs for the client. Optional.
            sub_id (str): The sub ID of the client. Optional.
            tg_id (str): The Telegram ID of the client. Optional.
            total_gb (int): The total amount of data transferred by the client in GB. Optional.
    """
    # limit_ip: int = 1,
    # enable: bool = True,



class ClientCreate(BaseSchema):
    ...
