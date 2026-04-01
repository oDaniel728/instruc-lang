# builtins

## Objetivo

Biblioteca interna do runtime. Ela registra os verificadores base da linguagem (stack, load/kill, req, call).

Essa biblioteca e carregada automaticamente em `Runner.run()` com `self.require("builtins")`.

## Comportamentos registrados

- controle de stacks:
  - `new stack <nome>`
  - `use stack <nome>`
  - `end stack <nome|*>`
  - `ret <valor>`
- operadores base:
  - `load <int>`
  - `kill <int>`
- requisito de biblioteca:
  - `req <lib>`
- chamada de metodo:
  - `call <lib>@<metodo>`

## Exemplo em Instruc

```instruc
new def @load
    req std
end def

new def @main
    new stack $
    use stack $
        load 10
        load 20
        call std@print
        kill 10
        print
    end stack *
end def
```

## Por baixo dos panos

- `__stack_controls__` usa regex do `ctx.enum` para manipular criacao/uso/fim de stack.
- `__stack_operators__` le `load` e `kill` e altera a stack ativa.
- `__requirements__` executa `ctx.require(...)` para `req`.
- `__methods__` resolve `lib@metodo`, valida existencia e executa o callable.
- `_on_load` registra todos esses verificadores com `ctx.add_syntax_verification(...)`.

## Codigo fonte Python

```python
import re
from typing import TYPE_CHECKING as __TC__
import builtins as __builtins__

if __TC__:
    from ..types import (
        RunnerAPIProtocol, 
        CodeLineProtocol
    )

def __stack_controls__(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    enum = ctx.enum;
    if m:=re.match(
        enum
            .SyntaxRegularExpressionPatterns
            .DEFINE_STACK,
        line
    ):
        ctx.register_stack(m.group(1));
    elif m:=re.match(
        enum
            .SyntaxRegularExpressionPatterns
            .USE_STACK,
        line
    ):
        ctx.register_stack(m.group(1));
        ctx.set_current_stack(m.group(1));
    elif m:=re.match(
        enum
            .SyntaxRegularExpressionPatterns
            .END_STACK,
        line
    ):
        if m.group(1) == "*" or m.group(1) == ctx.get_current_stack():
            ctx.set_current_stack("");
        if m.group(1) == "*":
            for s in ctx.get_stack(m.group(1)):
                ctx.overwrite_stack(s, []);
        else:
            ctx.register_stack(m.group(1));
    elif m:=re.match(
        enum
            .SyntaxRegularExpressionPatterns
            .RETURN,
        line
    ):
        return m.group(1);

def __stack_operators__(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    enum = ctx.enum;
    cstack = ctx.get_current_stack();
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

def __requirements__(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    enum = ctx.enum
    if m:=re.match(
        enum
            .SyntaxRegularExpressionPatterns
            .REQUIREMENT,
        line
    ):
        ctx.require(m.group(1));

def __methods__(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    enum = ctx.enum
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
            if lib not in ctx.get_libs():
                raise Exception(f"Lib '{lib}' not found");
            if method not in ctx.get_lib(lib):
                raise Exception(f"Method '{method}' not found in lib '{lib}'");
            m = ctx.get_lib(lib)[method];
            m(ctx);

def _on_load(ctx: "RunnerAPIProtocol"):
    ctx.add_syntax_verification(__stack_controls__);
    ctx.add_syntax_verification(__stack_operators__);
    ctx.add_syntax_verification(__requirements__);
    ctx.add_syntax_verification(__methods__);
```
