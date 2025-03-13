class DrawingEngine:
    filename: str
    distinct_lines: set[str]

    def __init__(self, filename: str):
        self.filename = filename
        self.distinct_lines = set()

    def establish_headers(self, width: int, height: int):
        with open(self.filename, "w") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><defs></defs>\n')

    def close_file(self):
        with open(self.filename, "a") as f:
            f.write(f'</svg>\n')

    def draw_rect(self, x: float, y: float, width: float, height: float, fill_colour: str):
        with open(self.filename, "a") as f:
            f.write(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{fill_colour}" />\n')

    def draw_line(self, sx: float, sy: float, ex: float, ey: float, stroke_colour: str, hover_colour: str, line_name: str):
        with open(self.filename, "a") as f:

            number_of_distinct_lines = len(self.distinct_lines)
            self.distinct_lines.add(line_name)

            if number_of_distinct_lines < len(self.distinct_lines):
                f.write(f'''
                            <style>
                                .{line_name} {{ stroke: {stroke_colour}; stroke-width: 2; transition: stroke 0.2s, stroke-width 0.2s; }}
                                .{line_name}:hover, .{line_name}:hover ~ .{line_name} {{ stroke: {hover_colour}; stroke-width: 4; }}
                                .hover-zone {{ stroke: transparent; stroke-width: 10; fill: none; pointer-events: stroke; }}
                            </style>
                            ''')

            f.write(f'<path class="hover-zone" d="M{sx},{sy} L{ex},{ey}" />\n')
            f.write(f'<path class="{line_name}" d="M{sx},{sy} L{ex},{ey}" />\n')

    def draw_text(self, x: float, y: float, font_size: int, anchor_position: str, content: str):
        with open(self.filename, "a") as f:
            f.write(f'<text x="{x}" y="{y}" font-size="{font_size}" text-anchor="{anchor_position}">{content}</text>')
