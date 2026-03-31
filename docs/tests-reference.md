# Instruc Tests Reference

Este documento descreve o objetivo de cada arquivo em `test/`.

## Como executar um teste manualmente

Exemplo geral:

```bash
python main.py test/nome_do_teste.instruc
```

Com snapshot final:

```bash
python main.py test/nome_do_teste.instruc --debug
```

## Lista de testes

### test/helloworld.instruc

Objetivo:

- validar carga de `comments`, `std` e `str`
- validar `str concat` com literais
- validar `std@printf`

Fluxo principal:

- concatena `"Hello,"` e `" World!"` em `$`
- imprime primeiro item

Saida esperada:

```text
Hello, World!
```

### test/test1.instruc

Objetivo:

- exercitar sintaxe basica com comentarios inline
- validar `stack merge`
- validar `stack run` com `math@opsum`
- validar `stack run` com `std@print`

Fluxo principal:

- cria stacks `0`, `1`, `2`, `$`
- preenche `0` com `[1,2,3]`
- preenche `1` com `[11,12,13]`
- mescla `0` e `1` em `$`
- soma stack `1` e salva resultado em `2`
- imprime stack `2`

Saida esperada:

```text
36
```

### test/test_math_mul.instruc

Objetivo:

- validar `math@opmul` via `stack run`

Fluxo principal:

- stack `numbers = [2,3,4]`
- executa multiplicacao em `numbers`
- envia resultado para `$`
- imprime primeiro item

Saida esperada:

```text
24
```

### test/test_stack_call_opsum.instruc

Objetivo:

- validar `stack call` com metodo de biblioteca
- validar `stack load` para trazer resultado para stack atual

Fluxo principal:

- stack `data = [5,15,25]`
- executa `math@opsum` em `data`, salva em `result`
- carrega `result` em `$`
- imprime primeiro item

Saida esperada:

```text
45
```

### test/test_stack_kill.instruc

Objetivo:

- validar comando nativo `kill`

Fluxo principal:

- stack `$ = [10,20,30]`
- remove valor `20`
- imprime stack inteira

Saida esperada:

```text
10 30
```

### test/test_stack_merge.instruc

Objetivo:

- validar merge entre stacks com destino explicito

Fluxo principal:

- `left = [1,2]`
- `right = [3,4]`
- `stack merge left right > merged`
- `stack load merged`
- imprime stack atual

Saida esperada:

```text
1 2 3 4
```

### test/test_str_joinchars.instruc

Objetivo:

- validar montagem de string por caracteres
- validar `str joinchars`

Fluxo principal:

- carrega caracteres `I N S T R U C`
- une em uma string
- imprime primeiro item

Saida esperada:

```text
INSTRUC
```

### test/test_str_loadstr_concat.instruc

Objetivo:

- validar `str loadstr`
- validar `str concat` com literais
- validar impressao da stack completa

Fluxo principal:

- adiciona `"Linguagem"` na stack
- concatena `"Instruc " + "Lang"` e envia para `$`
- imprime stack inteira

Saida esperada:

```text
Linguagem Instruc Lang
```

### test/test_string_concat.instruc

Objetivo:

- validar caminho minimo de concatenacao de string

Fluxo principal:

- concatena `"Instruc" + " Lang"`
- imprime primeiro item

Saida esperada:

```text
Instruc Lang
```

## Cobertura atual dos testes

Coberto:

- operacoes base de stack (`load`, `kill`, `use`, `end`)
- bibliotecas `std`, `math`, `stacks`, `str`, `comments`
- chamadas indiretas (`stack call` e `stack run`)

Nao coberto explicitamente:

- `math@opdiv`, `math@oppow`, `math@opmod`, `math@opsub`
- comando `ret`
- casos de erro (lib ausente, metodo ausente, stack invalida)

Sugestao de expansao:

- adicionar arquivos `test_math_div.instruc`, `test_math_sub.instruc`
- adicionar cenarios de erro esperado para validar mensagens de excecao
