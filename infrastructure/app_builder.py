import aws_cdk as cdk
from constructs import Construct

from infrastructure.configuration.loader import load_accounts_config, load_arch_config
from infrastructure.stacks.pipeline import PipelineStack, PipelineStackProps

DEFAULT_DEPLOYMENT_ID = "main"


def build_pipeline(app: Construct) -> None:
    # Load configuration of accounts
    deployment_id = app.node.try_get_context("deployment_id") or DEFAULT_DEPLOYMENT_ID
    accounts_config = load_accounts_config(deployment_id)
    arch_config = load_arch_config(deployment_id)

    project_name = arch_config.naming.project_name

    PipelineStack(
        app,
        f"{project_name}-pipeline",
        props=PipelineStackProps(deployment_id=deployment_id, accounts_config=accounts_config),
        env=cdk.Environment(account=accounts_config.get_pipeline_account_id(), region=arch_config.cicd_pipeline.region),
    )
