import numpy as np
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar

class PlotManager:
    def __init__(self, parent):
        self.figure = Figure()
        self.canvas = FigureCanvas(parent, -1, self.figure)
        self.ax = self.figure.add_subplot(projection='3d')
        self.toolbar = NavigationToolbar(self.canvas, parent)
        
        self.x_color = 'red'
        self.y_color = 'green'
        self.z_color = 'blue'
        
        self.original_x_dir = np.array([1, 0, 0])
        self.original_y_dir = np.array([0, 1, 0])
        self.original_z_dir = np.array([0, 0, 1])
        
        self.init_plot()
    
    def init_plot(self):
        self.ax.clear()
        self.ax.set_xlabel('X', color=self.x_color, fontweight='bold')
        self.ax.set_ylabel('Y', color=self.y_color, fontweight='bold')
        self.ax.set_zlabel('Z', color=self.z_color, fontweight='bold')
        
        self.canvas.draw()
    
    def update_axis_labels(self, rotation_matrix):
        rotated_x = np.dot(rotation_matrix, self.original_x_dir)
        rotated_y = np.dot(rotation_matrix, self.original_y_dir)
        rotated_z = np.dot(rotation_matrix, self.original_z_dir)
        
        x_proj = [abs(np.dot(rotated_x, [1, 0, 0])), 
                 abs(np.dot(rotated_y, [1, 0, 0])), 
                 abs(np.dot(rotated_z, [1, 0, 0]))]
        x_label = ['X', 'Y', 'Z'][np.argmax(x_proj)]
        x_color = [self.x_color, self.y_color, self.z_color][np.argmax(x_proj)]
        
        y_proj = [abs(np.dot(rotated_x, [0, 1, 0])), 
                 abs(np.dot(rotated_y, [0, 1, 0])), 
                 abs(np.dot(rotated_z, [0, 1, 0]))]
        y_label = ['X', 'Y', 'Z'][np.argmax(y_proj)]
        y_color = [self.x_color, self.y_color, self.z_color][np.argmax(y_proj)]
        
        z_proj = [abs(np.dot(rotated_x, [0, 0, 1])), 
                 abs(np.dot(rotated_y, [0, 0, 1])), 
                 abs(np.dot(rotated_z, [0, 0, 1]))]
        z_label = ['X', 'Y', 'Z'][np.argmax(z_proj)]
        z_color = [self.x_color, self.y_color, self.z_color][np.argmax(z_proj)]
        
        self.ax.set_xlabel(x_label, color=x_color, fontweight='bold')
        self.ax.set_ylabel(y_label, color=y_color, fontweight='bold')
        self.ax.set_zlabel(z_label, color=z_color, fontweight='bold')
    
    def set_equal_aspect(self):
        x_limits = self.ax.get_xlim3d()
        y_limits = self.ax.get_ylim3d()
        z_limits = self.ax.get_zlim3d()

        x_range = abs(x_limits[1] - x_limits[0])
        y_range = abs(y_limits[1] - y_limits[0])
        z_range = abs(z_limits[1] - z_limits[0])

        max_range = max(x_range, y_range, z_range)

        x_middle = (x_limits[1] + x_limits[0]) / 2
        y_middle = (y_limits[1] + y_limits[0]) / 2
        z_middle = (z_limits[1] + z_limits[0]) / 2

        self.ax.set_xlim3d([x_middle - max_range/2, x_middle + max_range/2])
        self.ax.set_ylim3d([y_middle - max_range/2, y_middle + max_range/2])
        self.ax.set_zlim3d([z_middle - max_range/2, z_middle + max_range/2])
    
    def clear_plot(self):
        self.ax.clear()
        self.update_axis_labels(np.eye(3))
        self.canvas.draw() 