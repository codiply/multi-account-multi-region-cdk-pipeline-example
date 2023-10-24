import typing

import aws_cdk as cdk
from aws_cdk import aws_ec2 as ec2
from constructs import Construct
from pydantic import BaseModel

from infrastructure.configuration.sections.naming import NamingConfig


class VpcProps(BaseModel):
    naming: NamingConfig
    name_suffix: typing.Optional[str] = None
    cidr: typing.Optional[str] = None
    max_availability_zones: int
    nat_gateways: typing.Optional[int] = None


class Vpc(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        props: VpcProps,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc_name = props.naming.prefix

        if props.name_suffix is not None:
            vpc_name += f"-{props.name_suffix}"

        vpc = ec2.Vpc(
            self,
            "vpc",
            ip_addresses=ec2.IpAddresses.cidr(props.cidr or "10.0.0.0/16"),
            max_azs=props.max_availability_zones,
            nat_gateways=props.nat_gateways,
        )

        cdk.Tags.of(vpc).add("Name", vpc_name)
