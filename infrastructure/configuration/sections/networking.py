from pydantic import BaseModel


class NetworkingConfig(BaseModel):
    vpc_cidr: str
    max_availability_zones: int
    nat_gateways: int
