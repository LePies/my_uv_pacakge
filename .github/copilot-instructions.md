# Copilot instructions for my_uv_pacakge

## Project context
- Python package managed with `uv` (`pyproject.toml` + `uv.lock`).
- Main package: `my_uv_pacakge/`, with subpackages in `my_uv_pacakge/subpackages/`
  (currently `barber`, `opt`).
- Docs are built with Read the Docs (see `.readthedocs.yaml` and `docs/`).

## Documentation standard
All docstrings must follow **Google style**:

- Every module, class, and public method/function gets a docstring.
- A docstring starts with a one-line summary in the imperative mood,
  ending with a period. No "TODO" or placeholder text.
- Public functions/methods document `Args`, `Returns`, and `Raises`
  sections where applicable, matching the actual signature (names,
  types, and defaults).
- Type hints in the signature and types in the docstring must agree.
- Do not document private attributes or internal helpers beyond a
  one-line summary.

## Code quality notes
- Prefer explicit, correctly spelled identifiers (watch out for
  historic typos such as `mustahce` / `_mustache_lengt` — do not
  replicate them in new docs, flag them instead).
- Keep `__all__` in every package `__init__.py` consistent with what
  is actually imported/exported.
- Issues about documentation use the `documentation` label.
