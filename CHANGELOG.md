# Changelog

Todas as mudancas relevantes deste projeto serão documentadas neste arquivo.

## [1.0.0] - 2026-03-31

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
