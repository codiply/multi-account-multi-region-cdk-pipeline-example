import typing

from pydantic import BaseModel


class StackConfig(BaseModel):
    regions: typing.List[str]


class StacksConfig(BaseModel):
    networking: StackConfig
