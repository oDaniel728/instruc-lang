# Architecture

Visao tecnica da implementacao atual.

## Fluxo de execucao

1. [main.py](../main.py) recebe caminho do arquivo `.instruc`
2. Cria um `Runner`
3. `Runner.read()` separa o codigo por labels (`@load`, `@main`, `@quit`)
4. `Runner.adjust_code()` aplica ajustadores de sintaxe (ex.: comentarios)
5. `Runner.execute()` roda labels na ordem:
   - `@load`
   - `@main`
   - `@quit`
6. Se `--debug`, mostra snapshot de estado

## Modulos principais

- [src/runner.py](../src/runner.py)
- [src/codeline.py](../src/codeline.py)
- [src/enum.py](../src/enum.py)
- [src/importer.py](../src/importer.py)
- [src/types.py](../src/types.py)

## Modelo de dados

O `Runner` mantem:

- `stacks`: dicionario de listas
- `labels`: dicionario de linhas de codigo por label
- `memory`: armazenamento auxiliar para libs
- `libs`: simbolos importados de cada biblioteca

## Extensibilidade por bibliotecas

Bibliotecas em [src/libs](../src/libs) podem:

- Registrar verificadores de sintaxe
- Registrar ajustadores de sintaxe
- Expor metodos para `call lib@metodo`
- Injetar codigo automaticamente em labels

Exemplo: `comments` registra um ajustador para remover comentarios apos `#`.

Contrato de tipagem da extensibilidade:

- [docs/types-protocols.md](types-protocols.md)
- define aliases (`SyntaxVerification`, `SyntaxAdjuster`) e protocolos (`CodeLineProtocol`, `RunnerLineContextProtocol`, `RunnerAPIProtocol`)

## Ciclo de uma linha

Cada `CodeLine` executa todos os verificadores registrados (`SYNTAXVERIFS`).
As regras base (stacks, load, kill, req, call) ficam em [src/codeline.py](../src/codeline.py).

## Observacoes de maturidade

Projeto em fase experimental, adequado para estudo de:

- Design de mini-linguagens
- Execucao baseada em pilhas
- Sistema de plugins simples por modulo Python
