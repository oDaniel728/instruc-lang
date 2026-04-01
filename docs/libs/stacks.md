# stacks

## Objetivo

Adicionar uma DSL para operacoes entre stacks com prefixo `stack`.

## Comandos

- `stack merge s1 s2`
- `stack merge s1 s2 > s3`
- `stack load s1`
- `stack call lib@metodo as s1 [> s2]`
- `stack run <linha_instruc> as s1 [> s2]`

## Exemplo em Instruc

```instruc
new def @load
    req std
    req math
    req stacks
end def

new def @main
    new stack $a
    new stack $b
    new stack $out

    use stack $a
        load 2
        load 3
    end stack *

    use stack $b
        load 4
        load 5
    end stack *

    stack merge $a $b > $out
    stack call math@opsum as $out > $a

    use stack $a
        print
    end stack *
end def
```

## Por baixo dos panos

- `__merge_kw_verif` junta stacks no destino ou in-place.
- `__load_kw_verif` copia elementos de uma stack para a stack ativa.
- `__call_kw_verif` troca stack ativa temporariamente, executa metodo e restaura a stack original.
- `__run_kw_verif` cria `CodeLine` dinamica e executa a linha no contexto de stack indicado.
- `_on_load` registra keywords em memoria (`stacks:*_keyword`) e adiciona os verificadores.

## Codigo fonte Python

```python
import re
from typing import TYPE_CHECKING as __TC__
import builtins as __builtins__

if __TC__:
    from ..types import RunnerAPIProtocol, CodeLineProtocol

__PREFIX = "stack";
__NAMESPACE = "stacks";
__PREXP = fr"{__PREFIX}\s+"

__merge_kw = "merge";

# stack merge <stack1> <stack2> > <stack3>
# stack merge <stack1> <stack2>
def __merge_kw_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    if not line.startswith(__PREFIX): return;
    stack_name = ctx.enum.SyntaxRulePatterns.STACK_NAME;

    if m:=re.match(
        fr"{__PREXP}{__merge_kw}\s+({stack_name})\s+({stack_name})\s*\>\s*({stack_name})", line
    ): # merge <stack1> <stack2> > <stack3>
        s1, s2, s3 = m.group(1), m.group(2), m.group(3);
        ctx.register_stack(s3);
        ctx.overwrite_stack(s3, [*ctx.get_stack(s1), *ctx.get_stack(s2)]);
        # print(f"merged {s1} and {s2} into {s3}");

    elif m:=re.match(
        fr"{__PREXP}{__merge_kw}\s+({stack_name})\s+({stack_name})", line
    ): # merge <stack1> <stack2> [> <stack3>]
        s1, s2 = m.group(1), m.group(2);
        ctx.get_stack(s1).extend(ctx.get_stack(s2));
        # print(f"merged {s2} into {s1}");

    return None;

__load_kw = "load";
# stack load <stack>
def __load_kw_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    if not line.startswith(__PREFIX): return;
    stack_name = ctx.enum.SyntaxRulePatterns.STACK_NAME;

    if m:=re.match(
        fr"{__PREXP}load\s+({stack_name})", line
    ):
        s = m.group(1);
        ctx.get_current_stack().extend(ctx.get_stack(s));
        # print(f"loaded stack {s}");

    return None;

__call_kw = "call";
# stack call <method> as <stack> (> stack)?
def __call_kw_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    if not line.startswith(__PREFIX): return;
    stack_name = ctx.enum.SyntaxRulePatterns.STACK_NAME;
    method_name = ".+";

    if m:=re.match(
        fr"{__PREXP}call\s+({method_name})\s+as\s+({stack_name})\s*(?:\>\s*({stack_name}))?", line
    ):
        # stack call <method> as <stack> (> stack)?
        method_id, s1, s2 = m.group(1), m.group(2), m.group(3);
        method = ctx.get_method(method_id);
        bak = ctx.get_current_stack_name();
        ctx.set_current_stack(s1);
        method(ctx);
        if s2 is not None:
            ctx.get_stack(s2).extend(ctx.get_current_stack());
        ctx.set_current_stack(bak);

    return None;

__run_kw = "run";
# stack run <line> as <stack_id> > <stack_output>
def __run_kw_verif(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
    line = cl.line;
    if not line.startswith(__PREFIX): return;
    stack_name = ctx.enum.SyntaxRulePatterns.STACK_NAME;
    if m:=re.match(
        fr"^{__PREXP}{__run_kw}\s+(.+)\s+as\s+({stack_name})\s*(?:\>\s*({stack_name}))?\s*$", line
    ):
        code_line, s1, s2 = m.group(1), m.group(2), m.group(3);
        cl = ctx.CodeLine(code_line);
        bak = ctx.get_current_stack_name();
        ctx.set_current_stack(s1);
        cl.execute(ctx);
        if s2 is not None:
            ctx.get_stack(s2).extend(ctx.get_current_stack());
        ctx.set_current_stack(bak);

    return None;

def _on_load(ctx: "RunnerAPIProtocol"):    
    ctx.register_memory(f"{__NAMESPACE}:merge_keyword", __merge_kw);
    ctx.register_memory(f"{__NAMESPACE}:load_keyword", __load_kw);
    ctx.register_memory(f"{__NAMESPACE}:call_keyword", __call_kw);
    ctx.register_memory(f"{__NAMESPACE}:run_keyword", __run_kw);

    ctx.add_syntax_verification(__merge_kw_verif);
    ctx.add_syntax_verification(__load_kw_verif);
    ctx.add_syntax_verification(__call_kw_verif);
    ctx.add_syntax_verification(__run_kw_verif);
```
