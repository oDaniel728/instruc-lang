# Language Reference

Referencia da sintaxe atual da Instruc Lang.

## Palavras-chave base

- `new`
- `use`
- `end`
- `def`
- `req`
- `stack`
- `load`
- `kill`
- `call`

## Labels especiais

- `@load`: inicializacao, geralmente para `req`
- `@main`: logica principal
- `@quit`: finalizacao

Definicao:

```instruc
new def @main
    # codigo
end def
```

## Requisitos (bibliotecas)

Sintaxe:

```instruc
req nome_da_lib
```

Exemplo:

```instruc
req std
req math
req stacks
req str
```

## Operacoes de stack nativas

### Criar stack

```instruc
new stack nome
```

### Selecionar stack ativa

```instruc
use stack nome
```

### Encerrar contexto de stack

```instruc
end stack *
```

### Carregar numero inteiro

```instruc
load 123
```

### Remover valor da stack ativa

```instruc
kill 123
```

## Chamada de metodo

Sintaxe:

```instruc
call lib@metodo
```

Exemplo:

```instruc
call std@print
```

## Bibliotecas

A referencia detalhada de cada biblioteca agora esta separada por arquivo:

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