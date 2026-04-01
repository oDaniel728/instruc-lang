# sayeachline

## Objetivo

Biblioteca de debug para imprimir cada linha executada.

## Comportamento

Nao adiciona palavra-chave nova. Apenas registra um verificador que imprime `cl.line` em toda linha executada.

## Exemplo em Instruc

```instruc
new def @load
    req sayeachline
    req std
end def

new def @main
    new stack $
    use stack $
        load 1
        print
    end stack *
end def
```

## Por baixo dos panos

- `_on_load` adiciona uma funcao ao fim da lista de verificadores.
- Esse verificador chama `__builtins__.print(cl.line)` e retorna `None`.

## Codigo fonte Python

```python
import re
from typing import TYPE_CHECKING as __TC__
import builtins as __builtins__

if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol
def _on_load(ctx: "RunnerAPIProtocol"):    
    @ctx.get_syntax_verifications().append
    def _say_each_line_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
        __builtins__.print(cl.line);
        return None;
```
