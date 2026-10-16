"""Scaffold a new workspace subpackage.

Usage: uv run python scripts/new_subpackage.py my-new-tool
"""

import sys
from pathlib import Path

TEMPLATE = '''[project]
name = "{name}"
version = "0.1.0"
description = "NEST subpackage: {name}"
readme = "README.md"
requires-python = ">=3.10"
dependencies = ["my-uv-pacakge"]          # core dependency

[build-system]
requires = ["uv_build>=0.12.21,<0.13.0"]
build-backend = "uv_build"

[tool.uv.build-backend]
module-root = ""                          # flat layout

[tool.uv.sources]
my-uv-pacakge = {{ workspace = true }}    # resolve core from this repo, not PyPI
'''


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: uv run python scripts/new_subpackage.py <name>")

    name = sys.argv[1].strip().lower().replace("-", "_")
    dist_name = name.replace("_", "-")
    pkg_dir = Path("packages") / dist_name
    mod_dir = pkg_dir / name

    if pkg_dir.exists():
        sys.exit(f"{pkg_dir} already exists")

    (mod_dir).mkdir(parents=True)
    (mod_dir / "__init__.py").write_text(
        f'"""NEST subpackage: {name}."""\n\n__all__: list[str] = []\n'
    )
    (pkg_dir / "pyproject.toml").write_text(
        TEMPLATE.format(name=dist_name)
    )
    (pkg_dir / "README.md").write_text(f"# {dist_name}\n")

    tests = pkg_dir / "tests"
    tests.mkdir()
    (tests / "test_import.py").write_text(
        f"def test_import():\n    import {name}\n"
    )

    print(f"Created {pkg_dir}")
    print(f"Next: add '{dist_name}' to [tool.uv.workspace] members or use 'packages/*', "
          f"then run: uv sync --all-packages")


if __name__ == "__main__":
    main()
