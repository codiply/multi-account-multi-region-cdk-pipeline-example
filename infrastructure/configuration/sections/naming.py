from pydantic import BaseModel


class EnvironmentNamingConfig(BaseModel):
    short_name: str
    complete_name: str


class NamingConfig(BaseModel):
    project_name: str
    environment: EnvironmentNamingConfig

    @property
    def prefix(self) -> str:
        return f"{self.project_name}-{self.environment.short_name}"
