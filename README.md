# Instruc Lang

Instruc Lang e uma linguagem de instrucao simples, criada como experimento para manipular listas e colecoes usando o conceito de stacks (pilhas).

O projeto foi desenvolvido para estudo e validacao de ideias de design de linguagem.

## Objetivo

A proposta da Instruc e oferecer uma sintaxe curta para:

- Criar e usar stacks
- Carregar valores numericos e strings
- Combinar colecoes
- Executar funcoes de bibliotecas em cima da stack atual

## Estrutura do projeto

- [main.py](main.py): ponto de entrada do interpretador
- [src](src): codigo-fonte do runtime, parser e bibliotecas
- [test](test): exemplos e arquivos de teste da linguagem
- [docs](docs): documentacao completa

## Como executar

Requisito:

- Python 3.11+ (recomendado)

Executar um arquivo .instruc:

```bash
python main.py test/helloworld.instruc
```

Executar com snapshot/debug do estado interno:

```bash
python main.py test/helloworld.instruc --debug
```

Se nenhum arquivo for passado, o projeto mostra o uso esperado.

## Exemplo minimo

```instruc
new def @load
    req comments
    req std
end def

new def @main
    new stack $
    use stack $
        load 10
        load 20
        call std@print
    end stack *
end def

new def @quit
end def
```

## Bibliotecas disponiveis

As bibliotecas agora possuem documentacao individual em [docs/libs/README.md](docs/libs/README.md).

- [basic](docs/libs/basic.md): atalho de setup (`req comments`, `req std`, `req str`, `req label`)
- [builtins](docs/libs/builtins.md): comandos base da linguagem (`new/use/end stack`, `load`, `kill`, `req`, `call`)
- [comments](docs/libs/comments.md): comentarios com `#`
- [epar](docs/libs/epar.md): comando de exemplo `epar <num>`
- [ireq](docs/libs/ireq.md): importacao de arquivo `.instruc` em runtime
- [label](docs/libs/label.md): chamada direta de labels com `call <label>`
- [math](docs/libs/math.md): operacoes numericas sobre a stack atual
- [read](docs/libs/read.md): leitura de entrada (`read str|int|float|bool`)
- [sayeachline](docs/libs/sayeachline.md): imprime cada linha executada (debug)
- [stacks](docs/libs/stacks.md): DSL para merge/load/call/run entre stacks
- [std](docs/libs/std.md): saida no terminal (`print`, `printf`, `snap`)
- [str](docs/libs/str.md): utilitarios de string (`load`, `loadstr`, `loadint`, `joinchars`, `concat`)

## Documentacao detalhada

- [docs/quickstart.md](docs/quickstart.md)
- [docs/language-reference.md](docs/language-reference.md)
- [docs/libs/README.md](docs/libs/README.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/python-code-reference.md](docs/python-code-reference.md)
- [docs/library-development.md](docs/library-development.md)
- [docs/types-protocols.md](docs/types-protocols.md) (referencia detalhada de simbolos e contratos de `src/types.py`)
- [docs/tests-reference.md](docs/tests-reference.md)

## Aviso

Este projeto e experimental e foi criado para aprendizado. A linguagem ainda esta evoluindo e pode ter comportamentos que mudem ao longo do tempo.
