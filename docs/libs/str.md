# str

## Objetivo

Adicionar comandos de string com prefixo `str`.

## Comandos

- `str load <CHAR>`
- `str loadstr "STRING"`
- `str loadint <INT>`
- `str joinchars`
- `str concat ("a"|stack1) ("b"|stack2) [> stack3]`

## Exemplo em Instruc

```instruc
new def @load
    req std
    req str
end def

new def @main
    new stack $
    use stack $
        str load H
        str load i
        str joinchars
        call std@print

        str concat "Ola" " mundo" > $saida
    end stack *
end def
```

## Por baixo dos panos

- `__str_kw_verif` roteia para funcoes internas (`__load`, `__loadstr`, ...).
- `__quote` define o padrao de aspas usado por outras libs (ex.: `ireq`, `read`) via memoria `str:__quote`.
- `__concat` aceita modo literal e modo stack.

## Codigo fonte Python

```python
import re
from typing import TYPE_CHECKING as __TC__
import builtins as __builtins__

if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol

__str_kw = "str";

# str
def __str_kw_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    if not line.startswith(__str_kw): return;
    __load(cl, ctx);
    __loadstr(cl, ctx);
    __loadint(cl, ctx);
    __joinchars(cl, ctx);
    __concat(cl, ctx);    

__load_kw = "load";
# str load <CHAR>
def __load(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    if (m:=re.match(fr"{__str_kw}\s+{__load_kw}\s+(.)\s*", cl.line)):
        s = m.group(1);
        ctx.get_current_stack().append(s);

__loadstr_kw = "loadstr";
__quote = r"(?<!\\)\""
# str loadstr "STRING"
def __loadstr(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    if (m:=re.match(fr"{__str_kw}\s+{__loadstr_kw}\s+{__quote}(.*){__quote}\s*", cl.line)):
        s = m.group(1);
        ctx.get_current_stack().append(s);

__loadint_kw = "loadint";
# str loadint <INT>
def __loadint(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    if (m:=re.match(fr"{__str_kw}\s+{__loadint_kw}\s+(\d+)\s*", cl.line)):
        i = int(m.group(1));
        ctx.get_current_stack().append(chr(i));

__joinchars_kw = "joinchars";
# str joinchars
def __joinchars(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    if (m:=re.match(fr"{__str_kw}\s+{__joinchars_kw}\s*", cl.line)):
        s = "".join(ctx.get_current_stack());
        ctx.get_current_stack().clear();
        ctx.get_current_stack().append(s);

__concat_kw = "concat";
def __is_stack(s: str, pattern: str = r"\$\w+"):
    return re.match(pattern, s) is not None
# str concat ("str1"|<stack1>) ("str2"|<stack2>) [> <stack3>]
def __concat(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    stack_name = ctx.enum.SyntaxRulePatterns.STACK_NAME
    __string = fr"((?:{__quote}(.*){__quote})|{stack_name})";
    if (m:=re.match(fr"^{__str_kw}\s+{__concat_kw}\s+{__string}\s+{__string}(?:\s*>\s*({stack_name}))?\s*$", cl.line)):
        s1 = m.group(1);
        s2 = m.group(2);
        s3 = m.group(3);
        s4 = m.group(4);
        s5 = m.group(5);
        # print(m.groups());
        # print(f"s1: {s1}, s2: {s2}, s3: {s3}, s4: {s4}, s5: {s5}");
        stack_mode = (
            __is_stack(s1, stack_name) and __is_stack(s3, stack_name)
        )
        # stack_mode = __is_stack(s1, stack_name) and __is_stack(s2, stack_name);
        if stack_mode:
            s1 = ctx.get_stack(s1);
            s3 = ctx.get_stack(s3);
            s = [*s1, *s3];
        else:
            s = s2 + s4;
        
        if s5 is not None:
            if isinstance(s, list):
                ctx.get_stack(s5).extend(s);
            else:
                ctx.get_stack(s5).append(s);
        else:
            if isinstance(s, list):
                ctx.get_current_stack().extend(s);
            else:
                ctx.get_current_stack().append(s);

def _on_load(ctx: "RunnerAPIProtocol"):    
    ctx.register_memory("str:__quote", __quote);
    ctx.get_syntax_verifications().append(__str_kw_verif)
```
