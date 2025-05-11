import wx
import math
import numpy as np
from typing import Tuple


class BaseCoordinateVisualizer(wx.Panel):
    AXIS_COLORS = {
        'x': (255, 0, 0),
        'y': (0, 255, 0),
        'z': (0, 0, 255)
    }

    def __init__(self, parent: wx.Window, panel_id: int = wx.ID_ANY):
        super().__init__(parent, panel_id)
        self.SetMinSize((330, 300))
        self.axis_length = 80
        self.center = (165, 150)
        self.orientation = (0, 0, 0)
        self.rotation_matrix = np.eye(3)
        self.Bind(wx.EVT_PAINT, self._on_paint)

    def set_orientation(self, orientation: Tuple[float, float, float]) -> None:
        self.orientation = orientation
        self._calculate_rotation_matrix(orientation)

    def _calculate_rotation_matrix(self, angles: Tuple[float, float, float]) -> None:
        x, y, z = [math.radians(angle) for angle in angles]

        rx = BaseCoordinateVisualizer._rotation_matrix_x(x)
        ry = BaseCoordinateVisualizer._rotation_matrix_y(y)
        rz = BaseCoordinateVisualizer._rotation_matrix_z(z)
        self.rotation_matrix = rx @ ry @ rz
        self.Refresh()

    @staticmethod
    def _rotation_matrix_x(angle: float) -> np.ndarray:
        return np.array([
            [1, 0, 0],
            [0, math.cos(angle), -math.sin(angle)],
            [0, math.sin(angle), math.cos(angle)]
        ])

    @staticmethod
    def _rotation_matrix_y(angle: float) -> np.ndarray:
        return np.array([
            [math.cos(angle), 0, math.sin(angle)],
            [0, 1, 0],
            [-math.sin(angle), 0, math.cos(angle)]
        ])

    @staticmethod
    def _rotation_matrix_z(angle: float) -> np.ndarray:
        return np.array([
            [math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle), 0],
            [0, 0, 1]
        ])

    def rotate_point(self, point: Tuple[float, float, float]) -> Tuple[float, float, float]:
        point_vector = np.array(point).reshape(3, 1)
        rotated = self.rotation_matrix @ point_vector
        return float(rotated[0][0]), float(rotated[1][0]), float(rotated[2][0])

    def project_point(self, point: Tuple[float, float, float]) -> Tuple[int, int]:
        x, y, z = point
        projection_angle = math.pi / 5
        px = x - y * math.cos(projection_angle)
        py = z - y * math.sin(projection_angle)
        return int(self.center[0] + px), int(self.center[1] - py)

    def _draw_axis(self, dc: wx.DC, start: Tuple[float, float, float], end: Tuple[float, float, float], color: Tuple[int, int, int]) -> None:
        start_rotated = self.rotate_point(start)
        end_rotated = self.rotate_point(end)

        start_2d = self.project_point(start_rotated)
        end_2d = self.project_point(end_rotated)

        dc.SetPen(wx.Pen(color, 2))
        dc.DrawLine(*start_2d, *end_2d)

    def _on_paint(self, event: wx.PaintEvent) -> None:
        dc = wx.PaintDC(self)
        dc.Clear()

        origin = (0.0, 0.0, 0.0)
        axis_vectors = {
            'x': (float(self.axis_length), 0.0, 0.0),
            'y': (0.0, float(self.axis_length), 0.0),
            'z': (0.0, 0.0, float(self.axis_length))
        }

        for axis, end_point in axis_vectors.items():
            color = self.AXIS_COLORS[axis]
            self._draw_axis(dc, origin, end_point, color)

            label_offset = 15.0
            label_point = (
                end_point[0] + label_offset * bool(end_point[0]),
                end_point[1] + label_offset * bool(end_point[1]),
                end_point[2] + label_offset * bool(end_point[2])
            )
            dc.SetTextForeground(wx.Colour(*color))
            end_pos = self.project_point(self.rotate_point(label_point))
            dc.DrawText(axis.upper(), *end_pos)

        event.Skip()

class VizualTCP(BaseCoordinateVisualizer):
    pass

class VizualWorkObj(BaseCoordinateVisualizer):
    pass