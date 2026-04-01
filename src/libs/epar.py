# BIBLIOTECA DE EXEMPLO
# verifica se um número é par ou impar

# importa regex
import re 

# importa o tipo de verificação de 
# tipo para evitar importações circulares
from typing import TYPE_CHECKING as __TC__;

# importa builtins para evitar conflitos de nomes
import builtins as __builtins__;

# importa os tipos necessários para a verificação 
# de tipo
if __TC__:

    # define a função de carregamento da biblioteca, 
    # que é chamada quando a biblioteca é carregada
    from ..types import RunnerAPIProtocol, CodeLineProtocol;

# função de carregamento da biblioteca, 
# que é chamada quando a biblioteca é carregada
def _on_load(ctx: "RunnerAPIProtocol"):
    # adiciona a função de verificação de sintaxe 
    # para a palavra-chave "epar"
    @ctx.add_syntax_verification
    def epar(cl: "CodeLineProtocol", ctx: "RunnerAPIProtocol"):
        # obtém a linha de código
        line = cl.line

        # epar <num>
        # verifica se a linha de código corresponde 
        # ao formato esperado
        if m:=re.match(
            fr"epar\s+(\d+)", line
        ):
            # obtém o número da linha de código
            num = int(m.group(1))
            
            # imprime se o número é par ou impar
            print(f"{num} é {"par" if num % 2 == 0 else "impar"}.")