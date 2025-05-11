from __future__ import annotations

import json
import logging
import os
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from _typeshed import SupportsWrite, SupportsRead
from core.model.app_settings import AppSettings
import threading


class SettingsManager:
    def __init__(self, settings_file: str = "settings.json") -> None:
        self.settings_file = settings_file
        self.settings_lock = threading.Lock()
        self._initialize_settings_file()

    def _initialize_settings_file(self) -> None:
        if not os.path.exists(self.settings_file):
            with self.settings_lock:
                default_settings = AppSettings()
                with open(self.settings_file, 'w', encoding='utf-8') as file_parameters: #type: SupportsWrite[str]
                    json.dump(default_settings.as_dict(), file_parameters)
                logging.error("The settings file is created with basic values")

    def load_all_settings(self) -> AppSettings:
        with self.settings_lock:
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as file_parameters: #type: SupportsRead[str]
                    content = json.load(file_parameters)
                    app_settings = AppSettings()
                    app_settings.from_dict(content)
                    logging.info("Loading settings: successful: %s", app_settings.as_dict())
                    return app_settings
            except FileNotFoundError:
                logging.warning("The settings file does not exist. I create a new one with default values.")
                self._initialize_settings_file()
                return AppSettings()
            except json.JSONDecodeError as e:
                logging.error("JSON format error: %s", e)
                return AppSettings()

    def save_all_settings(self, app_settings: AppSettings) -> None:
        with self.settings_lock:
            try:
                with open(self.settings_file, 'w', encoding='utf-8') as file_parameters: #type: SupportsWrite[str]
                    json.dump(app_settings.as_dict(), file_parameters, indent=4)
                    logging.info("Settings successfully saved %s", app_settings.as_dict())
            except Exception as e:
                logging.error("Saving error: %s", e, exc_info=True)