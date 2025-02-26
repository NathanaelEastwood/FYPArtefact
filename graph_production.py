from typing import List
import drawsvg as draw
from drawsvg import Drawing

from request_body import RequestBody


def produce_scatter(request: RequestBody):

    # the amount of space reserved for rendering the horizontal and vertical axis
    x_axis_size = request.configuration.x_axis_size
    y_axis_size = request.configuration.y_axis_size

    # height of graph pane
    body_height = request.height - x_axis_size
    # width of graph pane
    body_width = request.width - y_axis_size

    # x distance per data point
    point_distance = body_width/(len(request.data) - 1)

    # y distance per data point
    vertical_scaling = abs(body_height/(max(request.data) - min(request.data)))

    # the amount to shift the graph vertically upwards if the minimum is below zero
    vertical_offset = min(min(request.data), 0)

    drawing = draw.Drawing(request.width, request.height)
    background = draw.Rectangle(0, 0, request.width, request.height, fill="white")
    drawing.append(background)

    for i in range(len(request.data) - 1):
        distance = point_distance * i

        line_start_x = distance + y_axis_size
        # y = 0 is at the top of the image, so we need to subtract the calculated value from the body height rather than add it.
        line_start_y = request.height - (request.data[i] * vertical_scaling + x_axis_size)

        line_end_x = line_start_x + point_distance
        line_end_y = request.height - (request.data[i + 1] * vertical_scaling + x_axis_size)

        line = draw.Line(line_start_x, line_start_y, line_end_x, line_end_y, stroke='black')
        drawing.append(line)

    drawing.save_svg('example.svg')
    return True

def generate_axis(drawing: Drawing, width: int, height: int) -> Drawing:

    # draw initial boundary line.

    return drawing