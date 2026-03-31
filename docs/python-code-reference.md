# Python Code Reference

Este documento descreve os modulos Python que implementam o runtime da Instruc Lang.

## Visao geral

Arquivos principais:

- `main.py`: entrada da aplicacao
- `src/runner.py`: estado global e ciclo de execucao
- `src/codeline.py`: execucao de cada linha da linguagem
- `src/enum.py`: palavras-chave e regex da sintaxe
- `src/importer.py`: carregamento seguro de bibliotecas Python
- `src/types.py`: protocolos de tipagem para extensao das libs

Bibliotecas nativas:

- `src/libs/std.py`
- `src/libs/math.py`
- `src/libs/stacks.py`
- `src/libs/str.py`
- `src/libs/comments.py`
- `src/libs/basic.py`
- `src/libs/sayeachline.py`

## main.py

Responsavel por:

- ler argumentos de linha de comando
- validar se um arquivo `.instruc` foi passado
- criar `Runner(file)`
- executar `runner.run(debug)`

Flags:

- `-d` ou `--debug`: mostra snapshot de stacks, labels, memoria e libs no final.

## src/runner.py

Classe central: `Runner`.

Estado interno:

- `stacks: dict[str, list[Any]]`
- `labels: dict[str, list[CodeLine]]`
- `memory: dict[str, Any]`
- `libs: dict[str, dict[str, Any]]`
- `_current_label`, `_current_stack`

Metodos principais:

- `read()`: le o arquivo `.instruc` e separa por labels (`new def`, `end def`).
- `adjust_code()`: aplica todos os syntax adjusters registrados por libs.
- `execute(label)`: executa todas as linhas de uma label.
- `run(debug=False)`: fluxo completo (`@load`, `@main`, `@quit`).
- `require(name)`: carrega uma lib Python de `src/libs/<name>.py`.

Utilitarios de extensao:

- `add_syntax_verification(func)`
- `add_syntax_adjuster(func)`
- `inject_code(lines, label='@main')`
- `replace_code(...)`, `replace_line(...)`, `explode_code(...)`

## src/codeline.py

Classe `CodeLine` representa uma linha de codigo Instruc.

Fluxo da linha:

1. `adjust(runnerapi)`: executa ajustadores (ex.: remover comentarios)
2. `execute(runnerapi)`: executa validadores de sintaxe/comando

Verificadores base registrados no arquivo:

- `__stack_controls__`: `new stack`, `use stack`, `end stack`, `ret`
- `__stack_operators__`: `load`, `kill`
- `__requirements__`: `req`
- `__methods__`: `call lib@metodo`

## src/enum.py

Centraliza tokens e expressoes regulares da linguagem:

- `SyntaxKeywords`: palavras-chave (`new`, `use`, `end`, `req`, etc.)
- `SyntaxRulePatterns`: padroes basicos para nomes
- `SyntaxRegularExpressionPatterns`: regex finais usadas no parser

## src/importer.py

Funcao principal: `carregar_simbolos(path: Path)`.

Comportamento:

- le o arquivo Python da lib
- converte `if TYPE_CHECKING:` para `if False:` via AST
- executa o modulo em namespace isolado
- retorna simbolos publicos (sem `__dunder__`)

Objetivo: carregar libs sem dependencia de importacao padrao e sem poluir `sys.modules`.

## src/types.py

O detalhamento completo dos protocolos foi movido para:

- `docs/types-protocols.md`

Resumo rapido:

- `CodeLineProtocol`: contrato de uma linha de codigo executavel
- `RunnerAPIProtocol`: contrato da API que as bibliotecas usam

## Bibliotecas em src/libs

### std.py

Funcoes:

- `print(ctx)`: imprime toda stack atual
- `printf(ctx)`: imprime apenas o primeiro item
- `snap(ctx)`: imprime snapshot completo

No `_on_load`, registra atalho de linguagem:

- linha `print` (sem `call`) chama `std.print`.

### math.py

Operacoes sobre numeros da stack atual:

- `opsum`, `opsub`, `opmul`, `opdiv`, `oppow`, `opmod`

Padrao de execucao:

- processa itens numericos
- limpa stack atual
- adiciona resultado unico

### stacks.py

DSL auxiliar com prefixo `stack`:

- `stack merge s1 s2`
- `stack merge s1 s2 > s3`
- `stack load s1`
- `stack call metodo as s1 > s2`
- `stack run <linha> as s1 > s2`

No `_on_load`:

- registra palavras-chave em `memory`
- registra verificadores de sintaxe da DSL de stacks

### str.py

DSL auxiliar com prefixo `str`:

- `str load X`
- `str loadstr "texto"`
- `str loadint 65`
- `str joinchars`
- `str concat a b > destino`

Aceita concatenacao por literal e por stack (quando os argumentos sao nomes de stack).

### comments.py

Registra syntax adjuster que remove tudo apos `#` na linha.

### basic.py

No carregamento, injeta automaticamente em `@load`:

- `req comments`
- `req std`

### sayeachline.py

Registra verificador que imprime cada linha executada.
Util para debug de fluxo.

## Ordem recomendada para entender o codigo

1. `main.py`
2. `src/runner.py`
3. `src/codeline.py`
4. `src/libs/*.py`
5. `src/importer.py`
6. `docs/types-protocols.md`
