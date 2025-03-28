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

        drawing.draw_line(line_start_x, line_start_y + 20, line_end_x, line_end_y + 20, 'black', 'red','main_line', True, line_width=1)
        current_line_start += horizontal_scaling

    # Add axes with scales
    drawing = generate_y_axis(drawing, request)
    drawing = generate_x_axis(drawing, request)

    drawing.close_file()
    return True

def generate_scatter_plot(request: RequestBodyTwoDimensional):

    drawing = DrawingEngine("example.svg")
    drawing.establish_headers(request.width, request.height + 20)
    drawing.draw_rect(0, 0, request.width, request.height + 20, "white")

    array = np.array(request.data)
    starting_point = np.min(array[:, 1])
    ending_point = np.max(array[:, 1])
    data_min = np.min(array[:, 0])
    data_max = np.max(array[:, 0])
    graph_value_range = abs(data_max - data_min)
    graph_horizontal_data_range = abs(ending_point - starting_point)
    # This is the number of pixels per 1 change in the graph data
    vertical_scaling = (request.height - request.configuration.x_axis_size) / graph_value_range

    # This is the distance between each data point horizontally
    horizontal_scaling = (request.width - request.configuration.y_axis_size - 20) / graph_horizontal_data_range

    drawing = generate_y_axis(drawing, request)
    drawing = generate_x_axis(drawing, request)

    for data_point in request.data:
        x_coordinate = (horizontal_scaling * (data_point[0] - starting_point)) + request.configuration.y_axis_size
        y_coordinate = (request.height - request.configuration.x_axis_size + 20) - (vertical_scaling * (data_point[1] - data_min))
        drawing.draw_point(x_coordinate, y_coordinate, label = f"X: {data_point[0]}, Y: {data_point[1]}")

    drawing.close_file()
    return True

def generate_bar_chart(request: RequestBodyOneDimensional):
    drawing = DrawingEngine("example.svg")
    drawing.establish_headers(request.width, request.height + 20)
    drawing.draw_rect(0, 0, request.width, request.height + 20, "white")

    data_max = max(request.data)
    number_of_rects_to_draw = len(request.data)
    available_width = request.width - request.configuration.y_axis_size - 20
    width_per_rect = available_width/number_of_rects_to_draw

    vertical_scaling = (request.height - request.configuration.x_axis_size) / data_max

    generate_y_axis(drawing, request)
    generate_bar_chart_labels(drawing, request)

    # draw the coloured rectangles
    for i, point in enumerate(request.data):
        top_coordinate = request.height - (vertical_scaling * point) - request.configuration.x_axis_size + 20
        drawing.draw_rect(width_per_rect * i + request.configuration.y_axis_size, top_coordinate, width_per_rect, vertical_scaling * point, "gainsboro", stroke="black", title= request.configuration.bar_chart_labels[i])

    drawing.close_file()
    return True

def generate_pie_chart(request: RequestBodyOneDimensional):
    drawing = DrawingEngine("example.svg")
    drawing.establish_headers(request.width, request.height)
    drawing.draw_rect(0, 0, request.width, request.height + 20, "white")
    total_of_data_points = sum(request.data)
    number_of_data_points = len(request.data)

    request.data = sorted(request.data)
    radius = int(min(request.height/2, request.width/2)) - int(request.height/8)
    center_x = request.width/2
    center_y = request.height/2
    drawing.draw_circle(center_x, center_y, radius)
    degrees_per_data_point = 360/total_of_data_points
    current_angle = 270

    space_per_key = (request.width - 80)/(number_of_data_points/2)
    color_sequence = ["cornsilk", "cornflowerblue", "chocolate", "indianred", "lavender", "lightblue"]

    key_x = 40
    key_y = request.height - 20

    for i, data_point in enumerate(request.data):
        slice_angle = degrees_per_data_point * data_point

        # Calculate the endpoint of the first line
        first_line_ex = center_x + radius * math.cos(math.radians(current_angle))
        first_line_ey = center_y + radius * math.sin(math.radians(current_angle))

        # Calculate the endpoint of the second line
        second_angle = current_angle + slice_angle
        second_line_ex = center_x + radius * math.cos(math.radians(second_angle))
        second_line_ey = center_y + radius * math.sin(math.radians(second_angle))

        # Draw arc joining the ends together.
        large_arc_flag = 1 if abs(slice_angle) > 180 else 0
        drawing.draw_pie_slice(center_x, center_y, radius, first_line_ex, first_line_ey, second_line_ex, second_line_ey, large_arc_flag, fill=color_sequence[i%len(color_sequence)])

        # Draw key section with firstly the current colour swatch, and then the text.
        drawing.draw_rect(key_x, key_y, 12, 12, color_sequence[i%len(color_sequence)], stroke="black")
        drawing.draw_text(key_x + 15, key_y + 12, 12, "start", request.configuration.bar_chart_labels[i])
        if i == math.floor(number_of_data_points/2):
            key_x = 40
            key_y -= 20
        else:
            key_x += space_per_key

        # Update the current angle for the next segment
        current_angle += slice_angle

    drawing.close_file()
    return True

def generate_bar_chart_labels(drawing: DrawingEngine, request) -> DrawingEngine:
    drawing.draw_line(request.configuration.y_axis_size, (request.height - request.configuration.x_axis_size) + 20,
                      request.width - 20, (request.height - request.configuration.x_axis_size) + 20, 'black', 'black',
                      'x_axis', False)

    # We need to find the center point of each bar chart entry.
    number_of_rects_to_draw = len(request.data)
    available_width = request.width - request.configuration.y_axis_size - 20
    width_per_rect = available_width/number_of_rects_to_draw

    # Draw in the text labels
    current_x_coordinate = request.configuration.y_axis_size + width_per_rect/2
    for i in range(len(request.data)):
        drawing.draw_text(current_x_coordinate, request.height - request.configuration.x_axis_size + 40, 12, "middle", request.configuration.bar_chart_labels[i])
        current_x_coordinate += width_per_rect

    # Draw in the vertical ticks
    current_x_coordinate = request.configuration.y_axis_size + width_per_rect
    for i in range(len(request.data)):
        # draw a line from x-axis line down to half of the x-axis size
        drawing.draw_line(current_x_coordinate, request.height - request.configuration.x_axis_size + 20, current_x_coordinate, request.height - request.configuration.x_axis_size/2 + 20, "black", "black", "bottom_tick", False)
        current_x_coordinate += width_per_rect

    return drawing

def generate_y_axis(drawing: DrawingEngine, request) -> DrawingEngine:
    # Draw the y-axis
    drawing.draw_line(request.configuration.y_axis_size, request.height - request.configuration.x_axis_size + 20,
                      request.configuration.y_axis_size, 20, 'black', 'black', 'x_axis', False)

    if type(request.data[0]) == list:
        array = np.array(request.data)
        data_min = np.min(array[:, 0])
        data_max = np.max(array[:, 0])
    else:
        data_min = min(request.data)
        data_max = max(request.data)
    graph_value_range = abs(data_max - data_min)

    tick_interval = get_nice_number(graph_value_range / 5)  # Aim for ~5 ticks
    number_of_y_ticks = math.ceil(graph_value_range / tick_interval)

    # Calculate vertical scaling
    vertical_scaling = request.height - request.configuration.x_axis_size - 20 / graph_value_range

    # Compute first tick position
    y_tick_offset = tick_interval * vertical_scaling
    current_y_tick_value = math.ceil(data_min / tick_interval) * tick_interval
    current_y_tick_offset = request.height - request.configuration.x_axis_size - (current_y_tick_value - data_min) * vertical_scaling

    # Draw ticks and labels
    for i in range(number_of_y_ticks + 1):
        position_text = str(round(current_y_tick_value, 2))

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

    # detect if input is 2d
    if type(request.data[0]) == list:
        array = np.array(request.data)
        data_min = np.min(array[:, 0])
        data_max = np.max(array[:, 0])
        graph_value_range = abs(data_max - data_min)
    else:
        graph_value_range = len(request.data)
        data_min = 0

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
        position_text = str(round(((current_x_tick_offset - request.configuration.y_axis_size)/horizontal_scaling) + data_min, 2))

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