import unittest
from unittest.mock import patch, MagicMock

from configuration_body import Configuration
from graph_production import generate_line_graph, generate_scatter_plot, generate_bar_chart, generate_pie_chart, \
    generate_bar_chart_labels
from request_body import RequestBodyOneDimensional, RequestBodyTwoDimensional


class TestDrawingEngine(unittest.TestCase):
    def test_generate_line_graph_calls_expected_methods(self):
        mock_engine = MagicMock()

        config = Configuration(x_axis_size=10, y_axis_size=10, bar_chart_labels = [])

        request = RequestBodyOneDimensional(
            type="any",
            line_name="main_line",
            width=100,
            height=100,
            data=[1, 2, 3],
            configuration=config,
        )

        with patch("graph_production.DrawingEngine", return_value=mock_engine):
            with patch("graph_production.generate_x_axis", return_value=mock_engine):
                with patch("graph_production.generate_y_axis", return_value=mock_engine):
                    result = generate_line_graph(request)

        assert result is True
        assert mock_engine.establish_headers.called
        assert mock_engine.draw_rect.called
        assert mock_engine.draw_line.call_count == 2  # 3 points → 2 lines
        assert mock_engine.close_file.called

    def test_generate_scatter_plot_calls_expected_methods(self):
        mock_engine = MagicMock()

        config = Configuration(x_axis_size=10, y_axis_size=10, bar_chart_labels=[])
        request = RequestBodyTwoDimensional(
            type="scatter",
            line_name="scatter_data",
            width=100,
            height=100,
            data=[[1, 2], [2, 4], [3, 6]],
            configuration=config
        )

        with patch("graph_production.DrawingEngine", return_value=mock_engine):
            with patch("graph_production.generate_x_axis", return_value=mock_engine):
                with patch("graph_production.generate_y_axis", return_value=mock_engine):
                    result = generate_scatter_plot(request)

        assert result is True
        assert mock_engine.establish_headers.called
        assert mock_engine.draw_rect.called
        assert mock_engine.draw_point.call_count == 3  # one per point
        assert mock_engine.close_file.called

    def test_generate_bar_chart_calls_expected_methods(self):
        mock_engine = MagicMock()

        config = Configuration(x_axis_size=10, y_axis_size=10, bar_chart_labels=["A", "B", "C"])
        request = RequestBodyOneDimensional(
            type="bar",
            line_name="bar_data",
            width=120,
            height=100,
            data=[3, 6, 9],
            configuration=config
        )

        with patch("graph_production.DrawingEngine", return_value=mock_engine):
            with patch("graph_production.generate_y_axis", return_value=None):
                with patch("graph_production.generate_bar_chart_labels", return_value=None):
                    result = generate_bar_chart(request)

        assert result is True
        assert mock_engine.establish_headers.called
        assert mock_engine.draw_rect.called
        assert mock_engine.draw_rect.call_count == 4  # 1 background + 3 bars
        assert mock_engine.close_file.called

    def test_generate_pie_chart_calls_expected_methods(self):
        mock_engine = MagicMock()

        config = Configuration(
            x_axis_size=0,
            y_axis_size=0,
            bar_chart_labels=["A", "B", "C"]
        )

        request = RequestBodyOneDimensional(
            type="pie",
            line_name="not_needed",
            width=200,
            height=200,
            data=[3, 6, 9],
            configuration=config
        )

        with patch("graph_production.DrawingEngine", return_value=mock_engine):
            result = generate_pie_chart(request)

        assert result is True

        # Drawing should start with headers and a white background
        assert mock_engine.establish_headers.called
        assert mock_engine.draw_rect.called

        # Central circle of the pie
        assert mock_engine.draw_circle.called

        # Pie slices should be drawn for each data point
        assert mock_engine.draw_pie_slice.call_count == len(request.data)

        # Keys for the pie chart
        assert mock_engine.draw_text.call_count == len(request.data)
        assert mock_engine.draw_rect.call_count >= len(request.data)  # Includes background + color swatches

        # Final SVG closing
        assert mock_engine.close_file.called

    def test_generate_bar_chart_labels_calls_expected_methods(self):
        mock_engine = MagicMock()

        config = Configuration(
            x_axis_size=20,
            y_axis_size=50,
            bar_chart_labels=["Label 1", "Label 2", "Label 3"]
        )

        request = RequestBodyOneDimensional(
            type="bar",
            line_name="not_needed",
            width=300,
            height=200,
            data=[5, 10, 15],
            configuration=config
        )

        with patch("graph_production.DrawingEngine", return_value=mock_engine):
            generate_bar_chart_labels(mock_engine, request)

        assert mock_engine.draw_line.called
        args, kwargs = mock_engine.draw_line.call_args_list[0]
        assert args[0] == config.y_axis_size
        assert args[1] == request.height - config.x_axis_size + 20
        assert args[2] == request.width - 20
        assert args[3] == request.height - config.x_axis_size + 20

        assert mock_engine.draw_text.call_count == len(request.data)
        for i, label in enumerate(request.configuration.labels):
            current_x = config.y_axis_size + ((request.width - config.y_axis_size - 20) / len(request.data)) * (i + 0.5)
            mock_engine.draw_text.assert_any_call(current_x, request.height - config.x_axis_size + 40, 12, "middle",
                                                  label)

        assert mock_engine.draw_line.call_count == 4