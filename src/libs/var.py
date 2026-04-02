import re
from typing import TYPE_CHECKING as __TC__;
import builtins as __builtins__;
if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol;

def _on_load(ctx: "RunnerAPIProtocol"):
    __var_kw = "var";
    __var_typ = r"(int|str|float|bool)";
    __var_fmt = fr"^{__var_kw}\s+{__var_typ}\s+(.+)\s+(.+)\s*$";
    __var_get_fmt = fr"^{__var_kw}\s+get\s+(.+)\s*$";
    __var_set_fmt = fr"^{__var_kw}\s+set\s+(.+)\s+(.+)\s*$";
    __var_end_fmt = fr"^{__var_kw}\s+end\s+(.+)\s*$";
    @ctx.add_syntax_verification
    def __var_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
        if not cl.line.startswith(__var_kw):
            return;

        if m:=re.match(__var_fmt, cl.line):
            var_type = m.group(1);
            var_name = m.group(2);
            var_value_str = m.group(3);

            try:
                if var_type == "int":
                    var_value = int(var_value_str);
                elif var_type == "float":
                    var_value = float(var_value_str);
                elif var_type == "bool":
                    if var_value_str.lower() in ("true", "1"):
                        var_value = True;
                    elif var_value_str.lower() in ("false", "0"):
                        var_value = False;
                    else:
                        raise ValueError(f"Invalid boolean value: {var_value_str}");
                else:  # str
                    var_value = var_value_str;
            except ValueError as e:
                return (False, e.__class__, f"Invalid value for type {var_type}: {var_value_str}");

            ctx.overwrite_memory(var_name, var_value);
        elif m:=re.match(__var_get_fmt, cl.line):
            var_name = m.group(1);
            value = ctx.get_memory(var_name, None);
            ctx.get_current_stack().append(value);
            if value is None:
                return (False, NameError, f"Variable '{var_name}' is not defined");
            ctx.overwrite_memory("var:get", value);
        elif m:=re.match(__var_set_fmt, cl.line):
            var_name = m.group(1);
            var_value_str = m.group(2);
            current_value = ctx.get_memory(var_name, None);
            if current_value is None:
                return (False, NameError, f"Variable '{var_name}' is not defined");
            var_type = type(current_value);
            try:
                if var_type == int:
                    var_value = int(var_value_str);
                elif var_type == float:
                    var_value = float(var_value_str);
                elif var_type == bool:
                    if var_value_str.lower() in ("true", "1"):
                        var_value = True;
                    elif var_value_str.lower() in ("false", "0"):
                        var_value = False;
                    else:
                        raise ValueError(f"Invalid boolean value: {var_value_str}");
                else:  # str
                    var_value = var_value_str;
            except ValueError as e:
                return (False, e.__class__, f"Invalid value for type {var_type.__name__}: {var_value_str}");

            ctx.overwrite_memory(var_name, var_value);
        elif m:=re.match(__var_end_fmt, cl.line):
            var_name = m.group(1);
            ctx.get_memory(var_name, None);  # Just to check if it exists
            ctx.overwrite_memory(var_name, None);
        else:
            return (False, SyntaxError, "Invalid var syntax");