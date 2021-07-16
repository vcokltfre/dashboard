from pydantic import BaseModel


class SetConfig(BaseModel):
    value: str
