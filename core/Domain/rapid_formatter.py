from core.model.setting_object import BaseParameters, Gobject, Conversion


class RAPIDFormatter:
    @staticmethod
    def format_tool_data(params: BaseParameters, tcp: Gobject) -> str:
        x, y, z = tcp.position.as_position()
        qx, qy, qz, qw = tcp.orientation.as_quaternion()
        cog_x, cog_y, cog_z = tcp.get_center_of_gravity().as_position()
        return f"PERS tooldata {params.tool_name}:=[TRUE,[[{x},{y},{z}],[{qw},{qx},{qy},{qz}]],[1,[{cog_x},{cog_y},{cog_z}],[1,0,0,0],0,0,0]];"

    @staticmethod
    def format_workobj_data(params: BaseParameters, workobj: Gobject) -> str:
        x, y, z = workobj.position.as_position()
        qx, qy, qz, qw = workobj.orientation.as_quaternion()
        return f"TASK PERS wobjdata {params.workobj_name}:=[FALSE,TRUE,\"\",[[{x},{y},{z}],[{qw},{qx},{qy},{qz}]],[[0,0,0],[1,0,0,0]]];"

    @staticmethod
    def format_module(params: BaseParameters, tool_data: str, workobj_data: str, rapid_lines: list[str], conversion: Conversion) -> str:
        new_line = '\n'
        return f"""MODULE {params.module_name}
        {tool_data}

        {workobj_data}
        PROC main()
            {params.proc_name};
        ENDPROC

        PROC {params.proc_name}()
            MoveAbsJ [[0,8.5,24.5,0,57,0],[9E+09,9E+09,9E+09,9E+09,9E+09,9E+09]],v{conversion.arm_speed},z{conversion.zone},tool0\\Wobj:={params.workobj_name};
    {"".join(f'        {line}{new_line}' for line in rapid_lines)}    
        ENDPROC
    ENDMODULE"""