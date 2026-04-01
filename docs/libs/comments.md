# comments

## Objetivo

Permitir comentarios de linha com `#`.

## Comportamento

Com `req comments`, tudo apos `#` na linha e removido antes da execucao.

## Exemplo em Instruc

```instruc
new def @load
    req comments
    req std
end def

new def @main
    new stack $
    use stack $
        load 10 # este trecho nao e executado
        print
    end stack *
end def
```

## Por baixo dos panos

- `_comment_verif` aplica `re.sub(r"#.*$", "", line)`.
- `_on_load` registra esse adjuster e roda `ctx.adjust_code()` para reaplicar o ajuste no codigo ja lido.

## Codigo fonte Python

```python
import re
from typing import TYPE_CHECKING as __TC__
import builtins as __builtins__

if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol

def _comment_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    line = re.sub(r"#.*$", "", line);
    return line;
def _on_load(ctx: "RunnerAPIProtocol"):
    ctx.add_syntax_adjuster(_comment_verif)
    ctx.adjust_code();
    return None;
```
