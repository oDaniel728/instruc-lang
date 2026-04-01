import re
from typing import TYPE_CHECKING, Any, Callable
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
        c = runnerapi.get_current_line()
        c.index = runnerapi.get_memory("instruc:_line", 0);
        c.codeline = self;
        for v in self.SYNTAXVERIFS:
            r = v(self, runnerapi);
            if r == "SKIP":
                return;

    def adjust(self, runnerapi: "RunnerAPIProtocol"):
        """Apply syntax adjusters that can rewrite line text."""
        for a in runnerapi.get_syntax_adjusters():
            ret = a(self, runnerapi); # type: ignore
            self.line = ret if ret != None else self.line;

    def __str__(self) -> str:
        return self.line;

    def __repr__(self) -> str:
        return self.line;
