from typing import List

from pydantic import BaseModel


class RequestBody(BaseModel):
    type: str
    data: List[int]
    height: int
    width: int
