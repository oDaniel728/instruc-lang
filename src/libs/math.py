import re
from typing import TYPE_CHECKING as __TC__
import builtins as __builtins__

if __TC__:
    from ..types import RunnerAPIProtocol

def opsum(ctx: "RunnerAPIProtocol"):
    cstack = ctx.get_current_stack();
    s = sum(v for v in cstack if isinstance(v, (int, float)));
    ctx.get_current_stack().clear();
    ctx.get_current_stack().append(s);

def opsub(ctx: "RunnerAPIProtocol"):
    cstack = ctx.get_current_stack();
    s = 0;
    for v in cstack:
        if isinstance(v, (int, float)):
            s -= v;
    ctx.get_current_stack().clear();
    ctx.get_current_stack().append(s);
    
def opmul(ctx: "RunnerAPIProtocol"):
    cstack = ctx.get_current_stack();
    s = 1;
    for v in cstack:
        if isinstance(v, (int, float)):
            s *= v;
    ctx.get_current_stack().clear();
    ctx.get_current_stack().append(s);

def opdiv(ctx: "RunnerAPIProtocol"):
    cstack = ctx.get_current_stack();
    s = 1;
    for v in cstack:
        if isinstance(v, (int, float)):
            s //= v;
    ctx.get_current_stack().clear();
    ctx.get_current_stack().append(s);

def oppow(ctx: "RunnerAPIProtocol"):
    cstack = ctx.get_current_stack();
    s = 1;
    for v in cstack:
        if isinstance(v, (int, float)):
            s **= v;
    ctx.get_current_stack().clear();
    ctx.get_current_stack().append(s);

def opmod(ctx: "RunnerAPIProtocol"):
    cstack = ctx.get_current_stack();
    s = 1;
    for v in cstack:
        if isinstance(v, (int, float)):
            s %= v;
    ctx.get_current_stack().clear();
    ctx.get_current_stack().append(s);

def _on_load(ctx: "RunnerAPIProtocol"):
    pass