import ast
import types
from pathlib import Path
from typing import Any, Dict


class _TypeCheckingStripper(ast.NodeTransformer):
    """
    Substitui 'if TYPE_CHECKING:' por 'if False:'
    """

    def visit_If(self, node: ast.If) -> ast.AST:
        # Detecta: if TYPE_CHECKING:
        if isinstance(node.test, ast.Name) and node.test.id == "TYPE_CHECKING":
            node.test = ast.Constant(value=False)
        return self.generic_visit(node)


def _load_module_from_code(code: str, filename: str) -> types.ModuleType:
    """Execute source code in an isolated module object."""
    module = types.ModuleType(filename)
    compiled = compile(code, filename, "exec")
    exec(compiled, module.__dict__)
    return module


def carregar_simbolos(path: Path) -> Dict[str, Any]:
    """
    Carrega um arquivo Python e retorna seus símbolos como dict.

    - Ignora blocos `if TYPE_CHECKING`
    - Não registra no sys.modules
    """
    codigo = path.read_text(encoding="utf-8")

    # Parse + transformação AST
    arvore = ast.parse(codigo, filename=str(path))
    arvore = _TypeCheckingStripper().visit(arvore)
    ast.fix_missing_locations(arvore)

    # Compilar AST transformada
    codigo_modificado = compile(arvore, str(path), "exec")

    # Criar módulo isolado
    module = types.ModuleType(path.stem)
    exec(codigo_modificado, module.__dict__)

    # Extrair símbolos (sem __dunder__)
    return {
        k: v
        for k, v in module.__dict__.items()
        if not k.startswith("__")
    }