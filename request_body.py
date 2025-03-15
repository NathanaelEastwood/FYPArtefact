from typing import List

from pydantic import BaseModel

from configuration_body import Configuration


class RequestBodyOneDimensional(BaseModel):
    type: str
    data: List[float]
    height: int
    width: int
    line_name: str
    configuration: Configuration

class RequestBodyTwoDimensional(BaseModel):
    type: str
    data: List[List[float]]
    height: int
    width: int
    line_name: str
    configuration: Configuration