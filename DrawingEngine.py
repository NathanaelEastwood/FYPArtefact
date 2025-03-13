class DrawingEngine:
    filename: str

    def __init__(self, filename: str):
        self.filename = filename

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

    def draw_line(self, sx: float, sy: float, ex: float, ey: float, stroke_colour: str):
        with open(self.filename, "a") as f:
            f.write(f'<path d="M{sx},{sy} L{ex},{ey}" stroke="{stroke_colour}" />\n')

    def draw_text(self, x: float, y: float, font_size: int, anchor_position: str, content: str):
        with open(self.filename, "a") as f:
            f.write(f'<text x="{x}" y="{y}" font-size="{font_size}" text-anchor="{anchor_position}">{content}</text>')
