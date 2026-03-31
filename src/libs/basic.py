import re
from typing import TYPE_CHECKING as __TC__
import builtins as __builtins__

if __TC__:
    from ..types import RunnerAPIProtocol
def _on_load(ctx: "RunnerAPIProtocol"):    
    ctx.inject_code([
        "req comments",
        "req std",
        "req str",
        "req label"
    ], "@load")