# Quickstart

Este guia mostra o minimo para comecar a usar a Instruc Lang.

## 1. Execute o projeto

Na raiz do repositorio:

```bash
python main.py test/helloworld.instruc
```

Para ver o estado interno de stacks, labels, memoria e libs no fim da execucao:

```bash
python main.py test/helloworld.instruc --debug
```

## 2. Entenda os 3 blocos principais

Todo programa geralmente possui:

- `@load`: carrega bibliotecas
- `@main`: logica principal
- `@quit`: finalizacao

Exemplo:

```instruc
new def @load
    req comments
    req std
end def

new def @main
    new stack $
    use stack $
        load 1
        load 2
        call std@print
    end stack *
end def

new def @quit
end def
```

## 3. Crie sua primeira stack

```instruc
new stack numeros
use stack numeros
    load 10
    load 20
end stack *
```

## 4. Trabalhe com bibliotecas

Carregue no `@load`:

```instruc
req std
req math
req stacks
req str
```

Use no `@main`:

```instruc
call std@print
call math@opsum
```

## 5. Consulte exemplos prontos

A pasta [test](../test) contem cenarios reais para referencia:

- [test/helloworld.instruc](../test/helloworld.instruc)
- [test/test1.instruc](../test/test1.instruc)
- [test/test_stack_merge.instruc](../test/test_stack_merge.instruc)
- [test/test_string_concat.instruc](../test/test_string_concat.instruc)

Para descricao completa dos cenarios e saidas esperadas, veja:

- [docs/tests-reference.md](tests-reference.md)
