import re
from typing import TYPE_CHECKING, Any, Callable
if TYPE_CHECKING:
    from .types import RunnerAPIProtocol
from . import enum


class CodeLine():
    SYNTAXVERIFS = list[Callable[["CodeLine", "RunnerAPIProtocol"], Any]]();
    def __init__(self, line: str) -> None:
        self.line = line.strip();
    
    def execute(self, runnerapi: "RunnerAPIProtocol"):
        if (self.line == ''): return;
        for v in self.SYNTAXVERIFS:
            r = v(self, runnerapi);
            if r == "SKIP":
                return;

    def adjust(self, runnerapi: "RunnerAPIProtocol"):
        for a in runnerapi.get_syntax_adjusters():
            ret = a(self, runnerapi);
            self.line = ret if ret != None else self.line;

    def __str__(self) -> str:
        return self.line;

    def __repr__(self) -> str:
        return self.line;

@CodeLine.SYNTAXVERIFS.append
def __stack_controls__(cl: CodeLine, runnerapi: "RunnerAPIProtocol"):
    line = cl.line;
    if m:=re.match(
        enum
            .SyntaxRegularExpressionPatterns
            .DEFINE_STACK,
        line
    ):
        runnerapi.register_stack(m.group(1));
    elif m:=re.match(
        enum
            .SyntaxRegularExpressionPatterns
            .USE_STACK,
        line
    ):
        runnerapi.register_stack(m.group(1));
        runnerapi.set_current_stack(m.group(1));
    elif m:=re.match(
        enum
            .SyntaxRegularExpressionPatterns
            .END_STACK,
        line
    ):
        if m.group(1) == "*" or m.group(1) == runnerapi.get_current_stack():
            runnerapi.set_current_stack("");
        if m.group(1) == "*":
            for s in runnerapi.get_stack(m.group(1)):
                runnerapi.overwrite_stack(s, []);
        else:
            runnerapi.register_stack(m.group(1));
    elif m:=re.match(
        enum
            .SyntaxRegularExpressionPatterns
            .RETURN,
        line
    ):
        return m.group(1);

@CodeLine.SYNTAXVERIFS.append
def __stack_operators__(cl: CodeLine, runnerapi: "RunnerAPIProtocol"):
    line = cl.line;
    cstack = runnerapi.get_current_stack();
    if m:=re.match(
        enum
            .SyntaxRegularExpressionPatterns
            .LOAD,
        line
    ):
        cstack.append(int(m.group(1)));
    elif m:=re.match(
        enum
            .SyntaxRegularExpressionPatterns
            .KILL,
        line
    ):
        cstack.remove(int(m.group(1)));

@CodeLine.SYNTAXVERIFS.append
def __requirements__(cl: CodeLine, runnerapi: "RunnerAPIProtocol"):
    line = cl.line;
    if m:=re.match(
        enum
            .SyntaxRegularExpressionPatterns
            .REQUIREMENT,
        line
    ):
        runnerapi.require(m.group(1));

@CodeLine.SYNTAXVERIFS.append
def __methods__(cl: CodeLine, runnerapi: "RunnerAPIProtocol"):
    line = cl.line;
    if m:=re.match(
        enum
            .SyntaxRegularExpressionPatterns
            .CALL,
        line
    ):
        if m2:=re.match(
            enum
                .SyntaxRegularExpressionPatterns
                .LIBFORMAT,
            m.group(1)
        ):
            lib, method = m2.groups();
            if lib not in runnerapi.get_libs():
                raise Exception(f"Lib '{lib}' not found");
            if method not in runnerapi.get_lib(lib):
                raise Exception(f"Method '{method}' not found in lib '{lib}'");
            m = runnerapi.get_lib(lib)[method];
            m(runnerapi);