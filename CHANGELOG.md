# Changelog

Todas as mudancas relevantes deste projeto serão documentadas neste arquivo.

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
