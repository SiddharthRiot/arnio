Updating the C++ extension type stubs
===================================

This project exposes a C++ extension `_arnio_cpp` via pybind11. To provide
typing, autocompletion, and mypy support we keep a handwritten stub file at
`arnio/_arnio_cpp.pyi`.

When the C++ API changes, update the stub following these minimal steps:

1. Inspect the public C++ bindings (see `bindings/` and `cpp/include/arnio/`).
2. Update `arnio/_arnio_cpp.pyi` to match the public API:
   - Add or remove classes, functions, and module-level names.
   - Keep method names, parameter names, and return types aligned with usage in Python.
   - Prefer Python-friendly types: `dict[str, str]`, `list[str]`, `Optional[...]`, `numpy.ndarray` for array returns.
3. Run the local type check to validate signatures:

```bash
python -m pip install --user -U mypy
python -m mypy arnio --show-error-codes
```

4. Fix any mypy errors either by adjusting the stub or, when appropriate,
   by tightening Python call sites.

5. Add a brief note in the PR describing what changed in the C++ API and why
   the stub was updated.

Quick tips
- If a native class exposes simple constants (enums), declare them as
  class attributes on the corresponding stub type (e.g. `DType.INT64`).
- If a C++ function expects arguments in a particular order or type, reflect
  that exactly; Python call-sites rely on those signatures for mypy checks.
- When in doubt, run `mypy arnio` and follow its errors — they point to
  mismatches between usage and stub declarations.

CI
--
We recommend adding a CI job that runs `python -m mypy arnio` on PRs so
stubs remain in sync. If you'd like, I can add a GitHub Actions workflow that
runs mypy on pushes and PRs.

Contact
-------
If you need help reconciling a complex binding (overloads, buffers, or
callbacks), open a draft PR and ping the maintainers on the PR or in the
project Discord — we'll review the stub changes and suggest precise types.
