"""Scaffold a new subpackage inside the core distribution.

Usage:
    uv run new-subpackage <name> [attr1 attr2 ...]

Creates my_uv_pacakge/subpackages/<name>/ and rewrites the core
__init__.py's alias section (everything between the managed markers),
adding one alias block per subpackage:

    import my_uv_pacakge.subpackages.<name> as _<name>
    sys.modules["my_uv_pacakge.<name>"] = _<name>
    <name> = _<name>

Optional extra arguments are public names to re-export from the
subpackage __init__ (default: capitalized name, e.g. `new-subpackage opt`
re-exports `Opt`).
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # repo root
CORE_NAME = "my_uv_pacakge"
SUBPACKAGES_DIR = ROOT / CORE_NAME / "subpackages"
CORE_INIT = ROOT / CORE_NAME / "__init__.py"

# --- managed section in the core __init__.py -------------------------------

BLOCK_START = "# --- subpackage aliases (managed by dev/new_subpackage.py) ---"
BLOCK_END = "# --- end managed block ---"

INIT_TEMPLATE = '''"""Subpackage: {name}."""

from .{module} import {exports}


__all__ = {all_list}
'''

MODULE_TEMPLATE = '''"""Implementation of the {name} subpackage."""

import my_uv_pacakge as muv


class {main_class}:
    """TODO: describe what {main_class} does."""

    def __init__(self) -> None:
        pass


__all__ = ["{main_class}"]
'''


def slug(name: str) -> str:
    return name.strip().lower().replace("-", "_")


def update_core_init() -> None:
    """Rewrite the managed alias section: one import+alias per subpackage."""
    if not CORE_INIT.exists():
        sys.exit(f"Core __init__ not found at {CORE_INIT}")

    text = CORE_INIT.read_text()

    # registry = every subpackage on disk (covers pre-existing ones)
    names: set[str] = set()
    if SUBPACKAGES_DIR.is_dir():
        for p in sorted(SUBPACKAGES_DIR.iterdir()):
            if p.is_dir() and (p / "__init__.py").is_file():
                names.add(p.name)

    # build the new managed section
    lines = [BLOCK_START, "", "import sys", ""]
    for n in sorted(names):
        lines.append(f"import {CORE_NAME}.subpackages.{n} as _{n}")
    lines.append("")
    for n in sorted(names):
        lines.append(f'sys.modules["{CORE_NAME}.{n}"] = _{n}')
        lines.append(f"{n} = _{n}")
    lines.append("")
    lines.append(BLOCK_END)
    block = "\n".join(lines)

    # replace or append the managed section
    if BLOCK_START in text:
        text = re.sub(
            re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END),
            block,
            text,
            flags=re.DOTALL,
        )
    else:
        text = text.rstrip() + "\n\n" + block + "\n"

    # drop the old manual alias ceremony if present (superseded by the block)
    text = re.sub(
        r"import sys\n\n# alias my_uv_pacakge\.barber.*?\nbarber = _barber\n",
        "",
        text,
        flags=re.DOTALL,
    )

    # make sure the core's own import is at the top (before the aliases,
    # otherwise subpackages annotating with muv.Mustache hit a circular import)
    mustache_import = f"from {CORE_NAME}.mustache import Mustache as Mustache\n"
    text = text.replace(mustache_import, "")
    text = mustache_import + text

    # keep __all__ in sync: Mustache + every subpackage
    public = ["Mustache"] + sorted(names)
    text = re.sub(
        r"__all__ = \[.*?\]",
        "__all__ = " + repr(public),
        text,
        flags=re.DOTALL,
    )

    CORE_INIT.write_text(text)
    print(f"Core __init__ updated; aliases: {', '.join(sorted(names))}")


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: uv run new-subpackage <name> [attr1 attr2 ...]")

    name = slug(sys.argv[1])
    pkg_dir = SUBPACKAGES_DIR / name

    if pkg_dir.exists():
        sys.exit(f"{pkg_dir} already exists")

    # public names to re-export; default = CamelCase of the package name
    exports = sys.argv[2:] or ["".join(p.capitalize() for p in name.split("_"))]

    pkg_dir.mkdir(parents=True)
    (pkg_dir / f"{name}.py").write_text(
        MODULE_TEMPLATE.format(name=name, main_class=exports[0])
    )
    (pkg_dir / "__init__.py").write_text(
        INIT_TEMPLATE.format(
            name=name,
            module=name,
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

    update_core_init()

    print(f"Created {pkg_dir}")
    print(f"Public names: {', '.join(exports)}")


if __name__ == "__main__":
    main()
