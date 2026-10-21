# my_uv_pacakge

A test playground for a **uv workspace** monorepo: one core package
plus subpackages that depend on it, managed with a single `uv.lock`.

## Layout

```
my_uv_pacakge/
├── my_uv_pacakge/          # core package — mustaches (color, length, growing)
├── packages/
│   └── barber/             # subpackage — barbers who trim mustaches
└── dev/                    # repo maintenance tooling (never published)
```

- **my-uv-pacakge** (import: `my_uv_pacakge`) — the core.
- **barber** (import: `barber`) — workspace member, depends on the core.

## Quickstart (development)

```bash
git clone https://github.com/LePies/my_uv_pacakge.git
cd my_uv_pacakge

uv sync --all-packages      # core + all subpackages, one venv, one lockfile
uv run pytest               # tests across the workspace
```

Run an example:

```python
import my_uv_pacakge as muv
from barber import Barber

m = muv.Mustache()
print(m.get_mustache_length())   # 10 — "just right!"

b = Barber("Felix", 40, 100)
b.trim_mustache(m)               # trims 5 units
```

## Using the packages from outside (no clone)

```bash
uv add "my-uv-pacakge @ git+https://github.com/LePies/my_uv_pacakge.git"
uv add "barber @ git+https://github.com/LePies/my_uv_pacakge.git#subdirectory=packages/barber"
```

Plain pip works too:

```bash
pip install "my-uv-pacakge @ git+https://github.com/LePies/my_uv_pacakge.git"
```

## Adding a new subpackage

Subpackages live in `packages/<name>/` and must:

1. Depend on the core: `dependencies = ["my-uv-pacakge"]`
2. Resolve the core from the workspace:
   ```toml
   [tool.uv.sources]
   my-uv-pacakge = { workspace = true }
   ```
3. Declare the flat layout (uv_build defaults to `src/`):
   ```toml
   [tool.uv.build-backend]
   module-root = ""
   ```

Then `uv sync --all-packages` picks it up via `members = ["packages/*"]`.

## Tooling

This repo uses three tools from the modern Python toolchain, all configured in
`pyproject.toml` — no separate config files, no `requirements.txt`.

- **uv** — environment, dependencies, workspace (`uv.lock` committed)
- **ruff** — linter + formatter
- **ty** — type checker
- **uv_build** — build backend for all packages

### uv — project & environment manager

uv is a single fast executable (written in Rust) that replaces pip, pip-tools,
virtualenv, pipx, and poetry. It manages everything through `pyproject.toml` and
one committed lockfile (`uv.lock`), so every machine gets identical environments.
It also understands **workspaces**: one repo, multiple packages, one lockfile,
one virtualenv — subpackages link to each other locally via
`[tool.uv.sources] ... { workspace = true }`.

```bash
uv run script.py           # or uv run python script.py ... but python script.py doesn't work unless you have used pip to install
uv sync --all-packages     # create/update .venv from uv.lock (all packages)
uv add scipy               # add a dependency
uv run pytest              # run anything inside the project env
uv lock --upgrade          # bump locked versions
```

### ruff — linter & formatter

ruff replaces flake8, isort, pyupgrade, and black in one tool — orders of
magnitude faster, so it can run (and auto-fix) on every save and every PR.
Rules are selected in `pyproject.toml`; the common baseline is `E` (pycodestyle
errors) and `F` (pyflakes), tightened stepwise with `I` (import sorting), `UP`
(pyupgrade), `B` (bugbear), and `D` (docstrings, e.g. NumPy convention).

```bash
uv run ruff check .        # lint
uv run ruff check --fix .  # lint + auto-fix
uv run ruff format .       # format (black-compatible)
```

### ty — type checker

ty is a type checker from Astral (the ruff team). It verifies type
annotations statically — catching bugs like wrong argument types or missing
attributes before runtime, without the friction older checkers are known for.
The `uv_build` backend pairs with it, since it validates package layout at
build time.

```bash
uv run ty check            # type-check nest + tests (see [tool.ty.src])
```

Requires Python >= 3.14.
