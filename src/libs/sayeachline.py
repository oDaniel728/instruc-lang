import re
from typing import TYPE_CHECKING as __TC__
import builtins as __builtins__

if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol
def _on_load(ctx: "RunnerAPIProtocol"):    
    @ctx.get_syntax_verifications().append
    def _say_each_line_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
        __builtins__.print(cl.line);
        return None;