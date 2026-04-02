import re
from typing import TYPE_CHECKING as __TC__;
import builtins as __builtins__

from src.codeline import CodeLine;
if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol;

# for <command>
def _on_load(ctx: "RunnerAPIProtocol"):
    __method_name = ctx.enum.SyntaxRulePatterns.METHOD_NAME;
    __label_name = ctx.enum.SyntaxRulePatterns.LABEL_NAME;
  
    __for_kw = "foreach";
    __for_fmt = fr"^{__for_kw}\s+(.+)$";
    @ctx.add_syntax_verification
    def __for_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
        if not cl.line.startswith(__for_kw):
            return;
        if m:=re.match(__for_fmt, cl.line):
            cmd = m.group(1);
            _cl = CodeLine(cmd);
        
            for index, item in enumerate(ctx.get_current_stack()):
                ctx.overwrite_memory("for:item", item);
                ctx.overwrite_memory("for:index", index);
                _cl.execute(ctx);

        return;
