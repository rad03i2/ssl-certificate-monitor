# Contributing

Thanks for improving SSL Certificate Monitor.

1. Use Python 3.10+ and create a virtual environment.
2. Install development dependencies with `python -m pip install -e . pytest`.
3. Keep certificate verification secure by default; do not add silent verification bypasses.
4. Add or update deterministic tests for behavior changes.
5. Run `python -m compileall -q src tests` and `python -m pytest -q` before opening a pull request.
6. Keep changes focused and document user-visible behavior.

Please do not commit credentials, private certificates, private keys, production host inventories, or generated environments.

Author/maintainer: Radwan Abdulhadi Ahmed / @rad03i2.
