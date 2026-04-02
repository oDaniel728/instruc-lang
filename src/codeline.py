import re
from typing import TYPE_CHECKING, Any, Callable, Optional, Type
from typing_extensions import Literal
if TYPE_CHECKING:
    from .types import RunnerAPIProtocol
from . import enum


class CodeLine():
    """Represents and executes a single Instruc line."""
    SYNTAXVERIFS = list[Callable[["CodeLine", "RunnerAPIProtocol"], Any]]();
    def __init__(self, line: str) -> None:
        self.line = line.strip();
    
    def execute(self, runnerapi: "RunnerAPIProtocol"):
        """Run registered syntax verifications for this line."""
        if (self.line == ''): return;
        if (runnerapi.is_silent()): return;
    
        c = runnerapi.get_current_line()
        c.index = runnerapi.get_memory("instruc:_line", 0);
        c.codeline = self;
        for v in self.SYNTAXVERIFS:
            r = v(self, runnerapi);
            if r == "SKIP":
                return;
            # r = (False, [<exc>,] <message>)
            elif isinstance(r, tuple) and len(r) >= 2 and r[0] == False:
                if len(r) == 2:
                    raise SyntaxError(f"Syntax error at line {runnerapi.get_memory('instruc:_line', 0)}: {self.line}");
                elif len(r) == 3:
                    f: Literal[False]
                    e: Type[Exception]
                    m: Optional[str]
                    f, e, m = r;
                    raise e(f"Syntax error at line {runnerapi.get_memory('instruc:_line', 0)}: {self.line}\n{m}");

    def adjust(self, runnerapi: "RunnerAPIProtocol"):
        """Apply syntax adjusters that can rewrite line text."""
        if (runnerapi.is_silent()): return;
        for a in runnerapi.get_syntax_adjusters():
            ret = a(self, runnerapi); # type: ignore
            self.line = ret if ret != None else self.line;

    def __str__(self) -> str:
        return self.line;

    def __repr__(self) -> str:
        return self.line;
