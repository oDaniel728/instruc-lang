import re
from typing import TYPE_CHECKING as __TC__;
import builtins as __builtins__;
import os as __os__;
import subprocess as __subprocess__;
if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol;

__quote = ''
__str = ''
__stack_name = ''
def __os_load_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    global __quote, __str, __stack_name;
    if __quote != '': return;

    if __quote == '':
        __quote = ctx.get_memory("str:__quote", '');

    if __quote == '':
        raise ImportError("os library requires str library, use `req str` in `@load`");

    __stack_name = ctx.enum.SyntaxRulePatterns.STACK_NAME;
    __str = fr"(?:{__quote}([^{__quote}]*){__quote})"

__os_kw = "os";
__os_run_kw = "run";
# os run "<command>"
def __os_run_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    if not cl.line.startswith(__os_kw + " " + __os_run_kw):
        return;
    __os_run_fmt = fr"{__os_kw}\s+{__os_run_kw}\s+{__str}";
    if m:=re.match(__os_run_fmt, cl.line):
        command = m.group(1);
        result = __subprocess__.run(command, shell=True, capture_output=True, text=True);
        print(result);
    else:
        return (False, SyntaxError, f"Invalid syntax for os run, expected `os run <command>`");

__os_get_file_kw = "get";
# os get(f|l|fs) "<path>"
def __os_get_file_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    if not cl.line.startswith(__os_kw + " " + __os_get_file_kw):
        return;
    __os_get_file_fmt = fr"{__os_kw}\s+{__os_get_file_kw}\s*(f|l|(?:fs))\s+{__str}";
    if m:=re.match(__os_get_file_fmt, cl.line):
        cs = ctx.get_current_stack();
        mode = m.group(1);
        path = m.group(2);
        if mode == 'f': # file
            with open(path, 'r') as f:
                content = f.read();
            cs.append(content);
        elif mode == 'l': # lines
            with open(path, 'r') as f:
                content = f.read().split("\n");
            cs.append(content);
        elif mode == 'fs': # file size
            size = __os__.path.getsize(path);
            cs.append(size);
    else:
        return (False, SyntaxError, f"Invalid syntax for os get, expected `os get(f|l|fs) <path>`");

# os newf "<path>" (as <stack_id>|"<content>")
# ctx: os new file path as stack_id|"content"
__os_set_file_kw = "newf";
def __os_set_file_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    if not cl.line.startswith(__os_kw + " " + __os_set_file_kw):
        return;
    __os_set_file_as_stack = fr"^{__os_kw}\s+{__os_set_file_kw}\s+{__str}\s+(?:as\s+({__stack_name}))$";
    __os_set_file_content = fr"^{__os_kw}\s+{__os_set_file_kw}\s+{__str}\s+{__str}$";
    __os_set_file = fr"^{__os_kw}\s+{__os_set_file_kw}\s+{__str}$";

    if m:=re.match(__os_set_file, cl.line):
        path = m.group(1);
        stack = ctx.get_current_stack();
        content = "\n".join(stack);
        with open(path, 'w') as f:
            f.write(content);
    
    elif m:=re.match(__os_set_file_as_stack, cl.line):
        path = m.group(1);
        stack_id = m.group(2);
        stack = ctx.get_stack(stack_id);
        content = "\n".join(stack);
        with open(path, 'w') as f:
            f.write(content);

    elif m:=re.match(__os_set_file_content, cl.line):
        path = m.group(1);
        content = m.group(2);
        with open(path, 'w') as f:
            f.write(content);

    else:
        return (False, SyntaxError, f"Invalid use of newf, only `as <stack_id>` or `<content>` are allowed after path");

# os cd "<path>"
def __os_cd_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    if not cl.line.startswith(__os_kw + " cd"):
        return;
    __os_cd_fmt = fr"{__os_kw}\s+cd\s+{__str}";
    if m:=re.match(__os_cd_fmt, cl.line):
        path = m.group(1);
        try:
            __os__.chdir(path);
        except Exception as e:
            return (False, RuntimeError, f"Failed to change directory: {e}");
    else:
        return (False, SyntaxError, f"Invalid syntax for os cd, expected `os cd <path>`");

def _on_load(ctx: "RunnerAPIProtocol"):
    ctx.add_syntax_verification(__os_load_verif);
    ctx.add_syntax_verification(__os_run_verif);
    ctx.add_syntax_verification(__os_get_file_verif);
    ctx.add_syntax_verification(__os_set_file_verif);
    ctx.add_syntax_verification(__os_cd_verif);