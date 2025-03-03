from typing import List
import drawsvg as draw
from drawsvg import Drawing

from request_body import RequestBody


def produce_scatter(request: RequestBody):

    # Define padding for the axes (to prevent clipping)
    y_axis_padding_top = 20  # Padding at the top of y-axis
    x_axis_padding_right = 20  # Padding at the right of x-axis
    
    # Create drawing with adjusted height to account for padding
    total_height = request.height + y_axis_padding_top
    drawing = draw.Drawing(request.width, total_height)
    background = draw.Rectangle(0, 0, request.width, total_height, fill="white")
    drawing.append(background)
    
    # the amount of space reserved for rendering the horizontal and vertical axis
    x_axis_size = request.configuration.x_axis_size
    y_axis_size = request.configuration.y_axis_size

    # height of graph pane (accounting for padding)
    body_height = request.height - x_axis_size
    # width of graph pane (accounting for padding)
    body_width = request.width - y_axis_size - x_axis_padding_right

    # Get the actual data range
    data_min = int(min(request.data))
    actual_max = max(request.data)
    
    # Calculate number of steps needed to cover the range
    num_y_ticks = 5
    data_range = actual_max - data_min
    y_step = max(1, int((data_range + num_y_ticks - 1) / (num_y_ticks - 1)))  # Ceiling division
    
    # Calculate adjusted max to ensure it's above the actual maximum
    adjusted_max = data_min + y_step * (num_y_ticks - 1)
    while adjusted_max < actual_max:  # Ensure adjusted_max is never less than actual_max
        y_step += 1
        adjusted_max = data_min + y_step * (num_y_ticks - 1)
    
    # Use adjusted range for scaling
    data_range = adjusted_max - data_min

    # x distance per data point
    point_distance = body_width/(len(request.data) - 1)

    # y distance per data point using adjusted range
    vertical_scaling = abs(body_height/data_range)

    for i in range(len(request.data) - 1):
        distance = point_distance * i

        line_start_x = distance + y_axis_size
        # y = 0 is at the top of the image, so we need to subtract the calculated value from the body height rather than add it.
        line_start_y = total_height - ((request.data[i] - data_min) * vertical_scaling + x_axis_size)

        line_end_x = line_start_x + point_distance
        line_end_y = total_height - ((request.data[i + 1] - data_min) * vertical_scaling + x_axis_size)

        line = draw.Line(line_start_x, line_start_y, line_end_x, line_end_y, stroke='black')
        drawing.append(line)

    drawing.save_svg('example.svg')
    
    # Add axes with scales
    drawing = generate_axis(drawing, request, vertical_scaling, data_min, y_step, adjusted_max, total_height)
    
    drawing.save_svg('example.svg')
    return True

def generate_axis(drawing: Drawing, request: RequestBody, vertical_scaling: float, data_min: int, y_step: int, adjusted_max: float, total_height: int) -> Drawing:
    # Draw y-axis (vertical line)
    y_axis = draw.Line(
        request.configuration.y_axis_size, 
        total_height - request.configuration.x_axis_size,
        request.configuration.y_axis_size, 
        0,  # Start from the very top
        stroke='black'
    )
    drawing.append(y_axis)

    # Draw x-axis (horizontal line)
    x_axis = draw.Line(
        request.configuration.y_axis_size,
        total_height - request.configuration.x_axis_size,
        request.width - 20,  # Add right padding
        total_height - request.configuration.x_axis_size,
        stroke='black'
    )
    drawing.append(x_axis)

    # Add y-axis scale markers and values with whole number snapping
    num_y_ticks = 5
    
    for i in range(num_y_ticks):
        value = adjusted_max - (i * y_step)
        y_pos = total_height - ((value - data_min) * vertical_scaling + request.configuration.x_axis_size)
        
        # Draw tick mark
        tick = draw.Line(
            request.configuration.y_axis_size - 5,
            y_pos,
            request.configuration.y_axis_size + 5,
            y_pos,
            stroke='black'
        )
        drawing.append(tick)
        
        # Add value label (now always whole numbers)
        label = draw.Text(
            str(int(value)),  # Ensure integer display
            8,  # font size
            request.configuration.y_axis_size - 10,
            y_pos + 3,  # slight vertical adjustment for centering
            text_anchor='end'
        )
        drawing.append(label)

    # Add x-axis scale markers and values (already whole numbers as indices)
    num_x_ticks = min(len(request.data), 10)  # Don't overcrowd the x-axis
    x_step = max(1, (len(request.data) - 1) // (num_x_ticks - 1))  # Ensure whole number steps
    point_distance = (request.width - request.configuration.y_axis_size - 20) / (len(request.data) - 1)  # Account for right padding

    # Adjust number of x ticks based on whole number step
    num_x_ticks = ((len(request.data) - 1) // x_step) + 1

    for i in range(num_x_ticks):
        data_index = i * x_step
        x_pos = request.configuration.y_axis_size + (data_index * point_distance)
        
        # Draw tick mark
        tick = draw.Line(
            x_pos,
            total_height - request.configuration.x_axis_size - 5,
            x_pos,
            total_height - request.configuration.x_axis_size + 5,
            stroke='black'
        )
        drawing.append(tick)
        
        # Add value label
        label = draw.Text(
            str(data_index),
            8,  # font size
            x_pos,
            total_height - request.configuration.x_axis_size + 20,
            text_anchor='middle'
        )
        drawing.append(label)

    return drawing