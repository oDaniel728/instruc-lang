# epar

## Objetivo

Biblioteca de exemplo que adiciona o comando `epar <num>` para imprimir se um numero e par ou impar.

## Comando

- `epar <num>`

## Exemplo em Instruc

```instruc
new def @load
    req epar
end def

new def @main
    epar 10
    epar 7
end def
```

## Por baixo dos panos

- No `_on_load`, a biblioteca registra um verificador com decorator `@ctx.add_syntax_verification`.
- O verificador faz `re.match(fr"epar\s+(\d+)", line)`.
- O numero e convertido para `int` e impresso com `print`.

## Codigo fonte Python

```python
# BIBLIOTECA DE EXEMPLO
# verifica se um numero e par ou impar

# importa regex
import re 

# importa o tipo de verificacao de 
# tipo para evitar importacoes circulares
from typing import TYPE_CHECKING as __TC__;

# importa builtins para evitar conflitos de nomes
import builtins as __builtins__;

# importa os tipos necessarios para a verificacao 
# de tipo
if __TC__:

    # define a funcao de carregamento da biblioteca, 
    # que e chamada quando a biblioteca e carregada
    from ..types import RunnerAPIProtocol, CodeLineProtocol;

# funcao de carregamento da biblioteca, 
# que e chamada quando a biblioteca e carregada
def _on_load(ctx: "RunnerAPIProtocol"):
    # adiciona a funcao de verificacao de sintaxe 
    # para a palavra-chave "epar"
    @ctx.add_syntax_verification
    def epar(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
        # obtem a linha de codigo
        line = cl.line

        # epar <num>
        # verifica se a linha de codigo corresponde 
        # ao formato esperado
        if m:=re.match(
            fr"epar\s+(\d+)", line
        ):
            # obtem o numero da linha de codigo
            num = int(m.group(1))
            
            # imprime se o numero e par ou impar
            print(f"{num} e {"par" if num % 2 == 0 else "impar"}.")
```
