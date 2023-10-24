from pydantic import BaseModel


class AccountsConfig(BaseModel):
    tool: str
    dev: str
    pre: str
    prod: str
