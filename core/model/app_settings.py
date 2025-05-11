import logging
from typing import Union, Tuple, Dict, Any
from core.model.setting_object import Gobject, BaseParameters, ParameterType, Coordinates, Orientation, Conversion, EulerAngles, OrientationPresets
from utils.settings_helper import validate_name, format_coordinate

class AppSettings:
    def __init__(self):
        self.__tcp_object = Gobject()
        self.__work_object = Gobject()
        self.__parameters = BaseParameters()
        self.__conversion = Conversion()
        self.__orientation_presets = OrientationPresets()

    def from_dict(self, data: dict) -> None:
        parameters_data = data.get("parameters", {})
        if not parameters_data:
            logging.warning("Missing parameters: the 'parameters' section is empty or missing.")
        else:
            if ParameterType.MODULE_NAME.value in parameters_data.keys():
                self.set_module_name(parameters_data[ParameterType.MODULE_NAME.value])
            if ParameterType.PROC_NAME.value in parameters_data.keys():
                self.set_proc_name(parameters_data[ParameterType.PROC_NAME.value])
            if ParameterType.TOOL_NAME.value in parameters_data.keys():
                self.set_tool_name(parameters_data[ParameterType.TOOL_NAME.value])
            if ParameterType.WORKOBJ_NAME.value in parameters_data.keys():
                self.set_workobj_name(parameters_data[ParameterType.WORKOBJ_NAME.value])

        tcp_data = data.get("tcp_object", {})
        if not tcp_data:
            logging.warning("Missing TCP data: The 'tcp_object' section is empty or missing.")
        else:
            if "position" in tcp_data.keys():
                self.__tcp_object.position = Coordinates(**tcp_data["position"])
            if "orientation" in tcp_data.keys():
                euler = EulerAngles(**tcp_data["orientation"])
                self.__tcp_object.orientation = Orientation(euler=euler)

        work_data = data.get("work_object", {})
        if not work_data:
            logging.warning("Missing work data: The 'work_object' section is empty or missing.")
        else:
            if "position" in work_data.keys():
                self.__work_object.position = Coordinates(**work_data["position"])
            if "orientation" in work_data.keys():
                euler = EulerAngles(**work_data["orientation"])
                self.__work_object.orientation = Orientation(euler=euler)

        conversion_data = data.get("conversion", {})
        if not conversion_data:
            logging.warning("Missing conversion data: The 'conversion' section is empty or missing.")
        else:
            if "arm_speed" in conversion_data.keys():
                self.__conversion.arm_speed = conversion_data["arm_speed"]
            if "zone" in conversion_data.keys():
                self.__conversion.zone = conversion_data["zone"]

        orientation_presets_data = data.get("orientation_presets", {})
        if not orientation_presets_data:
            logging.warning("Missing presets data: The 'orientation_presets_data' section is empty or missing.")
        else:
            if "tcp_preset" in orientation_presets_data.keys():
                self.__orientation_presets.tcp_preset = orientation_presets_data.get("tcp_preset")
            if "workobj_preset" in orientation_presets_data.keys():
                self.__orientation_presets.workobj_preset = orientation_presets_data.get("workobj_preset")



    def as_dict(self) -> Dict[str, Any]:
        return {
            "parameters": self.__parameters.as_dict(),
            "tcp_object": self.__tcp_object.as_dict(),
            "work_object": self.__work_object.as_dict(),
            "conversion": self.__conversion.as_dict(),
            "orientation_presets": self.__orientation_presets.as_dict()
        }

    def get_orientation_presets(self) -> OrientationPresets:
        return self.__orientation_presets

    def get_conversion(self) -> Conversion:
        return self.__conversion

    def get_parameters(self) -> BaseParameters:
        return self.__parameters

    def get_tcp_object(self) -> Gobject:
        return self.__tcp_object

    def get_work_object(self) -> Gobject:
        return self.__work_object

    def set_speed_arm(self, arm_speed: int) -> None:
        self.__conversion.arm_speed = arm_speed

    def set_zone(self, zone: int) -> None:
        self.__conversion.zone = zone

    def set_orientation_presets(self, tcp_preset: int, workobj_preset: int) -> None:
        self.__orientation_presets.tcp_preset = tcp_preset
        self.__orientation_presets.workobj_preset = workobj_preset

    def set_tcp_position(self, value: Union[str, Tuple]) -> None:
        x, y, z = format_coordinate(value)
        self.__tcp_object.position = Coordinates(x, y, z)

    def set_tcp_orientation(self, value: Union[str, Tuple]) -> None:
        x, y, z = format_coordinate(value)
        euler = EulerAngles(x=x, y=y, z=z)
        self.__tcp_object.orientation = Orientation(euler=euler)

    def set_workobj_position(self, value: Union[str, Tuple]) -> None:
        x, y, z = format_coordinate(value)
        self.__work_object.position = Coordinates(x, y, z)

    def set_workobj_orientation(self, value: Union[str, Tuple]) -> None:
        x, y, z = format_coordinate(value)
        euler = EulerAngles(x=x, y=y, z=z)
        self.__work_object.orientation = Orientation(euler=euler)

    def set_module_name(self, module_name: str) -> None:
        try:
            validated_name = validate_name(module_name, ParameterType.MODULE_NAME)
            self.__parameters.module_name = validated_name
        except ValueError:
            pass

    def set_proc_name(self, proc_name: str) -> None:
        try:
            validated_name = validate_name(proc_name, ParameterType.PROC_NAME)
            self.__parameters.proc_name = validated_name
        except ValueError:
            pass

    def set_tool_name(self, tool_name: str) -> None:
        try:
            validated_name = validate_name(tool_name, ParameterType.TOOL_NAME)
            self.__parameters.tool_name = validated_name
        except ValueError:
            pass

    def set_workobj_name(self, workobj_name: str) -> None:
        try:
            validated_name = validate_name(workobj_name, ParameterType.WORKOBJ_NAME)
            self.__parameters.workobj_name = validated_name
        except ValueError:
            pass