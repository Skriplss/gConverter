import logging
from core.Domain.rapid_formatter import RAPIDFormatter


class FileHandler:
    def __init__(self):
        self.formatter = RAPIDFormatter()

    def write_rapid_file(self, rapid_lines: list[str], output_file: str, app_settings) -> None:
        try:
            params = app_settings.get_parameters()
            tcp = app_settings.get_tcp_object()
            workobj = app_settings.get_work_object()
            conversion = app_settings.get_conversion()

            tool_data = self.formatter.format_tool_data(params, tcp)
            workobj_data = self.formatter.format_workobj_data(params, workobj)
            rapid_module = self.formatter.format_module(params, tool_data, workobj_data, rapid_lines, conversion)

            with open(output_file, 'w') as file:
                file.write(rapid_module)
            logging.info(f"RAPID code successfully written to {output_file}")

        except Exception as e:
            logging.error(f"Error writing RAPID file: {e}")
            raise