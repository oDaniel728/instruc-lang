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

Bibliotecas nativas (documentacao por arquivo):

- [docs/libs/README.md](libs/README.md)
- [docs/libs/basic.md](libs/basic.md)
- [docs/libs/builtins.md](libs/builtins.md)
- [docs/libs/comments.md](libs/comments.md)
- [docs/libs/epar.md](libs/epar.md)
- [docs/libs/ireq.md](libs/ireq.md)
- [docs/libs/label.md](libs/label.md)
- [docs/libs/math.md](libs/math.md)
- [docs/libs/read.md](libs/read.md)
- [docs/libs/sayeachline.md](libs/sayeachline.md)
- [docs/libs/stacks.md](libs/stacks.md)
- [docs/libs/std.md](libs/std.md)
- [docs/libs/str.md](libs/str.md)

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

Resumo rapido dos simbolos de tipagem:

- `Unknown`: alias para `Any`
- `SyntaxVerification`: callable de verificador de sintaxe
- `SyntaxAdjuster`: callable de ajustador de sintaxe
- `CodeLineProtocol`: contrato de linha executavel
- `RunnerLineContextProtocol`: contrato da linha corrente no executor
- `RunnerAPIProtocol`: contrato da API que as bibliotecas usam

Detalhes importantes descritos no guia de tipos:

- agrupamento completo dos metodos por responsabilidade
- assinatura generica de `get_memory[T](...)`
- atributos especiais `enum` e `CodeLine` no contexto
- observacao de divergencia atual: `overwrite_syntax_verification` esta no protocolo, mas nao esta implementado em `Runner`

## Bibliotecas em src/libs

A documentacao detalhada das bibliotecas foi movida para arquivos dedicados em `docs/libs/`.
Cada arquivo inclui comandos/metodos, exemplos em Instruc, explicacao interna e codigo fonte Python da biblioteca.

## Ordem recomendada para entender o codigo

1. `main.py`
2. `src/runner.py`
3. `src/codeline.py`
4. `src/libs/*.py`
5. `src/importer.py`
6. `docs/types-protocols.md`
