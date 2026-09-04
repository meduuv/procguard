# Contributing

Contributions are welcome when they improve correctness, portability, documentation or test coverage.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
python -m unittest discover -s tests -v
```

On Windows, activate the environment with `.venv\Scripts\activate`.

## Pull requests

Keep changes focused and include tests for behavior changes. Platform-specific changes should document which operating systems were tested.

ProcGuard is intentionally read-only. Features that terminate, inject into, suspend or alter processes are outside the scope of this project.

## Reporting issues

Avoid posting private process names, command lines or environment details that may contain secrets.
