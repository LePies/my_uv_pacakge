---
description: Audit all docstrings and create GitHub issues for problems found
---

Audit the documentation of this repository and file issues for what you find.

## Scope
Go through **every** Python file in `my_uv_pacakge/`, including all
subpackages under `my_uv_pacakge/subpackages/`. For each module, class,
and public method/function, check:

1. **Missing docstrings** — no docstring at all.
2. **Incorrect docstrings** — wrong parameter names, mismatched types,
   docstring disagrees with the implementation, or literal
   placeholders like `TODO`.
3. **Unclear docstrings** — vague, misleading, misspelled, or too
   terse to be useful to a new contributor.

Use the documentation standard in `.github/copilot-instructions.md`
(Google style) as the reference for what "correct" means.

## Output
For **each distinct finding**, create a separate GitHub issue with:

- A title starting with `[docs]:` and naming the file/symbol
  (e.g. `[docs]: barber.Barber.trim_mustache has no docstring`).
- The file path and line number.
- A short quote of the offending code or docstring.
- Why it is missing, incorrect, or hard to understand.
- A suggested improved docstring in Google style.

Group trivial findings for the same file into one issue rather than
creating noise. Apply the `documentation` label to every issue you
create. Show me the list of proposed issues before creating them.
