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

## Biblioteca std

- `call std@print`: imprime todos os elementos da stack ativa
- `call std@printf`: imprime apenas o primeiro elemento da stack ativa
- `call std@snap`: imprime snapshot completo do runner
- `print`: atalho de impressão registrado pela propria lib

## Biblioteca math

Todas as operacoes usam a stack ativa, limpam a stack e inserem o resultado:

- `call math@opsum`
- `call math@opsub`
- `call math@opmul`
- `call math@opdiv`
- `call math@oppow`
- `call math@opmod`

## Biblioteca stacks

### Mesclar stacks

```instruc
stack merge s1 s2
stack merge s1 s2 > s3
```

### Carregar stack dentro da stack atual

```instruc
stack load origem
```

### Rodar metodo em stack especifica

```instruc
stack call math@opsum as dados > resultado
```

### Rodar uma linha em stack especifica

```instruc
stack run call math@opsum as dados > resultado
```

## Biblioteca str

### Carregar caractere

```instruc
str load A
```

### Carregar string literal

```instruc
str loadstr "Texto"
```

### Carregar caractere por codigo inteiro

```instruc
str loadint 65
```

### Juntar itens da stack em uma string

```instruc
str joinchars
```

### Concatenar strings (literais ou stacks)

```instruc
str concat "Hello" " World" > $
str concat s1 s2 > s3
```

## Comentarios

Com `req comments`, tudo apos `#` na linha é ignorado.

Exemplo:

```instruc
load 10 # este trecho é comentario
```

## Labels

Com `req label`, você pode chamar labels como se fossem métodos, usando `call`.

```instruc
new def hello
    load "Hello, World!"
    call std@print
end def 
new def @main
    call hello
end def
```

## Biblioteca basic
Adiciona std, comments, str e label.

```instruc
req basic
```