import typing

import aws_cdk as cdk
from constructs import Construct
from pydantic import BaseModel

from infrastructure.configuration.loader import load_arch_config
from infrastructure.stacks.networking import NetworkingStack, NetworkingStackProps


class ArchStageProps(BaseModel):
    deployment_id: str
    environment_id: str


class ArchStage(cdk.Stage):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        props: ArchStageProps,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        config = load_arch_config(deployment_id=props.deployment_id, environment_id=props.environment_id)

        for region in config.stacks.networking.regions:
            NetworkingStack(
                self,
                f"networking-{region}",
                NetworkingStackProps(naming=config.naming, networking_config=config.networking),
                env=cdk.Environment(region=region),
            )
