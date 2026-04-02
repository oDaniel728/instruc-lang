# Changelog

Todas as mudancas relevantes deste projeto serão documentadas neste arquivo.

## [1.2.18.9] - 2026-04-02

### Adicoes

- Suporte a variaveis de memoria da linguagem (`src/libs/var.py`) e novo cenario de teste em `test/test_var.instruc`.
- Nova biblioteca `os` (`src/libs/os.py`) com verificacoes de `os cd "<path>"` e `os ls -> [...str]`, incluindo testes dedicados (`test/test_os.instruc`, `test/test_os_chdir.instruc`, `test/test_os_ls.instruc`).
- Suporte a loops `for/foreach` com a nova biblioteca `src/libs/for.py` e cobertura de testes em `test/test_for.instruc`.
- Novas capacidades de stack: `kill i <index>`, `kill *`, `stack loadv` para literais (`int`, `float`, `string`, `boolean`), selecao de item por indice e tratamento de indice `-` (ultimo item), com novos testes (`test/test_kill_index.instruc`, `test/test_stack_value.instruc`).
- Historico de stacks com operacoes de `undo` e recuperacao da ultima stack no runtime (`src/runner.py`).
- Expansao das regras de sintaxe para stack (`expand` com indice opcional, ajustes de regex e padroes em `src/codeline.py`, `src/enum.py`, `src/types.py`, `src/libs/stacks.py`).
- Novo modo silencioso no runner e evolucao do tratamento de erros de execucao (`src/runner.py`).
- Melhorias funcionais de strings com formatacao e ajustes em `src/libs/str.py`.
- Atualizacao de exemplos e documentacao compacta em `tiny.md`.

### Alteracoes

- Novo formato de versões: `[general release].[code release].[added features].[bug fixes]` para refletir melhor o estado do projeto.
- Atualizacao dos snippets de desenvolvimento em `.vscode/instruc.code-snippets`.
- Ajustes em bibliotecas internas (`src/libs/builtins.py`, `src/libs/comments.py`, `src/libs/stacks.py`, `src/libs/str.py`) para compatibilizar os novos fluxos de execucao e sintaxe.
- Inclusao de novos arquivos de apoio e cenarios complementares de teste (`test/lib.instruc`, `test/test_instruc_ireq.instruc`, `foo.txt`).

### Fixes

- Correcao da implementacao incremental de recursos adicionados em commits recentes.
- Correcao de variaveis de memoria da linguagem.
- Correcao no parser de comentarios para remover espacos extras no inicio/fim.
- Correcao no `get_stack_item` para aceitar indice em string e resolver `-` como ultimo item.
- Melhoria da rotina de `undo` com validacoes adicionais e teste de regressao para gerenciamento de stack.
- Ajustes de comentarios/testes relacionados ao modulo `os`.
- Ajuste de legibilidade no snippet boilerplate (linha em branco adicional).

### Remocoes

- Nenhuma remocao de funcionalidade ou arquivo de runtime nesta versao.

## [1.1.0] - 2026-03-31

### Adicoes

- Novas bibliotecas em `src/libs`: `builtins`, `epar`, `ireq` e `read`.
- Novos snippets para desenvolvimento em `.vscode/instruc.code-snippets` e `.vscode/lib.code-snippets`.
- Novos cenarios de teste: `test/epar.instruc`, `test/test_imports.instruc`, `test/test_input.instruc` e `test/script.im.py`.
- Nova documentacao por biblioteca em `docs/libs/`, com um arquivo Markdown por lib.
- Referencia detalhada de simbolos e protocolos de `src/types.py` em `docs/types-protocols.md`.

### Alteracoes

- Ajustes em `src/codeline.py`, `src/runner.py` e `src/types.py` para evolucao da API de verificacao de sintaxe e do contrato do runtime.
- Atualizacoes na biblioteca `src/libs/str.py`.
- Atualizacao dos documentos centrais (`README.md`, `docs/language-reference.md`, `docs/python-code-reference.md`, `docs/library-development.md` e `docs/architecture.md`) para refletir o novo formato da documentacao e a referencia de tipos.

### Notas

- Esta versao representa o estado atual apos a base `1.0.0`.

## [1.0.0] - 2026-03-31

Base de referencia informada: commit `91cf15dbb38964799b3c999f933f02ff0b83420b`.

### Adicoes

- Estrutura base da linguagem Instruc Lang com blocos `new def @load`, `new def @main` e `new def @quit`.
- Suporte a gerenciamento de stacks com comandos nativos: `new stack`, `use stack`, `end stack *`, `load` e `kill`.
- Sistema de carregamento e execução de bibliotecas por `req` e `call lib@metodo`.
- Biblioteca `std` com recursos de saída e depuração: `print`, `printf` e `snap`.
- Biblioteca `math` com operações na stack ativa: `opsum`, `opsub`, `opmul`, `opdiv`, `oppow` e `opmod`.
- Biblioteca `stacks` com recursos para `stack merge`, `stack load`, `stack call` e `stack run`.
- Biblioteca `str` com utilitarios de string: `str load`, `str loadstr`, `str loadint`, `str joinchars` e `str concat`.
- Biblioteca `comments` para ignorar comentarios em linha usando `#`.
- Biblioteca `label` para chamadas de labels via `call`.
- Biblioteca `basic` para injetar requisitos basicos (std, comments, str e label).
- Biblioteca `sayeachline` para impressao de cada linha processada.
- Conjunto inicial de documentacao em `docs/` cobrindo quickstart, referencia da linguagem, arquitetura, testes e desenvolvimento de bibliotecas.
- Suite inicial de exemplos e cenarios de teste em `test/`.

### Remocoes

- Nenhuma remoção nesta versão inicial.
