from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from _typeshed import SupportsWrite, SupportsRead
from dataclasses import dataclass
from typing import Dict, List, Tuple
import json
import logging
import os


@dataclass
class OrientationPreset:
    name: str
    x: float
    y: float
    z: float

    def as_dict(self) -> Tuple[str, str, str]:
        return str(self.x), str(self.y), str(self.z)


class PositionPresets:
    def __init__(self, preset_file: str = "position_presets.json"):
        self.preset_file = preset_file
        self.tcp_presets: Dict[int, OrientationPreset] = {}
        self.workobj_presets: Dict[int, OrientationPreset] = {}
        self._load_presets()

    def _load_presets(self) -> None:
        if not os.path.exists(self.preset_file):
            self._create_default_presets()

        try:
            with open(self.preset_file, 'r', encoding='utf-8') as file_presets: #type: SupportsRead[str]
                data = json.load(file_presets)

                tcp_data = data.get('tcp_presets', {})
                for key, preset in tcp_data.items():
                    self.tcp_presets[int(key)] = OrientationPreset(**preset)

                workobj_data = data.get('workobj_presets', {})
                for key, preset in workobj_data.items():
                    self.workobj_presets[int(key)] = OrientationPreset(**preset)

                logging.info("Position presets loaded successfully")
        except Exception as e:
            logging.error(f"Error loading position presets: {e}")
            self._create_default_presets()

    def _create_default_presets(self) -> None:
        default_presets = {
            "tcp_presets": {
                "1": {"name": "Rotacia okolo osi X ", "x": 90.0, "y": 0.0, "z": 0.0},
                "2": {"name": "Rotacia okolo osi Y", "x": 0.0, "y": 90.0, "z": 0.0},
                "3": {"name": "Rotacia okolo osi Z", "x": 0.0, "y": 0.0, "z": 90.0}
            },
            "workobj_presets": {
                "1": {"name": "Rotacia okolo osi X", "x": 90.0, "y": 0.0, "z": 0.0},
                "2": {"name": "Rotacia okolo osi Y", "x": 0.0, "y": 90.0, "z": 0.0},
                "3": {"name": "Rotacia okolo osi Z", "x": 0.0, "y": 0.0, "z": 90.0}
            }
        }

        try:
            with open(self.preset_file, 'w', encoding='utf-8') as file_presets: #type: SupportsWrite[str]
                json.dump(default_presets, file_presets, indent=4)
            self._load_presets()
            logging.info("Created default position presets")
        except Exception as e:
            logging.error(f"Error creating default position presets: {e}")

    def get_tcp_preset_names(self) -> List[str]:
        return ["Vlastné nastavenie"] + [preset.name for preset in self.tcp_presets.values()]

    def get_workobj_preset_names(self) -> List[str]:
        return ["Vlastné nastavenie"] + [preset.name for preset in self.workobj_presets.values()]

    def get_tcp_preset(self, index: int) -> OrientationPreset:
        return self.tcp_presets.get(index)

    def get_workobj_preset(self, index: int) -> OrientationPreset:
        return self.workobj_presets.get(index)