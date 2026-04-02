import re
from typing import TYPE_CHECKING as __TC__
import builtins as __builtins__

if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol

def _comment_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    cl.line = cl.line.strip();
    line = cl.line;
    line = re.sub(r"#.*$", "", line);
    return line;
def _on_load(ctx: "RunnerAPIProtocol"):
    ctx.add_syntax_adjuster(_comment_verif)
    ctx.adjust_code();
    return None;