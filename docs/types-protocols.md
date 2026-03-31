# Types Protocols Reference

Este documento descreve os protocolos definidos em `src/types.py`.

## Por que existem protocolos

Os protocolos definem contratos de tipagem entre o runtime e as bibliotecas.

Vantagens:

- autocomplete melhor em editores
- validacao estatica de assinaturas
- menor acoplamento com implementacao concreta de Runner

## CodeLineProtocol

Representa uma linha executavel da linguagem.

Campos e metodos principais:

- `line: str`
- `execute(runnerapi)`
- `__str__()`
- `__repr__()`

Quando usar:

- funcoes de verificacao de sintaxe que recebem a linha atual
- adjusters que precisam ler ou transformar `line`

## RunnerAPIProtocol

Representa a API que uma biblioteca pode usar para interagir com o runtime.

Grupos principais de metodos:

1. Stacks e labels
- `get_stack`, `get_label`, `get_current_stack`, `set_current_stack`
- `register_stack`, `register_label`
- `overwrite_stack`, `explode_stack`

2. Memoria
- `get_memory`, `register_memory`, `overwrite_memory`

3. Bibliotecas e metodos
- `require`
- `get_libs`, `get_lib`, `get_method`

4. Extensao de sintaxe
- `get_syntax_verifications`, `add_syntax_verification`
- `get_syntax_adjusters`, `add_syntax_adjuster`
- `inject_code`, `replace_code`, `replace_line`, `explode_code`

5. Utilitarios de runtime
- `snapshot`
- `adjust_code`
- acesso ao namespace de enum com `enum`
- acesso ao tipo de linha com `CodeLine`

## Exemplo pratico com protocolos

```python
import re
from typing import TYPE_CHECKING as __TC__

if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol


def push_zero(ctx: "RunnerAPIProtocol"):
    ctx.get_current_stack().append(0)


def _zero_kw(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    if re.match(r"^zero\s*$", cl.line):
        push_zero(ctx)
    return None


def _on_load(ctx: "RunnerAPIProtocol"):
    ctx.add_syntax_verification(_zero_kw)
```

## Diretriz de importacao tipada

Padrao recomendado:

```python
from typing import TYPE_CHECKING as __TC__

if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol
```

Esse padrao evita importacao em runtime apenas para tipos.

## Relacao com src/types.py

O arquivo `src/types.py` e a fonte de verdade dessas assinaturas.
Quando houver mudanca de API no Runner, atualize os protocolos e as libs dependentes.
