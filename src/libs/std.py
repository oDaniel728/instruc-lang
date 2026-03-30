import re
from typing import TYPE_CHECKING as __TC__
import builtins as __builtins__

if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol

def print(ctx: "RunnerAPIProtocol"):
    cstack = ctx.get_current_stack();
    __builtins__.print(*cstack);
def printf(ctx: "RunnerAPIProtocol"):
    cstack = ctx.get_current_stack();
    __builtins__.print(cstack[0]);

def snap(ctx: "RunnerAPIProtocol"):
    snap = ctx.snapshot();
    __builtins__.print(snap);

def _on_load(ctx: "RunnerAPIProtocol"):
    @ctx.get_syntax_verifications().append
    def _print_kw(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
        line = cl.line;
        if m:=re.match(
            r"^print\s*$",
            line
        ):
            print(ctx);
        return None;
    # @ctx.get_syntax_verifications().append
    # def _say_idk(l, ctx):
    #     __builtins__.print(l);
    #     return None;