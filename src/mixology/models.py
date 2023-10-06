from pydantic import BaseModel


class Tasmota(BaseModel):
    """Tasmota model."""

    name: str
    relays: list[int]
    wifi: str = ""


class Client(BaseModel):
    tasmotas: list[Tasmota]
    key: str
    token: str


class TasmotaConfig(BaseModel):
    wifi_key: str
    wifi_pass: str
