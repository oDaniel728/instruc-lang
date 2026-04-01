# BIBLIOTECA IREQ DE EXEMPLO

import re
from typing import TYPE_CHECKING as __TC__;
import builtins as __builtins__;
if __TC__:
    from src.types import RunnerAPIProtocol, CodeLineProtocol;

def _on_load(ctx: "RunnerAPIProtocol"):
    __yo_kw = "yo";
    __yo_format = fr"^{__yo_kw}\s*$";
    @ctx.add_syntax_verification
    def __yo_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
        if m:=re.match(
            __yo_format,
            cl.line
        ):
            print("Yo!");