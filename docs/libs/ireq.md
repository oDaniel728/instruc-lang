# ireq

## Objetivo

Importar e executar outro arquivo `.instruc` em tempo de execucao, usando caminho entre aspas.

## Dependencia

- exige que `str` ja esteja carregada (`req str`), pois usa a memoria `str:__quote`

## Comando

- `ireq "caminho/arquivo.instruc"`

## Exemplo em Instruc

```instruc
new def @load
    req str
    req ireq
end def

new def @main
    ireq "./test/test_imports.instruc"
end def
```

## Por baixo dos panos

- `_on_load` valida dependencia de `str`.
- Monta regex com o mesmo padrao de aspas guardado em `str:__quote`.
- No match, resolve `Path(f).resolve()` e chama `ctx.require_file(...)`.

## Codigo fonte Python

```python
import re
from typing import TYPE_CHECKING as __TC__;
import builtins as __builtins__

from pathlib import Path;
if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol;

def _on_load(ctx: "RunnerAPIProtocol"):
    if not ctx.has_lib("str"): raise Exception("Library 'str' is required for 'ireq' to work. Please load it before using 'ireq'.");
    __kw = "ireq";
    __quote = ctx.get_memory("str:__quote", None);
    __import_format = fr"^{__kw}\s+{__quote}(.*){__quote}$";
    @ctx.add_syntax_verification
    def __import_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
        line = cl.line
        if m:=re.match(__import_format, line):
            f = m.group(1);
            ctx.require_file(Path(f).resolve());
```
