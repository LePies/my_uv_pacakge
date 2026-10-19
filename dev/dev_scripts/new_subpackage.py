"""Scaffold a new subpackage inside the core distribution.

Usage:
    uv run new-subpackage <name> [attr1 attr2 ...]

Creates my_uv_pacakge/subpackages/<name>/ with a correct __init__.py and
module file, and updates the managed alias block in the core __init__.py so
both `import my_uv_pacakge as muv; muv.<name>` and
`from my_uv_pacakge.<name> import <Class>` work.

Optional extra arguments are public names to re-export (defaults to the
capitalized name, e.g. `new-subpackage shave` re-exports `Shave`).
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # repo root
CORE_NAME = "my_uv_pacakge"
SUBPACKAGES_DIR = ROOT / CORE_NAME / "subpackages"
CORE_INIT = ROOT / CORE_NAME / "__init__.py"

# --- managed alias block in the core __init__.py ---------------------------

BLOCK_START = "# --- subpackage aliases (managed by dev/new_subpackage.py) ---"
BLOCK_END = "# --- end managed block ---"

# {aliases} is a repr'd dict: {'barber': ('barber',)}
BLOCK_TEMPLATE = '''{start}

import importlib
import sys

for _name, _module in {aliases}.items():
    _mod = importlib.import_module(f"{{CORE_NAME}}.{{_module}}")
    sys.modules[f"{{CORE_NAME}}.{{_name}}"] = _mod
    globals()[_name] = _mod

{end}
'''

INIT_TEMPLATE = '''"""Subpackage: {name}."""

from .{module} import {exports}


__all__ = {all_list}
'''

MODULE_TEMPLATE = '''"""Implementation of the {name} subpackage."""

import {CORE_NAME} as muv


class {main_class}:
    """TODO: describe what {main_class} does."""

    def __init__(self) -> None:
        pass


__all__ = ["{main_class}"]
'''


def slug(name: str) -> str:
    return name.strip().lower().replace("-", "_")


def update_core_init(name: str, module: str) -> None:
    """Refresh the managed alias block, registering subpackage `name`."""
    if not CORE_INIT.exists():
        sys.exit(f"Core __init__ not found at {CORE_INIT}")

    text = CORE_INIT.read_text()

    # registry = every subpackage currently on disk (covers pre-existing ones)
    registered: dict[str, str] = {}
    if SUBPACKAGES_DIR.is_dir():
        for p in sorted(SUBPACKAGES_DIR.iterdir()):
            if p.is_dir() and (p / "__init__.py").is_file():
                registered[p.name] = p.name
    registered[name] = module  # no-op if already present

    # drop any previously managed block
    if BLOCK_START in text:
        text = re.sub(
            re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END) + r"\n*",
            "",
            text,
            flags=re.DOTALL,
        )

    block = BLOCK_TEMPLATE.format(
        start=BLOCK_START,
        end=BLOCK_END,
        aliases=repr(registered),
    )

    # insert the block after the last import line, keep __all__ updated at end
    text = text.rstrip() + "\n\n" + block.rstrip() + "\n"

    # keep __all__ in sync with registered subpackages
    public = sorted(set(registered) | {"Mustache"})
    text = re.sub(r"__all__ = \[.*?\]", "__all__ = " + repr(public), text, flags=re.DOTALL)

    CORE_INIT.write_text(text)
    print(f"Core aliases refreshed: {', '.join(sorted(registered))}")


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: uv run new-subpackage <name> [attr1 attr2 ...]")

    name = slug(sys.argv[1])
    pkg_dir = SUBPACKAGES_DIR / name
    module = name

    if pkg_dir.exists():
        sys.exit(f"{pkg_dir} already exists")

    # public names to re-export; default = CamelCase of the package name
    exports = sys.argv[2:] or ["".join(p.capitalize() for p in name.split("_"))]

    pkg_dir.mkdir(parents=True)
    (pkg_dir / f"{module}.py").write_text(
        MODULE_TEMPLATE.format(name=name, CORE_NAME=CORE_NAME, main_class=exports[0])
    )
    (pkg_dir / "__init__.py").write_text(
        INIT_TEMPLATE.format(
            name=name,
            module=module,
            exports=", ".join(f"{e} as {e}" for e in exports),
            all_list=repr(exports),
        )
    )
    (pkg_dir / "README.md").write_text(
        f"# {name}\n\n"
        f"Subpackage of `my-uv-pacakge`. Access via:\n\n"
        f"```python\n"
        f"import my_uv_pacakge as muv\n"
        f"from my_uv_pacakge.{name} import {exports[0]}\n"
        f"```\n"
    )

    update_core_init(name, module)

    print(f"Created {pkg_dir}")
    print(f"Public names: {', '.join(exports)}")


if __name__ == "__main__":
    main()
