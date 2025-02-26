from typing import List

from pydantic import BaseModel

from configuration_body import Configuration


class RequestBody(BaseModel):
    type: str
    data: List[int]
    height: int
    width: int
    configuration: Configuration
