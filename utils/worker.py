import threading
from typing import Callable
from core.Domain.rapid_converter import RAPIDConverter
from core.model.app_settings import AppSettings


def convert_async(gcode_text: str, settings: AppSettings, callback: Callable):
    def worker():
        try:
            converter = RAPIDConverter()
            rapid_code = converter.gcode_to_rapid(gcode_text, settings)
            callback(rapid_code)
        except Exception as e:
            callback(f"Error during conversion: {e}")

    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()
