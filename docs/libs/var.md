# var

## Objetivo

Adicionar comandos de variaveis com prefixo `var`.

## Comandos

- `var (int|float|str|boolean) <name> <value>`
- `var get <name>`
- `var set <name> <value>`

## `var (...) <name> <value>`
- Cria uma variavel de memoria com o nome e valor especificados. O tipo da variavel e inferido a partir do valor, mas deve ser declarado para validacao. 

Ex.: `var int foo 3` cria uma variavel `foo` do tipo `int` com valor `3`.

## `var get <name>`
- Recupera o valor da variavel de memoria especificada e o empilha. 

Ex.: `var get foo` empilha o valor de `foo` na stack. 

Ex.: `var get foo` empilha o valor de `foo` na stack. 

Ex.: `var get instruc:_line` empilha a linha atual de execucao (string) na stack.

## `var set <name> <value>`
- Atualiza o valor da variavel de memoria especificada. O tipo do novo valor deve ser compatível com o tipo declarado da variavel.

Ex: `var set foo 5` atualiza o valor de `foo` para `5`, desde que `foo` seja do tipo `int`.

## Exemplo em Instruc

```instruc
new def @load
    req std
    req var
    req comments
end def

new def @main
    new stack $
    use stack $
        var int foo 3   # (int) foo = 3
        var get foo     # push foo (3) na stack
        call std@print  # imprime 3
    end stack *
end def
```