import typing

from pydantic import BaseModel


class AccountConfig(BaseModel):
    account_id: str
    is_cicd_account: typing.Optional[bool] = False
    is_enabled: typing.Optional[bool] = True
    needs_manual_approval: typing.Optional[bool] = True


class AccountsConfig(BaseModel):
    accounts: typing.Dict[str, AccountConfig]

    def get_pipeline_account_id(self) -> str:
        return next(acc for acc in self.accounts.values() if acc.is_cicd_account).account_id
