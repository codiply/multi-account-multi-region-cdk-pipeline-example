from pydantic import BaseModel

from infrastructure.configuration.sections.cicd_pipeline import CicdPipelineConfig
from infrastructure.configuration.sections.naming import NamingConfig
from infrastructure.configuration.sections.networking import NetworkingConfig
from infrastructure.configuration.sections.stacks import StacksConfig


class ArchConfig(BaseModel):
    cicd_pipeline: CicdPipelineConfig
    naming: NamingConfig
    stacks: StacksConfig
    networking: NetworkingConfig
