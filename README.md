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

- `std`: saida no terminal (`print`, `printf`, `snap`)
- `math`: operacoes com numeros na stack atual (`opsum`, `opsub`, `opmul`, `opdiv`, `oppow`, `opmod`)
- `stacks`: utilitarios para combinar e executar operacoes entre stacks
- `str`: utilitarios para strings e caracteres
- `comments`: suporte a comentarios com `#`
- `basic`: injeta requisitos basicos
- `sayeachline`: imprime cada linha processada

## Documentacao detalhada

- [docs/quickstart.md](docs/quickstart.md)
- [docs/language-reference.md](docs/language-reference.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/python-code-reference.md](docs/python-code-reference.md)
- [docs/tests-reference.md](docs/tests-reference.md)

## Aviso

Este projeto e experimental e foi criado para aprendizado. A linguagem ainda esta evoluindo e pode ter comportamentos que mudem ao longo do tempo.
