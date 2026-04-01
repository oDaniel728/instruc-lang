# basic

## Objetivo

Atalho de setup: injeta requisicoes de bibliotecas comuns no label `@load`.

## O que ela injeta

Quando `req basic` e executado, a biblioteca injeta em `@load`:

- `req comments`
- `req std`
- `req str`
- `req label`

## Exemplo em Instruc

```instruc
new def @load
    req basic
end def

new def @main
    new stack $
    use stack $
        str loadstr "ola"
        call std@print
    end stack *
end def
```

## Por baixo dos panos

- `_on_load` chama `ctx.inject_code([...], "@load")`.
- Isso evita repetir os mesmos `req` em todo script.

## Codigo fonte Python

```python
import re
from typing import TYPE_CHECKING as __TC__
import builtins as __builtins__

if __TC__:
    from ..types import RunnerAPIProtocol
def _on_load(ctx: "RunnerAPIProtocol"):    
    ctx.inject_code([
        "req comments",
        "req std",
        "req str",
        "req label"
    ], "@load")
```
