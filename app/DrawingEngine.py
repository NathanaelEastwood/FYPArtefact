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

    def draw_arc(self, sx, sy, ex, ey, radius, large_arc_flag=0, sweep_flag=1, stroke="black", fill="none", id=None):
        path_d = f"M {sx} {sy} A {radius} {radius} 0 {large_arc_flag} {sweep_flag} {ex} {ey}"
        with open(self.filename, "a") as f:
            f.write(f'<path d="{path_d}" stroke="black" fill="none" stroke-width="2"/>')

    def draw_pie_slice(self, cx, cy, radius, sx, sy, ex, ey, large_arc_flag=0, fill="gray", stroke="black", stroke_width=1, id=None):
        path_d = f"M {cx} {cy} L {sx} {sy} A {radius} {radius} 0 {large_arc_flag} 1 {ex} {ey} Z"
        with open(self.filename, "a") as f:
            f.write(
                f'<path d="{path_d}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" id="{id if id else ""}"/>\n')

    def draw_rect(self, x: float, y: float, width: float, height: float, fill_colour: str, stroke="none", label = ""):
        with open(self.filename, "a") as f:
            f.write(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{fill_colour}" stroke="{stroke}">\n')
            f.write(f'  <title>{label}</title>\n')
            f.write(f'</rect>')

    def draw_line(self, sx: float, sy: float, ex: float, ey: float, stroke_colour: str, hover_colour: str, line_name: str, has_on_hover: bool, line_width = 1):
        with open(self.filename, "a") as f:

            number_of_distinct_lines = len(self.distinct_lines)
            self.distinct_lines.add(line_name)

            if number_of_distinct_lines < len(self.distinct_lines):
                f.write(f'''<style>.{line_name} {{ stroke: {stroke_colour}; stroke-width: {line_width}; transition: stroke 0.2s, stroke-width 0.2s; }}</style>
                ''')
                if has_on_hover:
                    f.write(f'''<script>
                    window.onload = function() {{
                        document.querySelectorAll(".{line_name}").forEach(line => {{
                            line.addEventListener("mouseenter", function () {{
                                document.querySelectorAll(".{line_name}").forEach(l => {{
                                    l.style.stroke = "{hover_colour}";
                                    l.style.strokeWidth = "4px";
                                }});
                            }});
                            line.addEventListener("mouseleave", function () {{
                                document.querySelectorAll(".{line_name}").forEach(l => {{
                                    l.style.stroke = "{stroke_colour}";
                                    l.style.strokeWidth = "2px";
                                }});
                            }});
                        }});
                    }};
                    </script>''')

            f.write(f'<path class="{line_name}" d="M{sx},{sy} L{ex},{ey}" />\n')

    def draw_text(self, x: float, y: float, font_size: int, anchor_position: str, content: str):
        with open(self.filename, "a") as f:
            f.write(f'<text x="{x}" y="{y}" font-size="{font_size}" text-anchor="{anchor_position}">{content}</text>\n')

    def draw_point(self, x: float, y: float, radius=2, label=""):
        with open(self.filename, "a") as f:
            f.write(f'<circle cx="{x}" cy="{y}" r="{radius}">\n')
            f.write(f'  <title>{label}</title>\n')
            f.write(f'</circle>\n')

    def draw_circle(self, x: float, y: float, radius: int):
        with open(self.filename, "a") as f:
            f.write(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="gainsboro"/>\n')
