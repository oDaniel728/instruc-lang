# Library Development Guide

Este guia ensina como criar novas bibliotecas para a Instruc Lang.

## Objetivo

Uma biblioteca em `src/libs` pode:

- expor metodos para `call nome_da_lib@metodo`
- registrar verificadores de sintaxe (novos comandos)
- registrar ajustadores de sintaxe (reescrita de linha)
- injetar codigo automaticamente com `inject_code`

## Passo a passo rapido

1. Crie o arquivo `src/libs/minha_lib.py`.
2. Implemente uma ou mais funcoes publicas.
3. Implemente `_on_load(ctx)` para registrar hooks.
4. No arquivo `.instruc`, carregue com `req minha_lib`.
5. Use com `call minha_lib@metodo` ou com sua sintaxe customizada.

## Template minimo

```python
from typing import TYPE_CHECKING as __TC__

if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol


def hello(ctx: "RunnerAPIProtocol"):
    cstack = ctx.get_current_stack()
    cstack.append("hello")


def _on_load(ctx: "RunnerAPIProtocol"):
    # Opcional: registrar verificadores ou adjusters
    pass
```

Uso em `.instruc`:

```instruc
new def @load
    req comments
    req std
    req minha_lib
end def

new def @main
    new stack $
    use stack $
        call minha_lib@hello
        call std@print
    end stack *
end def

new def @quit
end def
```

## _on_load: quando usar

`_on_load(ctx)` e executado no momento do `req nome_da_lib`.

Use `_on_load` para:

- registrar verificadores: `ctx.add_syntax_verification(func)`
- registrar adjusters: `ctx.add_syntax_adjuster(func)`
- registrar valores em memoria: `ctx.register_memory(nome, valor)`
- injetar codigo: `ctx.inject_code([...], "@load")`

Evite usar `_on_load` para:

- mutar stacks de negocio sem necessidade
- imprimir logs em excesso em producao

## Regex para novos comandos

A maioria das libs novas define comandos por regex em verificadores.

Referencia oficial do Python:

- https://docs.python.org/3/howto/regex.html

Exemplo de verificador:

```python
import re


def _my_kw_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line
    if m := re.match(r"^mykw\s+(\d+)\s*$", line):
        value = int(m.group(1))
        ctx.get_current_stack().append(value)
    return None
```

Boas praticas com regex:

- use `^` e `$` para evitar match parcial inesperado
- prefira grupos nomeados em regex longas
- reutilize padroes do runtime quando possivel, como `ctx.enum.SyntaxRulePatterns.STACK_NAME`
- compile regex em variaveis quando o padrao for usado em varios lugares
- teste entradas invalidas alem das validas

## Variaveis privadas e dunder

No contexto deste projeto, use dois niveis:

- privado de modulo: prefixo simples `_nome`
- interno forte de modulo: prefixo dunder `__NOME`

Exemplo em libs existentes:

- `__PREFIX`, `__NAMESPACE` em `src/libs/stacks.py`

Importante sobre dunder neste projeto:

- o carregador em `src/importer.py` remove simbolos que comecam com `__`
- isso significa que variaveis e funcoes dunder nao sao exportadas como API da lib
- use dunder para constantes internas que nao devem ser acessadas externamente

## Tipagem recomendada

Importe tipos apenas em TYPE_CHECKING para evitar custo de import ciclico:

```python
from typing import TYPE_CHECKING as __TC__

if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol
```

Assine funcoes com os protocolos:

```python
def meu_metodo(ctx: "RunnerAPIProtocol"):
    ...

def meu_verificador(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    ...
```

Detalhes completos de protocolos:

- veja `docs/types-protocols.md`

## Boas praticas gerais

- mantenha cada biblioteca com um foco unico
- padronize nomes de comandos (prefixo curto e claro)
- sempre retorne `None` em verificadores que nao interrompem fluxo
- use mensagens de erro objetivas quando houver validacao de entrada
- evite alterar estado global fora do `ctx`
- adicione pelo menos um teste `.instruc` para cada nova feature
- documente comando, sintaxe e exemplo de uso no docs

## Checklist de entrega para nova lib

- arquivo criado em `src/libs`
- funcoes de API implementadas
- `_on_load` implementado (se necessario)
- teste em `test/test_<nome>.instruc`
- documentacao atualizada em `docs/language-reference.md`
- referencia do teste atualizada em `docs/tests-reference.md`
