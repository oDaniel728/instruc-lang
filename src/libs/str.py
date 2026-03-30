import re
from typing import TYPE_CHECKING as __TC__
import builtins as __builtins__

if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol

__str_kw = "str";

# str
def __str_kw_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    if not line.startswith(__str_kw): return;
    __load(cl, ctx);
    __loadstr(cl, ctx);

__load_kw = "load";
# str load <CHAR>
def __load(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    if (m:=re.match(fr"{__str_kw}\s+{__load_kw}\s+(.)\s*", cl.line)):
        s = m.group(1);
        ctx.get_current_stack().append(s);

__loadstr_kw = "loadstr";
__quote = r"(?<!\\)\""
# str loadstr "STRING"
def __loadstr(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    if (m:=re.match(fr"{__str_kw}\s+{__loadstr_kw}\s+{__quote}(.*){__quote}\s*", cl.line)):
        s = m.group(1);
        ctx.get_current_stack().append(s);

def _on_load(ctx: "RunnerAPIProtocol"):    
    ctx.get_syntax_verifications().append(__str_kw_verif)