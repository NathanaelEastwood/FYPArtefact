from typing import List

from pydantic import BaseModel

from configuration_body import Configuration


class RequestBody(BaseModel):
    type: str
    data: List[float]
    height: int
    width: int
    line_name: str
    configuration: Configuration
