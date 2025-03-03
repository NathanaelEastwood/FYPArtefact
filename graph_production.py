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
    
    # Add axes with scales
    drawing = generate_axis(drawing, request, vertical_scaling)
    
    drawing.save_svg('example.svg')
    return True

def generate_axis(drawing: Drawing, request: RequestBody, vertical_scaling: float) -> Drawing:
    # Draw y-axis (vertical line)
    y_axis = draw.Line(
        request.configuration.y_axis_size, 
        request.height - request.configuration.x_axis_size,
        request.configuration.y_axis_size, 
        0, 
        stroke='black'
    )
    drawing.append(y_axis)

    # Draw x-axis (horizontal line)
    x_axis = draw.Line(
        request.configuration.y_axis_size,
        request.height - request.configuration.x_axis_size,
        request.width,
        request.height - request.configuration.x_axis_size,
        stroke='black'
    )
    drawing.append(x_axis)

    # Add y-axis scale markers and values
    data_min = min(request.data)
    data_max = max(request.data)
    num_y_ticks = 5
    y_step = (data_max - data_min) / (num_y_ticks - 1)
    
    for i in range(num_y_ticks):
        value = data_max - (i * y_step)
        y_pos = request.height - (value * vertical_scaling + request.configuration.x_axis_size)
        
        # Draw tick mark
        tick = draw.Line(
            request.configuration.y_axis_size - 5,
            y_pos,
            request.configuration.y_axis_size + 5,
            y_pos,
            stroke='black'
        )
        drawing.append(tick)
        
        # Add value label
        label = draw.Text(
            str(round(value, 1)),
            8,  # font size
            request.configuration.y_axis_size - 10,
            y_pos + 3,  # slight vertical adjustment for centering
            text_anchor='end'
        )
        drawing.append(label)

    # Add x-axis scale markers and values
    num_x_ticks = min(len(request.data), 10)  # Don't overcrowd the x-axis
    x_step = (len(request.data) - 1) / (num_x_ticks - 1)
    point_distance = (request.width - request.configuration.y_axis_size) / (len(request.data) - 1)

    for i in range(num_x_ticks):
        data_index = round(i * x_step)
        x_pos = request.configuration.y_axis_size + (data_index * point_distance)
        
        # Draw tick mark
        tick = draw.Line(
            x_pos,
            request.height - request.configuration.x_axis_size - 5,
            x_pos,
            request.height - request.configuration.x_axis_size + 5,
            stroke='black'
        )
        drawing.append(tick)
        
        # Add value label
        label = draw.Text(
            str(data_index),
            8,  # font size
            x_pos,
            request.height - request.configuration.x_axis_size + 20,
            text_anchor='middle'
        )
        drawing.append(label)

    return drawing