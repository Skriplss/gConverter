import wx
import numpy as np
import threading
import time
import logging
from utils.tab_manager import get_tab_manager

class AnimationManager:
    def __init__(self, plot_manager, update_callback, parent=None):
        self.plot_manager = plot_manager
        self.update_callback = update_callback
        self.parent = parent

        self.animation_thread = None
        self.animation_running = False
        self.animation_lock = threading.Lock()
        self.current_frame = 0
        self.is_visualize_finished = False

        self.start_points = None
        self.current_points = None
        self.line = None
        self.history_line = None

        self.rotation_matrix = None
        self.animation_interval = 5

    def set_rotation_matrix(self, rotation_matrix):
        self.rotation_matrix = rotation_matrix

    def set_data(self, positions):
        if not positions.empty:
            self.start_points = np.array([positions['x'], positions['y'], positions['z']])
            self.current_points = np.array([[], [], []])
            self.current_frame = 0
            self.is_visualize_finished = False
            return True
        return False

    def start_visualize(self):
        if self.start_points is None:
            logging.warning("No data to visualize")
            return False

        self.stop_visualize()

        if self.line is None:
            self.history_line = self.plot_manager.ax.plot([], [], [], color='#48D1CC', alpha=1, linestyle='-', linewidth=1)[0]
            self.line = self.plot_manager.ax.plot([], [], [], color='red', alpha=1, linestyle='-', linewidth=2)[0]

        remaining_frames = len(self.start_points[0]) - self.current_frame

        if remaining_frames <= 0:
            logging.warning("No frames left to animate")
            self.is_visualize_finished = True
            return False

        self.animation_running = True
        self.animation_thread = threading.Thread(target=self.animation_worker)
        self.animation_thread.daemon = True
        self.animation_thread.start()
        return True

    def show_immediate_result(self):
        if self.start_points is None:
            logging.warning("No data to visualize")
            return False

        if self.line is None:
            self.history_line = self.plot_manager.ax.plot([], [], [], color='#48D1CC', alpha=1, linestyle='-', linewidth=1)[0]
            self.line = self.plot_manager.ax.plot([], [], [], color='red', alpha=1, linestyle='-', linewidth=2)[0]

        self.stop_visualize()

        with self.animation_lock:
            self.current_frame = len(self.start_points[0])
            self.is_visualize_finished = True

            if self.current_frame > 0:
                all_points = np.array([
                    self.start_points[0][:self.current_frame],
                    self.start_points[1][:self.current_frame],
                    self.start_points[2][:self.current_frame]
                ])

                rotated_points = np.dot(self.rotation_matrix, all_points)

                self.history_line.set_data_3d(
                    rotated_points[0],
                    rotated_points[1],
                    rotated_points[2]
                )

                self.line.set_data_3d([], [], [])

                if self.parent and hasattr(self.parent, 'update_parent_status'):
                    wx.CallAfter(self.parent.update_parent_status, "Vizualizácia dokončená", 100)
                try:
                    tab_manager = get_tab_manager()
                    wx.CallAfter(tab_manager.unblock_converter_tab)
                except Exception as e:
                    logging.error(f"Chyba pri odblokovaní karty konvertora: {str(e)}")
                    
                wx.CallAfter(self.plot_manager.canvas.draw)
                return True

        return False

    def animation_worker(self):
        try:
            total_frames = len(self.start_points[0]) if self.start_points is not None else 0

            if self.parent and hasattr(self.parent, 'update_parent_status'):
                self.parent.update_parent_status("Vizualizácia...", 0)

            while self.animation_running:
                with self.animation_lock:
                    if self.current_frame >= total_frames:
                        self.is_visualize_finished = True
                        self.animation_running = False

                        if self.parent and hasattr(self.parent, 'update_parent_status'):
                            wx.CallAfter(self.parent.update_parent_status, "Vizualizácia dokončená", 100)
                        try:
                            tab_manager = get_tab_manager()
                            wx.CallAfter(tab_manager.unblock_converter_tab)
                        except Exception as e:
                            logging.error(f"Chyba pri odblokovaní karty konvertora: {str(e)}")
                            
                        break

                    self.current_frame += 1
                    progress_percent = int((self.current_frame / total_frames) * 100) if total_frames > 0 else 0
                    current_interval = self.animation_interval

                    if self.current_frame % 5 == 0 and self.parent and hasattr(self.parent, 'update_parent_status'):
                        wx.CallAfter(self.parent.update_parent_status, "Vizualizácia...", progress_percent)

                wx.CallAfter(self.update_callback)
                wx.CallAfter(self.plot_manager.canvas.draw_idle)
                time.sleep(current_interval / 1000.0)

        except Exception as e:
            logging.error(f"Error in animation thread: {str(e)}")
            self.animation_running = False
            try:
                tab_manager = get_tab_manager()
                wx.CallAfter(tab_manager.unblock_converter_tab)
            except Exception as ex:
                logging.error(f"Chyba pri odblokovaní karty konvertora: {str(ex)}")

    def update_lines(self, rotation_matrix):
        try:
            with self.animation_lock:
                current_frame = self.current_frame

            if current_frame > 1:
                history_points = np.array([
                    self.start_points[0][:current_frame - 1],
                    self.start_points[1][:current_frame - 1],
                    self.start_points[2][:current_frame - 1]
                ])

                rotated_history = np.dot(rotation_matrix, history_points)

                self.history_line.set_data_3d(
                    rotated_history[0],
                    rotated_history[1],
                    rotated_history[2]
                )

            current_segment = np.array([
                self.start_points[0][max(0, current_frame - 1):current_frame + 1],
                self.start_points[1][max(0, current_frame - 1):current_frame + 1],
                self.start_points[2][max(0, current_frame - 1):current_frame + 1]
            ])

            rotated_current = np.dot(rotation_matrix, current_segment)
            self.line.set_data_3d(
                rotated_current[0],
                rotated_current[1],
                rotated_current[2]
            )

        except Exception as e:
            logging.error(f"Error updating lines: {str(e)}")
            self.stop_visualize()

    def stop_visualize(self):
        self.animation_running = False

        if self.animation_thread and self.animation_thread.is_alive():
            self.animation_thread.join(0.5)

        self.animation_thread = None

    def reset_visualize_state(self):
        self.current_frame = 0
        self.is_visualize_finished = False
        self.current_points = np.array([[], [], []])
        self.stop_visualize()

        if self.parent and hasattr(self.parent, 'update_parent_status'):
            wx.CallAfter(self.parent.update_parent_status, "Pripravené", 0)

        xlim = self.plot_manager.ax.get_xlim3d() if hasattr(self.plot_manager, 'ax') else None
        ylim = self.plot_manager.ax.get_ylim3d() if hasattr(self.plot_manager, 'ax') else None
        zlim = self.plot_manager.ax.get_zlim3d() if hasattr(self.plot_manager, 'ax') else None

        if self.line is not None:
            try:
                self.line.remove()
            except Exception as e:
                logging.error(f"Error removing line: {str(e)}")
            self.line = None

        if self.history_line is not None:
            try:
                self.history_line.remove()
            except Exception as e:
                logging.error(f"Error removing history line: {str(e)}")
            self.history_line = None

        try:
            self.plot_manager.ax.clear()
            self.plot_manager.ax.set_xlabel('X', color=self.plot_manager.x_color, fontweight='bold')
            self.plot_manager.ax.set_ylabel('Y', color=self.plot_manager.y_color, fontweight='bold')
            self.plot_manager.ax.set_zlabel('Z', color=self.plot_manager.z_color, fontweight='bold')

            if None not in (xlim, ylim, zlim):
                self.plot_manager.ax.set_xlim3d(xlim)
                self.plot_manager.ax.set_ylim3d(ylim)
                self.plot_manager.ax.set_zlim3d(zlim)
        except Exception as e:
            logging.error(f"Error resetting plot state: {str(e)}")
        self.plot_manager.canvas.draw()

    def set_animation_interval(self, interval):
        with self.animation_lock:
            self.animation_interval = interval 