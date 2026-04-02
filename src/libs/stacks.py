import re
from typing import TYPE_CHECKING as __TC__
import builtins as __builtins__

if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol

__PREFIX = "stack";
__NAMESPACE = "stacks";
__PREXP = fr"{__PREFIX}\s+"

__merge_kw = "merge";

# stack merge <stack1> <stack2> > <stack3>
# stack merge <stack1> <stack2>
def __merge_kw_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    if not line.startswith(__PREFIX): return;
    stack_name = ctx.enum.SyntaxRulePatterns.STACK_NAME;

    if m:=re.match(
        fr"{__PREXP}{__merge_kw}\s+({stack_name})\s+({stack_name})\s*\>\s*({stack_name})", line
    ): # merge <stack1> <stack2> > <stack3>
        s1, s2, s3 = m.group(1), m.group(2), m.group(3);
        ctx.register_stack(s3);
        ctx.overwrite_stack(s3, [*ctx.get_stack(s1), *ctx.get_stack(s2)]);
        # print(f"merged {s1} and {s2} into {s3}");

    elif m:=re.match(
        fr"{__PREXP}{__merge_kw}\s+({stack_name})\s+({stack_name})", line
    ): # merge <stack1> <stack2> [> <stack3>]
        s1, s2 = m.group(1), m.group(2);
        ctx.get_stack(s1).extend(ctx.get_stack(s2));
        # print(f"merged {s2} into {s1}");

    return None;

__load_kw = "load";
# stack load <stack>
def __load_kw_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    if not line.startswith(__PREFIX): return;
    stack_name = ctx.enum.SyntaxRulePatterns.STACK_NAME;

    if m:=re.match(
        fr"{__PREXP}load\s+({stack_name})", line
    ):
        s = m.group(1);
        ctx.get_current_stack().extend(ctx.get_stack(s));
        # print(f"loaded stack {s}");

    return None;

__call_kw = "call";
# stack call <method> as <stack> (> stack)?
def __call_kw_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    if not line.startswith(__PREFIX): return;
    stack_name = ctx.enum.SyntaxRulePatterns.STACK_NAME;
    method_name = ".+";

    if m:=re.match(
        fr"{__PREXP}call\s+({method_name})\s+as\s+({stack_name})\s*(?:\>\s*({stack_name}))?", line
    ):
        # stack call <method> as <stack> (> stack)?
        method_id, s1, s2 = m.group(1), m.group(2), m.group(3);
        method = ctx.get_method(method_id);
        bak = ctx.get_current_stack_name();
        ctx.set_current_stack(s1);
        method(ctx);
        if s2 is not None:
            ctx.get_stack(s2).extend(ctx.get_current_stack());
        ctx.set_current_stack(bak);

    return None;

__run_kw = "run";
# stack run <line> as <stack_id> > <stack_output>
def __run_kw_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    if not line.startswith(__PREFIX): return;
    stack_name = ctx.enum.SyntaxRulePatterns.STACK_NAME;
    if m:=re.match(
        fr"^{__PREXP}{__run_kw}\s+(.+)\s+as\s+({stack_name})\s*(?:\>\s*({stack_name}))?\s*$", line
    ):
        code_line, s1, s2 = m.group(1), m.group(2), m.group(3);
        cl = ctx.CodeLine(code_line);
        bak = ctx.get_current_stack_name();
        ctx.set_current_stack(s1);
        cl.execute(ctx);
        if s2 is not None:
            ctx.get_stack(s2).extend(ctx.get_current_stack());
        ctx.set_current_stack(bak);

    return None;

__loadv_kw = "loadv";
__loadv_literal_kw = "literal";
__loadv_literal_types = r"(int|float|str|bool)";
__loadv_literal_fmt = fr"{__PREXP}{__loadv_kw}\s+{__loadv_literal_kw}\s+{__loadv_literal_types}\s+(.+)";
__quote = ''
# stack load <...values>
def __loadv_kw_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    global __quote; 
    if __quote == '': 
        __quote = ctx.get_memory("str:__quote", '');
    if __quote == '': 
        raise Exception("String quote character not found in memory. Please load the 'str' library before using 'stack load literal'.");
    __str = fr"(?:{__quote}([^{__quote}]*){__quote})"
    line = cl.line;
    if not line.startswith(__PREFIX): return;
    stack_name = ctx.enum.SyntaxRulePatterns.STACK_NAME;

    if m:=re.match(
        exp:=fr"^{__loadv_literal_fmt}$", line
    ):  
        typ, values = str(m.group(1)), str(m.group(2));
        cs = ctx.get_current_stack()
        if typ == "int":
            cs.extend(map(int, re.split(r"\s+", values)));
        elif typ == "float":
            cs.extend(map(float, re.split(r"\s+", values)));
        elif typ == "str":
            strings = [ 
                s 
                for s in re.split(fr"{__str}", values) 
                if not re.match(r"^\s*$", s)!=None 
            ];
            cs.extend(strings);
        elif typ == "bool":
            for v in re.split(r"\s+", values):
                if v.lower() in ("true", "1", "yes"):
                    cs.append(True);
                elif v.lower() in ("false", "0", "no"):
                    cs.append(False);
                else:
                    raise Exception(f"Invalid boolean value: {v}");
        # print(f"loading literal values {values} of type {typ} into current stack");
        # print(f"loaded values {values} into current stack");

    return None;

__expand_kw = "expand";
# stack expand <stack>[:<index>] [into <stack>]
def __expand_kw_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    if not line.startswith(__PREFIX): return;
    stack_opt_index = ctx.enum.SyntaxRulePatterns.STACK_OPT_ITEM_SELECTION
    stack_name = ctx.enum.SyntaxRulePatterns.STACK_NAME
    into = fr"(?:\s+into\s+({stack_name}))";
    __expand_fmt = fr"^{__PREXP}{__expand_kw}\s+{stack_opt_index}{into}?$";
    if m:=re.match(__expand_fmt, line):
        stack_id, index, into_stack = m.group(1), m.group(2), m.group(3);
        stack = ctx.get_stack(stack_id);
        if index is not None:
            i = ctx.get_stack_item(stack_id, index);
            if isinstance(i, list):
                items = i;
            else:
                items = [i];
        else:
            items = stack[-1];
        if into_stack is not None:
            ctx.get_stack(into_stack).extend(items);
        else:
            ctx.get_current_stack().extend(items);
        # print(f"expanded stack {s} at index {i} into {'current stack' if into_stack is None else 'stack ' + into_stack}");

def _on_load(ctx: "RunnerAPIProtocol"):    
    ctx.register_memory(f"{__NAMESPACE}:merge_keyword", __merge_kw);
    ctx.register_memory(f"{__NAMESPACE}:load_keyword", __load_kw);
    ctx.register_memory(f"{__NAMESPACE}:call_keyword", __call_kw);
    ctx.register_memory(f"{__NAMESPACE}:run_keyword", __run_kw);
    ctx.register_memory(f"{__NAMESPACE}:loadv_keyword", __loadv_kw);
    ctx.register_memory(f"{__NAMESPACE}:loadv_literal_keyword", __loadv_literal_kw);

    ctx.add_syntax_verification(__merge_kw_verif);
    ctx.add_syntax_verification(__load_kw_verif);
    ctx.add_syntax_verification(__loadv_kw_verif);
    ctx.add_syntax_verification(__call_kw_verif);
    ctx.add_syntax_verification(__run_kw_verif);
    ctx.add_syntax_verification(__expand_kw_verif);