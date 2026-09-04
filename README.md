# ProcGuard

ProcGuard is a cross-platform process visibility tool for quick local inspection. It can display memory-heavy processes or take two snapshots and report what started and stopped between them.

## Features

* Windows and Linux/macOS process discovery
* No third-party runtime dependency
* Process start and stop detection
* Memory-oriented process ranking
* JSON output for other tools
* Read-only behavior

## Install

```bash
git clone https://github.com/meduuv/procguard.git
cd procguard
pip install -e .
```

## Examples

```bash
procguard
procguard --top 20
procguard --watch 5
procguard --watch 2 --json
```

ProcGuard does not terminate, inject into, or modify processes. It only reads operating-system process information.

## Development

```bash
python -m unittest discover -s tests -v
```

## Credits

Built by [meduuv](https://guns.lol/meduu).

## License

MIT
