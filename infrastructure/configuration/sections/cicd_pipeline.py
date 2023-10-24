from pydantic import BaseModel


class CicdPipelineConfig(BaseModel):
    github_repo: str
    github_token_secret_key: str
    git_branch: str
    region: str
