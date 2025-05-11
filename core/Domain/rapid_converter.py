import pandas as pd
from core.model.app_settings import AppSettings
import logging
import re

class RAPIDConverter:
    def __init__(self):
        self.positions = pd.DataFrame([[0.0, 0.0, -10.0]], columns=["x", "y", "z"])
        self.robtargets = []
        self.moveLs = []
        self.current_z = 0.0
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_f = None


    def translate_gcode_to_rapid(self, gcode_cmd, params, settings: AppSettings):
        tool_name = settings.get_parameters().tool_name
        workobj_name = settings.get_parameters().workobj_name
        conversion = settings.get_conversion()

        qx, qy, qz, qw = settings.get_work_object().orientation.as_quaternion()

        if not isinstance(gcode_cmd, list):
            gcode_cmd = [gcode_cmd]

        if 'Z' in params:
            self.current_z = params['Z']
        if 'X' in params:
            self.current_x = params['X']
        if 'Y' in params:
            self.current_y = params['Y']

        if any(cmd in ["G0", "G1", "G00", "G01"] for cmd in gcode_cmd):
            x = params.get('X', self.current_x)
            y = params.get('Y', self.current_y)
            z = params.get('Z', self.current_z)
            if conversion.arm_speed == 0:
                speed = int(self.current_f)
            else:
                speed = conversion.arm_speed

            robtarget = f"[[{x},{y},{z}],[{qw},{qx},{qy},{qz}],[0,0,0,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]]"
            return f"MoveL {robtarget},v{speed},z{conversion.zone},{tool_name}\\WObj:={workobj_name};"

        return ""

    def gcode_to_rapid(self, gcode_text: str, settings: AppSettings) -> str:
        rapid_lines = []
        self.current_f = None

        for line in gcode_text.splitlines():
            if line.startswith(';') or not line.strip():
                continue
            command = line.split(';')[0].strip()
            if not command:
                continue
            parts = command.split()
            if not parts:
                continue

            gcode_cmd = parts[0]
            params = {}
            for part in parts[1:]:
                if len(part) > 1 and part[0].isalpha():
                    try:
                        params[part[0]] = float(part[1:])
                        if part[0] == 'F':
                            self.current_f = float(part[1:])
                    except ValueError:
                        logging.info(f"Ignoring non-numeric value in line: '{line}'")
                        continue

            if gcode_cmd in ["G0", "G1", "G00", "G01"]:
                rapid_cmd = self.translate_gcode_to_rapid(gcode_cmd, params, settings)
                if rapid_cmd:
                    rapid_lines.append(rapid_cmd)

                x = params.get('X', self.current_x)
                y = params.get('Y', self.current_y)
                z = params.get('Z', self.current_z)
                self.positions = pd.concat([self.positions, pd.DataFrame([[x, y, z]], columns=["x", "y", "z"])],
                                           ignore_index=True)

        return "\n".join(rapid_lines)

    def get_positions(self):
        return self.positions

    def extract_coordinates_from_rapid(self, rapid_code):
        positions_list = []
        pattern = r"\[\[([-+]?\d*\.\d+|\d+),([-+]?\d*\.\d+|\d+),([-+]?\d*\.\d+|\d+)\]"

        for line in rapid_code.strip().split('\n'):
            match = re.search(pattern, line)
            if match:
                try:
                    x = float(match.group(1))
                    y = float(match.group(2))
                    z = float(match.group(3))
                    positions_list.append([x, y, z])
                except (ValueError, IndexError) as e:
                    logging.error(f"Error extracting coordinates from RAPID: {line}, Error: {str(e)}")

        if positions_list:
            return pd.DataFrame(positions_list, columns=["x", "y", "z"])
        else:
            return pd.DataFrame(columns=["x", "y", "z"])


