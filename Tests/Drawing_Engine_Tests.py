import unittest
from unittest.mock import mock_open, patch

from DrawingEngine import DrawingEngine


class TestDrawingEngine(unittest.TestCase):

    def get_written_content(mock_file):
        handle = mock_file()
        return "".join(call.args[0] for call in handle.write.call_args_list)

    def test_establish_headers(self):
        mock_file = mock_open()
        engine = DrawingEngine("dummy.svg")
        width, height = 100, 200

        with patch("builtins.open", mock_file):
            engine.establish_headers(width, height)

        mock_file.assert_called_once_with("dummy.svg", "w")

        handle = mock_file()
        handle.write.assert_any_call('<?xml version="1.0" encoding="UTF-8"?>\n')
        handle.write.assert_any_call(
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{width}" height="{height}" viewBox="0 0 {width} {height}"><defs></defs>\n'
        )

    def test_close_file(self):
        mock_file = mock_open()
        engine = DrawingEngine("dummy.svg")

        with patch("builtins.open", mock_file):
            engine.close_file()

        # Ensure the file was opened in append mode
        mock_file.assert_called_once_with("dummy.svg", "a")

        # Check that the closing tag was written
        handle = mock_file()
        handle.write.assert_called_once_with('</svg>\n')

    def test_draw_arc(self):
        mock_file = mock_open()
        engine = DrawingEngine("dummy.svg")

        with patch("builtins.open", mock_file):
            engine.draw_arc(10, 20, 30, 40, 50)

        expected_path = '<path d="M 10 20 A 50 50 0 0 1 30 40" stroke="black" fill="none" stroke-width="2"/>'
        mock_file.assert_called_once_with("dummy.svg", "a")
        handle = mock_file()
        handle.write.assert_called_once_with(expected_path)

    def test_draw_pie_slice(self):
        mock_file = mock_open()
        engine = DrawingEngine("dummy.svg")

        with patch("builtins.open", mock_file):
            engine.draw_pie_slice(
                cx=100, cy=100,
                radius=50,
                sx=150, sy=100,
                ex=100, ey=150,
                large_arc_flag=0,
                fill="red", stroke="blue", stroke_width=2, id="slice1"
            )

        expected_path = (
            '<path d="M 100 100 L 150 100 A 50 50 0 0 1 100 150 Z" '
            'fill="red" stroke="blue" stroke-width="2" id="slice1"/>\n'
        )
        mock_file.assert_called_once_with("dummy.svg", "a")
        handle = mock_file()
        handle.write.assert_called_once_with(expected_path)

    def test_draw_rect(self):
        mock_file = mock_open()
        engine = DrawingEngine("dummy.svg")

        with patch("builtins.open", mock_file):
            engine.draw_rect(x=10, y=20, width=100, height=50, fill_colour="green", stroke="black")

        expected_rect = '<rect x="10" y="20" width="100" height="50" fill="green" stroke="black"/>\n'
        mock_file.assert_called_once_with("dummy.svg", "a")
        handle = mock_file()
        handle.write.assert_called_once_with(expected_rect)

    def test_draw_line_first_time_with_hover(self):
        mock_file = mock_open()
        engine = DrawingEngine("dummy.svg")

        with patch("builtins.open", mock_file):
            engine.draw_line(
                sx=0, sy=0, ex=100, ey=100,
                stroke_colour="black",
                hover_colour="red",
                line_name="myLine",
                has_on_hover=True,
                line_width=2
            )

        handle = mock_file()
        calls = [call.args[0] for call in handle.write.call_args_list]

        assert any('<style>.myLine {' in c for c in calls)
        assert any('<script>' in c for c in calls)
        assert any('<path class="myLine" d="M0,0 L100,100"' in c for c in calls)

    def test_draw_line_repeated_same_name(self):
        mock_file = mock_open()
        engine = DrawingEngine("dummy.svg")
        engine.distinct_lines.add("myLine")

        with patch("builtins.open", mock_file):
            engine.draw_line(
                sx=10, sy=20, ex=30, ey=40,
                stroke_colour="blue",
                hover_colour="green",
                line_name="myLine",
                has_on_hover=True,
                line_width=2
            )

        handle = mock_file()
        calls = [call.args[0] for call in handle.write.call_args_list]

        assert not any('<style>' in c for c in calls)
        assert not any('<script>' in c for c in calls)
        assert any('<path class="myLine" d="M10,20 L30,40"' in c for c in calls)

    def test_draw_line_no_hover(self):
        mock_file = mock_open()
        engine = DrawingEngine("dummy.svg")

        with patch("builtins.open", mock_file):
            engine.draw_line(
                sx=1, sy=2, ex=3, ey=4,
                stroke_colour="gray",
                hover_colour="yellow",
                line_name="noHoverLine",
                has_on_hover=False,
                line_width=1
            )

        handle = mock_file()
        calls = [call.args[0] for call in handle.write.call_args_list]

        assert any('<style>.noHoverLine {' in c for c in calls)
        assert not any('<script>' in c for c in calls)
        assert any('<path class="noHoverLine" d="M1,2 L3,4"' in c for c in calls)

    def test_draw_text(self):
        mock_file = mock_open()
        engine = DrawingEngine("dummy.svg")

        with patch("builtins.open", mock_file):
            engine.draw_text(
                x=50, y=100,
                font_size=12,
                anchor_position="middle",
                content="Hello, World!"
            )

        expected_text = '<text x="50" y="100" font-size="12" text-anchor="middle">Hello, World!</text>\n'

        handle = mock_file()
        handle.write.assert_called_once_with(expected_text)

    def test_draw_circle(self):
        mock_file = mock_open()
        engine = DrawingEngine("dummy.svg")

        with patch("builtins.open", mock_file):
            engine.draw_circle(
                x=100, y=150,
                radius=10
            )

        expected_output = '<circle cx="100" cy="150" r="10" fill="gainsboro"/>\n'

        handle = mock_file()
        handle.write.assert_called_once_with(expected_output)
