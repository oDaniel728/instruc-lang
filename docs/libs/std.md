# std

## Objetivo

Fornecer metodos padrao de saida e inspeccao.

## Metodos

- `call std@print`: imprime todos os itens da stack ativa
- `call std@printf`: imprime o primeiro item da stack ativa
- `call std@snap`: imprime o snapshot completo do runner
- `print`: atalho registrado pela propria biblioteca

## Exemplo em Instruc

```instruc
new def @load
    req std
end def

new def @main
    new stack $
    use stack $
        load 1
        load 2
        call std@print
        print
        call std@snap
    end stack *
end def
```

## Por baixo dos panos

- As funcoes `print`, `printf` e `snap` sao metodos normais da lib.
- No `_on_load`, a lib registra um verificador para reconhecer a keyword `print` sem `call`.

## Codigo fonte Python

```python
import re
from typing import TYPE_CHECKING as __TC__
import builtins as __builtins__

if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol

def print(ctx: "RunnerAPIProtocol"):
    cstack = ctx.get_current_stack();
    __builtins__.print(*cstack);
def printf(ctx: "RunnerAPIProtocol"):
    cstack = ctx.get_current_stack();
    __builtins__.print(cstack[0]);

def snap(ctx: "RunnerAPIProtocol"):
    snap = ctx.snapshot();
    __builtins__.print(snap);

def _on_load(ctx: "RunnerAPIProtocol"):
    @ctx.get_syntax_verifications().append
    def _print_kw(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
        line = cl.line;
        if m:=re.match(
            r"^print\s*$",
            line
        ):
            print(ctx);
        return None;
    # @ctx.get_syntax_verifications().append
    # def _say_idk(l, ctx):
    #     __builtins__.print(l);
    #     return None;
```
