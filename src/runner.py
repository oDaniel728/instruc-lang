import importlib
from pathlib import Path
import re
from typing import Any, Callable

from .codeline import CodeLine
from . import enum
from .importer import carregar_simbolos
from .types import RunnerAPIProtocol


class Runner():
    """Runtime executor for Instruc programs."""
    enum = enum;
    CodeLine = CodeLine;
    SyntaxAdjusters = list[Callable[["CodeLine", "RunnerAPIProtocol"], Any]]();
    def __init__(self, file: Path | str) -> None:
        self.fp = Path(file);
        self.stacks = dict[str, list[Any]]();
        self.labels = dict[str, list[CodeLine]]();
        self.memory = dict[str, Any]();
        self.libs = dict[str, dict[str, Any]]();

        self._current_label = "";
        self._current_stack = "";

    def __require__(self, name: str) -> dict[str, Any]:
        f = Path(f"src/libs/{name}.py");
        symbols = carregar_simbolos(f);
        if "_on_load" in symbols:
            symbols["_on_load"](self);
        return symbols;
    def require(self, name: str):
        c = self.__require__(name);
        self.libs[name] = c;
    
    def get_current_stack(self) -> list[Any]:
        if self._current_stack == "":
            return [];
        return self.get_stack(self._current_stack);
    def get_current_stack_name(self) -> str:
        return self._current_stack;
    def set_current_stack(self, name: str):
        self._current_stack = name;

    def get_stack(self, name: str) -> list[Any]:
        if name not in self.stacks:
            self.stacks[name] = [];
        return self.stacks[name];
    def get_label(self, name: str) -> list[CodeLine]:
        if name not in self.labels:
            self.labels[name] = [];
        return self.labels[name];
    def get_memory[T](self, name: str, default: T) -> T:
        if name not in self.memory:
            self.memory[name] = default;
        return self.memory[name];

    def register_stack(self, name: str):
        if name not in self.stacks:
            self.stacks[name] = [];
    def register_label(self, name: str):
        if name not in self.labels:
            self.labels[name] = [];
    def register_memory(self, name: str, default: Any):
        if name not in self.memory:
            self.memory[name] = default;
    
    def overwrite_stack(self, name: str, value: list[Any]):
        self.stacks[name] = value;
    def overwrite_label(self, name: str, value: list[CodeLine]):
        self.labels[name] = value;
    def overwrite_memory(self, name: str, value: Any):
        self.memory[name] = value;

    def explode_stack(self, name: str):
        del self.stacks[name];
    
    def replace_code(self, expression: str, repl: Callable[[re.Match], str] | str):
        for label in self.labels.values():
            for line in label:
                if re.match(expression, line.line):
                    line.line = re.sub(expression, repl, line.line);
    def replace_line(self, line: str, new_line: str):
        for label in self.labels.values():
            for l in label:
                if l.line == line:
                    l.line = new_line;
    def explode_code(self, expression: str):
        for label in self.labels.values():
            label[:] = [line for line in label if not re.match(expression, line.line)];

    def get_libs(self) -> dict[str, dict[str, Any]]:
        return self.libs;
    def get_lib(self, name: str) -> dict[str, Any]:
        return self.libs[name];

    def get_method(self, id: str) -> Callable[["RunnerAPIProtocol"], None]:
        # name = lib@method
        if "@" in id:
            lib_name, method_name = id.split("@", 1);
            if lib_name in self.libs and method_name in self.libs[lib_name]:
                return self.libs[lib_name][method_name];
        else:
            for lib in self.libs.values():
                if id in lib:
                    return lib[id];
        raise Exception(f"Method '{id}' not found in any loaded library");

    def get_syntax_verifications(self):
        return CodeLine.SYNTAXVERIFS;
    def add_syntax_verification(self, func: Callable[[CodeLine, "RunnerAPIProtocol"], None]):
        CodeLine.SYNTAXVERIFS.append(func);
    
    def get_syntax_adjusters(self):
        return self.SyntaxAdjusters;
    def add_syntax_adjuster(self, func: Callable[[CodeLine, "RunnerAPIProtocol"], None]):
        self.SyntaxAdjusters.append(func);
    
    def inject_code(self, lines: list[str | CodeLine], label: str = "@main"):
        lines = ["# new INJEC", *lines, "# end INJEC"];
        lines_ = []
        for line in lines:
            if isinstance(line, str):
                line = CodeLine(line);
            lines_.append(line);
        self.get_label(label).extend(lines_);

    def each_line(self, line: str):
        line = line.strip();
        if (line == ''): return;
        c = CodeLine(line)
        if m:=re.match(
            enum
                .SyntaxRegularExpressionPatterns
                .DEFINE_LABEL, 
            line
        ):
            self._current_label = m.group(1);
            self.register_label(self._current_label);
        elif m:=re.match(
            enum
                .SyntaxRegularExpressionPatterns
                .END_LABEL, 
            line
        ):
            self._current_label = "";
        elif self._current_label != "":
            self.get_label(self._current_label).append(c);

    def read(self):
        """Parse the source file and distribute lines by label."""
        with self.fp.open() as f:
            for line in f:
                self.each_line(line)

    def execute(self, label: str):
        """Execute all lines registered for a label."""
        for line in self.labels[label]:
            line.execute(self)

    def adjust_code(self):
        """Apply all syntax adjusters to all parsed lines."""
        for label in self.labels.values():
            for line in label:
                line.adjust(self);

    def snapshot(self):
        print("Stacks:")
        for name, stack in self.stacks.items():
            print(f"  {name}: {stack}");
        print("Labels:")
        for name, label in self.labels.items():
            print(f"  {name}: {label}");
        print("Memory:")
        for name, mem in self.memory.items():
            print(f"  {name}: {mem}");
        print("Libs:")
        for name, lib in self.libs.items():
            print(f"  {name}: {lib}");

    def run(self, debug: bool = False):
        """Run the full lifecycle: @load, @main, @quit."""
        self.read();
        self.adjust_code();
        self.execute("@load");
        self.execute("@main");
        self.execute("@quit");
        if debug:
            self.snapshot();
