# math

## Objetivo

Executar operacoes matematicas sobre os valores numericos da stack ativa.

## Metodos

- `call math@opsum`
- `call math@opsub`
- `call math@opmul`
- `call math@opdiv`
- `call math@oppow`
- `call math@opmod`

## Exemplo em Instruc

```instruc
new def @load
    req std
    req math
end def

new def @main
    new stack $
    use stack $
        load 2
        load 3
        load 4
        call math@opmul
        print
    end stack *
end def
```

## Por baixo dos panos

- Cada metodo percorre a stack ativa e considera apenas `int`/`float`.
- Ao final, limpa a stack e empilha um unico resultado.
- Algumas operacoes usam acumulador inicial igual a `1` (`opmul`, `opdiv`, `oppow`, `opmod`).

## Codigo fonte Python

```python
import re
from typing import TYPE_CHECKING as __TC__
import builtins as __builtins__

if __TC__:
    from ..types import RunnerAPIProtocol

def opsum(ctx: "RunnerAPIProtocol"):
    cstack = ctx.get_current_stack();
    s = sum(v for v in cstack if isinstance(v, (int, float)));
    ctx.get_current_stack().clear();
    ctx.get_current_stack().append(s);

def opsub(ctx: "RunnerAPIProtocol"):
    cstack = ctx.get_current_stack();
    s = 0;
    for v in cstack:
        if isinstance(v, (int, float)):
            s -= v;
    ctx.get_current_stack().clear();
    ctx.get_current_stack().append(s);
    
def opmul(ctx: "RunnerAPIProtocol"):
    cstack = ctx.get_current_stack();
    s = 1;
    for v in cstack:
        if isinstance(v, (int, float)):
            s *= v;
    ctx.get_current_stack().clear();
    ctx.get_current_stack().append(s);

def opdiv(ctx: "RunnerAPIProtocol"):
    cstack = ctx.get_current_stack();
    s = 1;
    for v in cstack:
        if isinstance(v, (int, float)):
            s //= v;
    ctx.get_current_stack().clear();
    ctx.get_current_stack().append(s);

def oppow(ctx: "RunnerAPIProtocol"):
    cstack = ctx.get_current_stack();
    s = 1;
    for v in cstack:
        if isinstance(v, (int, float)):
            s **= v;
    ctx.get_current_stack().clear();
    ctx.get_current_stack().append(s);

def opmod(ctx: "RunnerAPIProtocol"):
    cstack = ctx.get_current_stack();
    s = 1;
    for v in cstack:
        if isinstance(v, (int, float)):
            s %= v;
    ctx.get_current_stack().clear();
    ctx.get_current_stack().append(s);

def _on_load(ctx: "RunnerAPIProtocol"):
    pass
```
