from typing import List
import drawsvg as draw

def produce_scatter(data: List[int], height: int, width: int):
    point_distance = width/(len(data) - 1)
    vertical_scaling = height/max(data)

    drawing = draw.Drawing(width, height)
    background = draw.Rectangle(0, 0, width, height, fill="white")
    drawing.append(background)

    for i in range(len(data) - 1):
        distance = point_distance * i
        line = draw.Line(distance, height - (data[i] * vertical_scaling), distance + point_distance, height - (data[i + 1] * vertical_scaling), stroke='black')
        drawing.append(line)

    drawing.save_svg('example.svg')
    return True