from pydantic import BaseModel


class Configuration(BaseModel):
    x_axis_size: int
    y_axis_size: int