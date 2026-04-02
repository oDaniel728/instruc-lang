from pathlib import Path
import re
from typing import Any, Callable, Protocol, TYPE_CHECKING, Type
type Unknown = Any
from . import enum
if TYPE_CHECKING:
    from .codeline import CodeLine

type SyntaxVerification = Callable[["CodeLine", "RunnerAPIProtocol"], Any]
type SyntaxAdjuster = Callable[["CodeLine", "RunnerAPIProtocol"], Any]

class CodeLineProtocol(Protocol):
    line: str;
    def execute(self, runnerapi: "RunnerAPIProtocol"): ...;
    def __str__(self) -> str: ...;
    def __repr__(self) -> str: ...;
class RunnerLineContextProtocol(Protocol):
    @property
    def index(self) -> int: ...;
    @index.setter
    def index(self, value: int): ...;

    @property
    def codeline(self) -> CodeLineProtocol: ...;
    @codeline.setter
    def codeline(self, value: CodeLineProtocol): ...;
class RunnerAPIProtocol(Protocol):
    def get_stack(self, name: str) -> list[Any]: ...;
    def get_stack_item(self, stack_name: str, index: str) -> Any: ...;
    def get_label(self, name: str) -> list[CodeLine]: ...;
    def get_memory[T](self, name: str, default: T) -> T: ...;

    def register_stack(self, name: str): ...;
    def register_label(self, name: str): ...;
    def register_memory(self, name: str, default: Any): ...;

    def overwrite_stack(self, name: str, value: list[Any]): ...;
    def overwrite_label(self, name: str, value: list[CodeLine]): ...;
    def overwrite_memory(self, name: str, value: Any): ...;

    def get_current_stack(self) -> list[Any]: ...;
    def get_current_stack_name(self) -> str: ...;
    def set_current_stack(self, name: str): ...;

    def require(self, name: str): ...;
    def require_file(self, path: str | Path): ...;

    def get_libs(self) -> dict[str, dict[str, Any]]: ...;
    def get_lib(self, name: str) -> dict[str, Any]: ...;

    def get_syntax_verifications(self) -> list[SyntaxVerification]: ...;
    def add_syntax_verification(self, func: SyntaxVerification): ...;
    def overwrite_syntax_verification(self, name: str , func: SyntaxVerification): ...;

    def get_syntax_adjusters(self) -> list[SyntaxAdjuster]: ...;
    def add_syntax_adjuster(self, func: SyntaxAdjuster): ...;

    def inject_code(self, lines: list[str | CodeLine], label: str = "@main"): ...;

    enum = enum;

    def snapshot(self) -> Unknown: ...;

    def get_method(self, id: str) -> Callable[["RunnerAPIProtocol"], None]: ...;

    def explode_stack(self, name: str): ...;
    def explode_code(self, expression: str): ...;
    
    def replace_code(self, expression: str, repl: Callable[[re.Match], str] | str): ...;
    def replace_line(self, line: str, new_line: str): ...;

    CodeLine: "Type[CodeLine]" = None; # type: ignore

    def adjust_code(self) -> Unknown: ...;

    def get_current_line(self) -> RunnerLineContextProtocol: ...;
    def set_current_line(self, line: RunnerLineContextProtocol): ...;

    def execute(self, label: str): ...;

    def has_lib(self, name: str) -> bool: ...;

    def undo_current_stack(self): ...;