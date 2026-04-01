# read

## Objetivo

Ler entrada do usuario em runtime e empilhar o valor convertido.

## Dependencia

- exige que `str` ja esteja carregada (`req str`), pois usa a memoria `str:__quote`

## Comando

- `read (str|int|float|bool) ["PROMPT"] [> stack]`

## Exemplo em Instruc

```instruc
new def @load
    req str
    req read
    req std
end def

new def @main
    new stack $
    use stack $
        read int "Digite um numero: "
        print
        read bool "Continuar? " > $flags
    end stack *
end def
```

## Por baixo dos panos

- O verificador parseia tipo, prompt opcional e stack de destino opcional.
- Chama `input(prompt)`.
- Faz cast para `int`, `float` ou `bool` conforme tipo.
- Se houver `> stack`, insere nessa stack; senao, fica na stack atual.

## Codigo fonte Python

```python
import re
from typing import TYPE_CHECKING as __TC__, Optional;
import builtins as __builtins__

from pathlib import Path
from typing_extensions import Literal;
if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol;

def _on_load(ctx: "RunnerAPIProtocol"):
    if not ctx.has_lib("str"): raise Exception("Library 'str' is required for 'input' to work. Please load it before using 'input'.");
    __kw = r"read";
    __quote = ctx.get_memory("str:__quote", None);
    # input (str|int|float|bool) ["PROMPT"] [> <stack>]
    __options_1 = r"(str|int|float|bool)";
    __string = fr"(?:{__quote}(.*){__quote})";
    __stack_insert = fr"\s*>\s*({ctx.enum.SyntaxRulePatterns.STACK_NAME})";
    __import_format = fr"^{__kw}\s+{__options_1}(?:\s+{__string})?(?:\s+{__stack_insert})?\s*$";
    @ctx.add_syntax_verification
    def __input_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
        if m:=re.match(__import_format, cl.line):
            type_: Literal["str", "int", "float", "bool"] = m.group(1); # type: ignore
            prompt: str = m.group(2) or "";
            stack_name: Optional[str] = m.group(3);
            value = input(prompt);
            if type_ == "int":
                value = int(value);
            elif type_ == "float":
                value = float(value);
            elif type_ == "bool":
                value = value.lower() in ("true", "1", "yes", "y");
            
            if stack_name:
                ctx.get_stack(stack_name).append(value);
    
```
