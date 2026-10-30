"""Maps a dotted engine name to a callable.

Example: "physics.engines.vernier" -> core.physics.engines.vernier
"""

from importlib import import_module
from typing import Any, Callable


def get_engine(path: str) -> Callable[..., dict[str, Any]]:
    module_name, _, func_name = path.rpartition(".")
    if not module_name:
        raise ValueError(f"Engine path must be dotted, got: {path!r}")
    module = import_module(f"core.{module_name}")
    try:
        return getattr(module, func_name)
    except AttributeError as exc:
        raise AttributeError(f"{module_name} has no engine named {func_name!r}") from exc
