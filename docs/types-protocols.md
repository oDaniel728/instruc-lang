# Types Protocols Reference

Referencia detalhada de todos os simbolos de tipagem definidos em `src/types.py`.

## Escopo

Este documento cobre:

- aliases de tipo
- callables de extensao da linguagem
- protocolos (`CodeLineProtocol`, `RunnerLineContextProtocol`, `RunnerAPIProtocol`)
- atributos especiais do runtime expostos via protocolo
- observacoes de compatibilidade entre contrato e implementacao atual

## Mapa de simbolos de src/types.py

- `Unknown = Any`
- `SyntaxVerification = Callable[[CodeLine, RunnerAPIProtocol], Any]`
- `SyntaxAdjuster = Callable[[CodeLine, RunnerAPIProtocol], Any]`
- `CodeLineProtocol`
- `RunnerLineContextProtocol`
- `RunnerAPIProtocol`

## Alias de tipos

### Unknown

`Unknown` e um alias para `Any`.

Uso esperado:

- retornos dinamicos como `snapshot()`
- APIs cujo formato pode variar sem quebrar assinaturas

### SyntaxVerification

Assinatura:

```python
Callable[[CodeLine, RunnerAPIProtocol], Any]
```

Representa um verificador/interpretador de linha.

Comportamento esperado no runtime:

- recebe a linha atual e o contexto (`ctx`)
- pode executar efeitos colaterais (mudar stack, chamar metodo, etc.)
- pode retornar `None`, `"SKIP"`, ou outro valor que o fluxo interprete

### SyntaxAdjuster

Assinatura:

```python
Callable[[CodeLine, RunnerAPIProtocol], Any]
```

Representa um ajustador de sintaxe executado antes dos verificadores.

Comportamento esperado:

- transforma `cl.line` direta ou indiretamente
- pode retornar nova string de linha (dependendo do implementador)

## CodeLineProtocol

Contrato de uma linha executavel.

### Atributo

- `line: str`

### Metodos

- `execute(runnerapi: RunnerAPIProtocol)`
- `__str__() -> str`
- `__repr__() -> str`

### Quando usar em bibliotecas

- em verificadores que precisam ler/parsing da linha atual
- em adjusters que limpam ou reescrevem comandos

## RunnerLineContextProtocol

Contrato do contexto de linha corrente no executor.

### Propriedades

- `index: int`
  - indice da linha no label atual
- `codeline: CodeLineProtocol`
  - objeto de linha corrente

### Observacao

Esse contrato existe para permitir leitura/escrita do estado de linha durante execucao, sem acoplar o codigo a uma classe concreta.

## RunnerAPIProtocol

Contrato principal consumido por bibliotecas em `src/libs`.

## Grupo 1: stacks, labels e memoria

### Leitura

- `get_stack(name: str) -> list[Any]`
- `get_label(name: str) -> list[CodeLine]`
- `get_memory[T](name: str, default: T) -> T`

Notas:

- `get_stack` e `get_label` no runtime atual criam automaticamente o item se nao existir.
- `get_memory` suporta fallback tipado via parametro generico `T`.

### Registro

- `register_stack(name: str)`
- `register_label(name: str)`
- `register_memory(name: str, default: Any)`

### Sobrescrita

- `overwrite_stack(name: str, value: list[Any])`
- `overwrite_label(name: str, value: list[CodeLine])`
- `overwrite_memory(name: str, value: Any)`

## Grupo 2: stack corrente

- `get_current_stack() -> list[Any]`
- `get_current_stack_name() -> str`
- `set_current_stack(name: str)`

Uso tipico:

- comandos que operam sobre a stack ativa (`std`, `math`, `str`)
- bibliotecas que trocam contexto temporariamente (`stacks`)

## Grupo 3: carga de bibliotecas e arquivos

- `require(name: str)`
- `require_file(path: str | Path)`
- `has_lib(name: str) -> bool`
- `get_libs() -> dict[str, dict[str, Any]]`
- `get_lib(name: str) -> dict[str, Any]`
- `get_method(id: str) -> Callable[[RunnerAPIProtocol], None]`

Notas:

- `get_method` aceita `lib@metodo` e tambem busca por nome sem prefixo em libs carregadas.
- `require_file` e usado por `ireq` para importar `.instruc` externo.

## Grupo 4: extensao de sintaxe

- `get_syntax_verifications() -> list[SyntaxVerification]`
- `add_syntax_verification(func: SyntaxVerification)`
- `overwrite_syntax_verification(name: str, func: SyntaxVerification)`
- `get_syntax_adjusters() -> list[SyntaxAdjuster]`
- `add_syntax_adjuster(func: SyntaxAdjuster)`
- `adjust_code() -> Unknown`

Notas:

- verificadores implementam novos comandos e keywords
- adjusters reescrevem/limpam linhas antes da execucao
- no runtime atual, `overwrite_syntax_verification` esta no protocolo, mas nao possui implementacao concreta em `src/runner.py`

## Grupo 5: transformacao e injecao de codigo

- `inject_code(lines: list[str | CodeLine], label: str = "@main")`
- `replace_code(expression: str, repl: Callable[[re.Match], str] | str)`
- `replace_line(line: str, new_line: str)`
- `explode_code(expression: str)`
- `explode_stack(name: str)`

Uso tipico:

- injecao automatica de dependencias (`basic`)
- remocao/substituicao de trechos por regex
- limpeza de estruturas temporarias

## Grupo 6: execucao e observabilidade

- `execute(label: str)`
- `snapshot() -> Unknown`
- `get_current_line() -> RunnerLineContextProtocol`
- `set_current_line(line: RunnerLineContextProtocol)`

## Atributos de classe expostos pelo protocolo

- `enum = enum`
  - acesso aos padroes e keywords oficiais (`ctx.enum.SyntaxRulePatterns.*`)
- `CodeLine: Type[CodeLine]`
  - acesso ao construtor de linha para execucao dinamica (`ctx.CodeLine(...)`)

## Fluxo tipico de uma biblioteca com tipagem correta

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

## Convenio de imports para tipagem

Padrao recomendado nas libs:

```python
from typing import TYPE_CHECKING as __TC__

if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol
```

Motivo:

- evita import ciclico em runtime
- mantem autocomplete e verificacao estatica

## Compatibilidade e manutencao

`src/types.py` e a fonte de verdade do contrato de extensao.

Sempre que `src/runner.py` ou `src/codeline.py` mudar API publica:

1. atualize `src/types.py`
2. atualize este documento
3. valide impacto nas bibliotecas em `src/libs`
