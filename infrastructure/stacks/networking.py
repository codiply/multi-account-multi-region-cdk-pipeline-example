import typing

import aws_cdk as cdk
from constructs import Construct
from pydantic import BaseModel

from infrastructure.components.vpc import Vpc, VpcProps
from infrastructure.configuration.sections.naming import NamingConfig
from infrastructure.configuration.sections.networking import NetworkingConfig


class NetworkingStackProps(BaseModel):
    naming: NamingConfig
    networking_config: NetworkingConfig


class NetworkingStack(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        props: NetworkingStackProps,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        Vpc(
            self,
            "vpc",
            VpcProps(
                naming=props.naming,
                cidr=props.networking_config.vpc_cidr,
                max_availability_zones=props.networking_config.max_availability_zones,
                nat_gateways=props.networking_config.nat_gateways,
            ),
        )
