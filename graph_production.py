import math

from DrawingEngine import DrawingEngine
from request_body import RequestBodyOneDimensional, RequestBodyTwoDimensional
import numpy as np


def generate_line_graph(request: RequestBodyOneDimensional):

    drawing = DrawingEngine("example.svg")
    drawing.establish_headers(request.width, request.height + 20)
    drawing.draw_rect(0, 0, request.width, request.height + 20, "white")

    data_min = min(request.data)
    data_max = max(request.data)
    graph_value_range = abs(data_min - data_max)

    # This is the number of pixels per 1 change in the graph data
    vertical_scaling = (request.height - request.configuration.x_axis_size)/graph_value_range

    # This is the distance between each data point horizontally
    horizontal_scaling = (request.width - request.configuration.y_axis_size)/len(request.data)
    current_line_start = request.configuration.y_axis_size

    for i in range(len(request.data) - 1):

        line_start_x = current_line_start
        # y = 0 is at the top of the image, so we need to subtract the calculated value from the body height rather than add it.
        line_start_y = request.height - ((request.data[i] - data_min) * vertical_scaling + request.configuration.x_axis_size)

        line_end_x = current_line_start + horizontal_scaling
        line_end_y = request.height - ((request.data[i + 1] - data_min) * vertical_scaling + request.configuration.x_axis_size)

        drawing.draw_line(line_start_x, line_start_y + 20, line_end_x, line_end_y + 20, 'black', 'red','main_line', True)
        current_line_start += horizontal_scaling

    # Add axes with scales
    drawing = generate_y_axis(drawing, request)
    drawing = generate_x_axis(drawing, request)

    drawing.close_file()
    return True

def generate_scatter_plot(request: RequestBodyTwoDimensional):

    drawing = DrawingEngine("example")
    drawing.establish_headers(request.width, request.height)
    drawing.draw_rect(0, 0, request.width, request.height, "white")
    array = np.array(request.data)
    highest_value = np.max(array[:, 0])
    lowest_value = np.min(array[:, 0])
    data_range = abs(highest_value - lowest_value)
    vertical_scaling = request.height / data_range

    # Define padding for the axes (to prevent clipping)
    y_axis_padding_top = 20  # Padding at the top of y-axis
    x_axis_padding_right = 20  # Padding at the right of x-axis

    # Create drawing with adjusted height to account for padding
    total_height = request.height + y_axis_padding_top

    drawing = DrawingEngine("example.svg")
    drawing.establish_headers(request.width, total_height)
    drawing.draw_rect(0, 0, request.width, total_height, "white")

    # the amount of space reserved for rendering the horizontal and vertical axis
    x_axis_size = request.configuration.x_axis_size
    y_axis_size = request.configuration.y_axis_size

    # height of graph pane (accounting for padding)
    body_height = request.height - x_axis_size
    # width of graph pane (accounting for padding)
    body_width = request.width - y_axis_size - x_axis_padding_right

    # Calculate optimal number of y-axis ticks (aim for roughly 50 pixels between ticks)
    optimal_tick_spacing = 50  # pixels between ticks
    num_y_ticks = max(3, min(10, int(body_height / optimal_tick_spacing)))

    y_step = max(1, int((data_range + num_y_ticks - 1) / (num_y_ticks - 1)))  # Ceiling division
    adjusted_max = lowest_value + y_step * (num_y_ticks - 1)

    drawing = generate_y_axis(drawing, request)

    return True

import math

def generate_y_axis(drawing: DrawingEngine, request) -> DrawingEngine:
    # Draw the y-axis
    drawing.draw_line(request.configuration.y_axis_size, request.height - request.configuration.x_axis_size + 20,
                      request.configuration.y_axis_size, 20, 'black', 'black', 'x_axis', False)

    data_min = min(request.data)
    data_max = max(request.data)
    graph_value_range = abs(data_max - data_min)

    tick_interval = get_nice_number(graph_value_range / 5)  # Aim for ~5 ticks
    number_of_y_ticks = math.ceil(graph_value_range / tick_interval)

    # Calculate vertical scaling
    vertical_scaling = (request.height - request.configuration.x_axis_size) / graph_value_range

    # Compute first tick position
    y_tick_offset = tick_interval * vertical_scaling
    current_y_tick_value = math.ceil(data_min / tick_interval) * tick_interval
    current_y_tick_offset = request.height - request.configuration.x_axis_size - (current_y_tick_value - data_min) * vertical_scaling

    # Draw ticks and labels
    for i in range(number_of_y_ticks + 1):
        position_text = str(int(current_y_tick_value))

        drawing.draw_line(request.configuration.y_axis_size, current_y_tick_offset + 20,
                          request.configuration.y_axis_size / 1.4, current_y_tick_offset + 20, "black", "black", "tick", False)
        drawing.draw_text(request.configuration.y_axis_size / 1.5, current_y_tick_offset + 22, 8, "end", position_text)

        current_y_tick_value += tick_interval
        current_y_tick_offset -= y_tick_offset

    return drawing


def generate_x_axis(drawing: DrawingEngine, request):
    # Draw the x-axis
    drawing.draw_line(request.configuration.y_axis_size, (request.height - request.configuration.x_axis_size) + 20,
                      request.width - 20, (request.height - request.configuration.x_axis_size)  + 20, 'black', 'black',
                      'x_axis', False)

    graph_value_range = len(request.data)

    # Choose a "nice" tick interval
    tick_interval = get_nice_number(graph_value_range / 5)  # Aim for ~5 ticks
    number_of_x_ticks = math.ceil(graph_value_range / tick_interval)

    # Calculate horizontal scaling
    horizontal_scaling = (request.width - request.configuration.y_axis_size - 20) / graph_value_range

    # Compute first tick position
    x_tick_offset = tick_interval * horizontal_scaling
    current_x_tick_value = math.ceil(request.configuration.y_axis_size / tick_interval) * tick_interval
    current_x_tick_offset = request.configuration.y_axis_size + (
                current_x_tick_value - request.configuration.y_axis_size) * horizontal_scaling

    # Draw x-axis ticks and labels
    for i in range(number_of_x_ticks + 1):
        position_text = str(int(current_x_tick_offset/horizontal_scaling))

        drawing.draw_line(current_x_tick_offset, (request.height - request.configuration.x_axis_size) + 20,
                          current_x_tick_offset, (request.height - request.configuration.x_axis_size) + 25, "black",
                          "black", "tick", False)
        drawing.draw_text(current_x_tick_offset, (request.height - request.configuration.x_axis_size) + 35, 8,
                          "middle", position_text)

        current_x_tick_offset += x_tick_offset

    return drawing

def get_nice_number(value):
    exponent = math.floor(math.log10(value))  # Order of magnitude
    fraction = value / (10 ** exponent)  # Fractional part
    if fraction <= 1.5:
        nice_fraction = 1
    elif fraction <= 3:
        nice_fraction = 2
    elif fraction <= 7:
        nice_fraction = 5
    else:
        nice_fraction = 10
    return nice_fraction * (10 ** exponent)