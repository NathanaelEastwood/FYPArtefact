from typing import List

from pydantic import BaseModel


class Configuration(BaseModel):
    x_axis_size: int
    y_axis_size: int
    bar_chart_labels: List[str]