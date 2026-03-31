import re
from typing import TYPE_CHECKING as __TC__
import builtins as __builtins__

if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol

def __call_label_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    LABEL = ctx.enum.SyntaxRulePatterns.LABEL_NAME;
    CALL = ctx.enum.SyntaxKeywords.CALL;
    if m:=re.match(
        fr"^{CALL}\s+({LABEL})\s*$",
        line
    ):
        lbl = m.group(1);
        ctx.execute(lbl);
        return "SKIP";

def _on_load(ctx: "RunnerAPIProtocol"):
    ctx.add_syntax_verification(__call_label_verif);
    return None;