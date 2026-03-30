import re
from typing import Any, Callable, Protocol, TYPE_CHECKING, Type
type Unknown = Any
from . import enum
if TYPE_CHECKING:
    from .codeline import CodeLine

class CodeLineProtocol(Protocol):
    line: str;
    def execute(self, runnerapi: "RunnerAPIProtocol"): ...;
    def __str__(self) -> str: ...;
    def __repr__(self) -> str: ...;
class RunnerAPIProtocol(Protocol):
    def get_stack(self, name: str) -> list[Any]: ...;
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

    def get_libs(self) -> dict[str, dict[str, Any]]: ...;
    def get_lib(self, name: str) -> dict[str, Any]: ...;

    def get_syntax_verifications(self) -> list[Callable[["CodeLine", "RunnerAPIProtocol"], Any]]: ...;
    def add_syntax_verification(self, func: Callable[["CodeLine", "RunnerAPIProtocol"], Any]): ...;
    
    def get_syntax_adjusters(self) -> list[Callable[["CodeLine", "RunnerAPIProtocol"], Any]]: ...;
    def add_syntax_adjuster(self, func: Callable[["CodeLine", "RunnerAPIProtocol"], Any]): ...;

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