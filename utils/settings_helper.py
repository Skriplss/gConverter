import logging
from typing import Union, Tuple
from core.model.setting_object import ParameterType

ERROR_INVALID_NUMBER = "Zadajte platné číslo: '{value}' nemožno prepočítať na číslo"
ERROR_INVALID_NAME = "{param_type} môže obsahovať len písmená, číslice a podčiarkovníky"


def validate_float(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        raise ValueError(ERROR_INVALID_NUMBER.format(value=value))


def validate_name(name: str, param_type: ParameterType) -> str:
    if not name:
        return ParameterType.get_default(param_type)

    cleaned_name = name.strip()
    if not cleaned_name.replace("_", "").isalnum():
        raise ValueError(ERROR_INVALID_NAME.format(param_type=param_type.value))
    return cleaned_name



def format_coordinate(value: Union[Tuple[float, float, float], str, None]) -> Tuple[float, float, float]:
    logging.info("Starting coordinate conversion")
    try:
        if isinstance(value, str):
            parts = [p.strip() for p in value.split(',')]
            if len(parts) != 3:
                raise ValueError(f"Expected 3 values, got {len(parts)}")
            x, y, z = (validate_float(p) for p in parts)
            return x, y, z
        elif isinstance(value, tuple) and len(value) == 3:
            return float(value[0]), float(value[1]), float(value[2])
        return 0.0, 0.0, 0.0
    except ValueError as e:
        logging.warning("Conversion error: %s", e)
        raise