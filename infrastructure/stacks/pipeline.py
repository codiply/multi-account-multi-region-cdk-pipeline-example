import typing

import aws_cdk as cdk
from aws_cdk import pipelines
from constructs import Construct
from pydantic import BaseModel

from infrastructure.configuration.configs.accounts import AccountsConfig
from infrastructure.configuration.loader import load_arch_config
from infrastructure.stages.architecture import ArchStage, ArchStageProps


class PipelineStackProps(BaseModel):
    deployment_id: str
    accounts_config: AccountsConfig


class PipelineStack(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        props: PipelineStackProps,
        **kwargs: typing.Any,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        config = load_arch_config(props.deployment_id)
        project_name = config.naming.project_name

        pipeline = pipelines.CodePipeline(
            self,
            "pipeline",
            pipeline_name=f"{project_name}",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.git_hub(
                    repo_string=config.cicd_pipeline.github_repo,
                    branch=config.cicd_pipeline.git_branch,
                    authentication=cdk.SecretValue.secrets_manager(config.cicd_pipeline.github_token_secret_key),
                ),
                commands=[
                    "npm install -g aws-cdk",
                    "python -m pip install -r requirements/requirements.txt",
                    "cdk synth",
                ],
            ),
            cross_account_keys=True,
        )

        for environment_id, account_config in props.accounts_config.accounts.items():
            if account_config.is_enabled and not account_config.is_cicd_account:
                wave = pipeline.add_wave(f"wave-{environment_id}")

                account_config = props.accounts_config.accounts[environment_id]
                account_id = account_config.account_id

                if account_config.needs_manual_approval:
                    wave.add_pre(
                        pipelines.ManualApprovalStep(
                            f"approve-{environment_id}", comment=f"Approve deployment to {environment_id}"
                        )
                    )

                wave.add_stage(
                    ArchStage(
                        self,
                        f"{project_name}-{environment_id}",
                        props=ArchStageProps(deployment_id=props.deployment_id, environment_id=environment_id),
                        env=cdk.Environment(account=account_id),
                    )
                )
