import wx
import numpy as np
import logging
import threading
from core.Domain.rapid_converter import RAPIDConverter
from utils.tab_manager import get_tab_manager

from .plot_manager import PlotManager
from .animation_manager import AnimationManager
from .event_handler import EventHandler

class ModelVisualisation(wx.Panel):
    def __init__(self, parent, widget_id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        super(ModelVisualisation, self).__init__(parent, widget_id, pos, size, style)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.plot_manager = PlotManager(self)

        self.rotation_lock = threading.Lock()
        self.draw_lock = threading.Lock()

        self.animation_manager = AnimationManager(self.plot_manager, self.update_lines, self)
        self.rotation_matrix = np.eye(3)
        self.animation_manager.set_rotation_matrix(self.rotation_matrix)
        self.event_handler = EventHandler(self.plot_manager, self.animation_manager, self.rotation_matrix)

        self.x_lim = None
        self.y_lim = None
        self.z_lim = None

        self.visualization_mode = "animated"
        self.file_info_panel = None
        self.filename = None
        self.stop_button = None
        self.visualize_button = None
        self.button_sizer = None
        self.mode_choice = None
        self.file_info_text = None
        self.file_info_label = None
        self.file_info_sizer = None
        self.speed_choice = None
        self.create_ui()

        self.bind_events()

        self.dragging = False
        self.ready_for_visualization = False
        self.last_x = 0
        self.last_y = 0

    def create_ui(self):
        self.file_info_panel = wx.Panel(self, wx.ID_ANY)
        self.file_info_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.file_info_label = wx.StaticText(self.file_info_panel, wx.ID_ANY, "Súbor:")
        self.file_info_text = wx.StaticText(self.file_info_panel, wx.ID_ANY, "Nie je načítané")

        font = self.file_info_text.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        self.file_info_text.SetFont(font)

        self.file_info_sizer.Add(self.file_info_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        self.file_info_sizer.Add(self.file_info_text, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        self.file_info_panel.SetSizer(self.file_info_sizer)

        self.sizer.Add(self.file_info_panel, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)

        mode_panel = wx.Panel(self, wx.ID_ANY)
        mode_sizer = wx.BoxSizer(wx.HORIZONTAL)

        mode_label = wx.StaticText(mode_panel, wx.ID_ANY, "Režim zobrazenia:")
        mode_sizer.Add(mode_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)

        self.mode_choice = wx.Choice(mode_panel, wx.ID_ANY, choices=["Animácia", "Finálny model"])
        self.mode_choice.SetSelection(0)
        mode_sizer.Add(self.mode_choice, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)

        speed_label = wx.StaticText(mode_panel, wx.ID_ANY, "Rýchlosť:")
        mode_sizer.Add(speed_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 15)

        speed_choices = ["x0.5", "x1", "x2", "x5", "x10"]
        self.speed_choice = wx.Choice(mode_panel, wx.ID_ANY, choices=speed_choices)
        self.speed_choice.SetSelection(1)
        mode_sizer.Add(self.speed_choice, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)

        mode_panel.SetSizer(mode_sizer)
        self.sizer.Add(mode_panel, 0, wx.EXPAND | wx.BOTTOM, 5)

        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.visualize_button = wx.Button(self, label="Spustiť vizualizáciu")
        self.stop_button = wx.Button(self, label="Zastaviť vizualizáciu")

        self.button_sizer.Add(self.visualize_button, 1, wx.EXPAND | wx.RIGHT, 2)
        self.button_sizer.Add(self.stop_button, 1, wx.EXPAND | wx.LEFT, 2)

        self.sizer.Add(self.plot_manager.canvas, 1, wx.EXPAND | wx.ALL, 0)
        self.sizer.Add(self.plot_manager.toolbar, 0, wx.EXPAND)
        self.sizer.Add(self.button_sizer, 0, wx.EXPAND | wx.ALL, 2)

        self.SetSizer(self.sizer)

    def bind_events(self):
        self.visualize_button.Bind(wx.EVT_BUTTON, self.on_visualize_button)
        self.stop_button.Bind(wx.EVT_BUTTON, self.on_stop_button)
        self.mode_choice.Bind(wx.EVT_CHOICE, self.on_mode_change)
        self.speed_choice.Bind(wx.EVT_CHOICE, self.on_speed_change)
        self.Bind(wx.EVT_SHOW, self.event_handler.on_show)
        self.Bind(wx.EVT_SIZE, self.event_handler.on_size)

    def set_rapid_text(self, rapid_text):
        self.animation_manager.reset_visualize_state()

        try:
            positions = RAPIDConverter().extract_coordinates_from_rapid(rapid_text)

            if positions.empty:
                logging.warning("No coordinates found in RAPID code")
                wx.MessageBox("V kóde RAPID sa nenašli žiadne súradnice", "Upozornenie", wx.OK | wx.ICON_WARNING)
                return False

            success = self.animation_manager.set_data(positions)
            if not success:
                return False

            self._setup_plot_with_data()
            return True

        except Exception as e:
            logging.error(f"Error when parsing RAPID code: {str(e)}")
            return False

    def _setup_plot_with_data(self):
        self.plot_manager.clear_plot()

        with self.rotation_lock:
            rotated_points = np.dot(self.rotation_matrix, self.animation_manager.start_points)

        if rotated_points.size == 0:
            return False

        self.plot_manager.ax.set_xlim([np.min(rotated_points[0]), np.max(rotated_points[0])])
        self.plot_manager.ax.set_ylim([np.min(rotated_points[1]), np.max(rotated_points[1])])
        self.plot_manager.ax.set_zlim([np.min(rotated_points[2]), np.max(rotated_points[2])])

        self.plot_manager.set_equal_aspect()
        self.plot_manager.update_axis_labels(self.rotation_matrix)

        self.x_lim = self.plot_manager.ax.get_xlim3d()
        self.y_lim = self.plot_manager.ax.get_ylim3d()
        self.z_lim = self.plot_manager.ax.get_zlim3d()

        with self.draw_lock:
            self.plot_manager.canvas.draw()

        self.ready_for_visualization = True

        if self.visualization_mode == "immediate":
            self.visualize_button.Enable(False)
            self.stop_button.Enable(False)
            self.animation_manager.show_immediate_result()
        else:
            self.visualize_button.Enable(True)
            self.stop_button.Enable(True)

        return True

    def update_lines(self):
        with self.rotation_lock:
            rotation_matrix = self.rotation_matrix
        self.animation_manager.update_lines(rotation_matrix)

    @staticmethod
    def update_parent_status(message, progress):
        main_frame = wx.GetApp().GetTopWindow()
        if main_frame:
            wx.CallAfter(main_frame.update_status, message, progress)

    def on_speed_change(self, event):
        self.event_handler.on_speed_change(self.speed_choice, event)

    def on_visualize_button(self, event):
        event.Skip()

        if not self.ready_for_visualization:
            logging.warning("Visualization not ready - RAPID code not set")
            wx.MessageBox("Najprv konvertujte G-kód do RAPID pre vizualizáciu", "Upozornenie", wx.OK | wx.ICON_WARNING)
            return

        if self.animation_manager.start_points is None or len(self.animation_manager.start_points) == 0:
            logging.warning("No data to visualize")
            wx.MessageBox("Dáta pre vizualizáciu nie sú k dispozícii", "Chyba", wx.OK | wx.ICON_ERROR)
            return

        if self.animation_manager.animation_running:
            dlg = wx.MessageDialog(self,
                                 "Vizualizácia práve prebieha. Chcete ju spustiť znova?",
                                 "Prebiehajúca vizualizácia", wx.YES_NO | wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()

            if result == wx.ID_YES:
                self.animation_manager.reset_visualize_state()
            else:
                return

        self.update_parent_status("Vizualizácia...", 0)

        try:
            tab_manager = get_tab_manager()
            tab_manager.block_converter_tab()
        except Exception as e:
            logging.error(f"Chyba pri blokovaní karty konvertora: {str(e)}")

        self.event_handler.on_speed_change(self.speed_choice, None)

        if self.visualization_mode == "immediate":
            self.visualize_button.Enable(False)
            self.stop_button.Enable(False)
            self.animation_manager.show_immediate_result()
        elif self.animation_manager.is_visualize_finished:
            self.show_completion_dialog()
        else:
            self.animation_manager.start_visualize()
            self.stop_button.Enable(True)

    def on_stop_button(self, event):
        event.Skip()
        self.animation_manager.stop_visualize()

        try:
            tab_manager = get_tab_manager()
            tab_manager.unblock_converter_tab()
        except Exception as e:
            logging.error(f"Chyba pri odblokovaní karty konvertora: {str(e)}")

    def show_completion_dialog(self):
        if not self.animation_manager.is_visualize_finished:
            return

        try:
            tab_manager = get_tab_manager()
            tab_manager.unblock_converter_tab()
        except Exception as e:
            logging.error(f"Chyba pri odblokovaní karty konvertora: {str(e)}")

        dlg = wx.MessageDialog(self,
                             "Vizualizácia je dokončená. Chcete ju spustiť znova?",
                             "Dokončenie vizualizácie", wx.YES_NO | wx.ICON_INFORMATION)
        result = dlg.ShowModal()
        dlg.Destroy()

        if result == wx.ID_YES:
            self.animation_manager.reset_visualize_state()
            self.animation_manager.start_visualize()

            try:
                tab_manager = get_tab_manager()
                tab_manager.block_converter_tab()
            except Exception as e:
                logging.error(f"Chyba pri blokovaní karty konvertora: {str(e)}")

    def set_filename(self, filename):
        self.filename = filename
        self.file_info_text.SetLabel(filename)
        self.file_info_panel.Layout()

    def reset_visualize_state(self):
        self.animation_manager.reset_visualize_state()
        self.ready_for_visualization = False

        if self.visualization_mode == "immediate":
            self.visualize_button.Enable(False)
            self.stop_button.Enable(False)
        else:
            self.visualize_button.Enable(True)
            self.stop_button.Enable(True)

    def on_mode_change(self, event):
        self.visualization_mode = self.event_handler.on_mode_change(event, self.mode_choice, self.visualize_button, self.stop_button)

        if not self.ready_for_visualization:
            return

        if self.animation_manager.start_points is not None and len(self.animation_manager.start_points) > 0:
            current_xlim = self.plot_manager.ax.get_xlim3d()
            current_ylim = self.plot_manager.ax.get_ylim3d()
            current_zlim = self.plot_manager.ax.get_zlim3d()

            if self.visualization_mode == "animated":
                self.animation_manager.reset_visualize_state()
                self.ready_for_visualization = True

                if self.x_lim is not None and self.y_lim is not None and self.z_lim is not None:
                    self.plot_manager.ax.set_xlim3d(current_xlim)
                    self.plot_manager.ax.set_ylim3d(current_ylim)
                    self.plot_manager.ax.set_zlim3d(current_zlim)
                    self.plot_manager.canvas.draw()
            else:
                self.animation_manager.show_immediate_result()
                self.x_lim = current_xlim
                self.y_lim = current_ylim
                self.z_lim = current_zlim
        else:
            if self.visualization_mode == "animated":
                pass

        event.Skip()