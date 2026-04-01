# label

## Objetivo

Permitir chamar labels diretamente com `call <label>`, sem `lib@metodo`.

## Comando

- `call <nome_da_label>`

## Exemplo em Instruc

```instruc
new def @load
    req str
    req std
    req label
end def

new def hello
    str loadstr "hello"
    call std@print
end def

new def @main
    call hello
end def
```

## Por baixo dos panos

- O verificador `__call_label_verif` reconhece `call <label>` por regex.
- Em vez de buscar metodo de biblioteca, chama `ctx.execute(lbl)`.
- Retorna `"SKIP"` para sinalizar que a linha ja foi tratada.

## Codigo fonte Python

```python
import re
from typing import TYPE_CHECKING as __TC__
import builtins as __builtins__

if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol

def __call_label_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    LABEL = ctx.enum.SyntaxRulePatterns.LABEL_NAME;
    CALL = ctx.enum.SyntaxKeywords.CALL;
    if m:=re.match(
        fr"^{CALL}\s+({LABEL})\s*$",
        line
    ):
        lbl = m.group(1);
        ctx.execute(lbl);
        return "SKIP";

def _on_load(ctx: "RunnerAPIProtocol"):
    ctx.add_syntax_verification(__call_label_verif);
    return None;
```
