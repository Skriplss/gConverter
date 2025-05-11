from dataclasses import dataclass, field
from typing import Dict, Tuple
from enum import Enum
from utils.quaternion_calculator import QuaternionCalculator

@dataclass
class Coordinates:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def as_dict(self) -> Dict[str, float]:
        return {'x': self.x, 'y': self.y, 'z': self.z}

    def as_position(self) -> Tuple[float, float, float]:
        return self.x, self.y, self.z

@dataclass
class EulerAngles:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def as_dict(self) -> Dict[str, float]:
        return {'x': self.x, 'y': self.y, 'z': self.z}

@dataclass
class Orientation:
    euler: EulerAngles = field(default_factory=EulerAngles)
    __quaternion: tuple[float, float, float, float] = 0.0, 0.0, 0.0, 0.0

    def __post_init__(self):
        qx, qy, qz, qw = QuaternionCalculator.euler_to_quaternion(self.euler.x, self.euler.y, self.euler.z)
        self.__quaternion = (qx, qy, qz, qw)

    def as_dict(self) -> Dict[str, float]:
        return self.euler.as_dict()

    def as_quaternion(self) -> tuple[float, float, float, float]:
        return self.__quaternion

@dataclass
class Gobject:
    position: Coordinates = field(default_factory=Coordinates)
    orientation: Orientation = field(default_factory=Orientation)

    def as_dict(self) -> dict[str, dict[str, float]]:
        return {'position': self.position.as_dict(), 'orientation': self.orientation.as_dict()}

    def get_position(self) -> Coordinates:
        return self.position

    def get_orientation(self) -> Orientation:
        return self.orientation

    def get_center_of_gravity(self) -> Coordinates:
        pos = self.get_position()
        return Coordinates(x=pos.x/2, y=pos.y/2, z=pos.z/2)

@dataclass(frozen=True)
class DefaultConfig:
    MODULE_NAME: str = "Module1"
    PROC_NAME: str = "Process"
    TOOL_NAME: str = "Tool"
    WORKOBJ_NAME: str = "POZ"

    @classmethod
    def get_default(cls, param: str) -> str:
        return getattr(cls, param.upper(), "")

class ParameterType(Enum):
    MODULE_NAME = "module_name"
    PROC_NAME = "proc_name"
    TOOL_NAME = "tool_name"
    WORKOBJ_NAME = "workobj_name"

    @classmethod
    def get_default(cls, param_type: 'ParameterType') -> str:
        return DefaultConfig.get_default(param_type.value)

@dataclass
class BaseParameters:
    module_name: str = "Module1"
    proc_name: str = "Process"
    tool_name: str = "Tool"
    workobj_name: str = "POZ"

    def as_dict(self) -> dict[str, str]:
        return {
            ParameterType.MODULE_NAME.value: self.module_name,
            ParameterType.PROC_NAME.value: self.proc_name,
            ParameterType.TOOL_NAME.value: self.tool_name,
            ParameterType.WORKOBJ_NAME.value: self.workobj_name,
        }

@dataclass
class Conversion:
    arm_speed: int = 0
    zone: int = 0

    def as_dict(self) -> dict[str, int]:
        return {
            'arm_speed': self.arm_speed,
            'zone': self.zone
        }

@dataclass
class OrientationPresets:
    tcp_preset: int = 0
    workobj_preset: int = 0

    def as_dict(self) -> dict[str, int]:
        return {
            'tcp_preset': self.tcp_preset,
            'workobj_preset': self.workobj_preset
        }