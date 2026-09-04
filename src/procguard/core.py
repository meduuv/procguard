from __future__ import annotations

import csv
import io
import os
import subprocess
from dataclasses import dataclass


@dataclass(slots=True)
class Process:
    pid: int
    name: str
    memory_kb: int | None = None


def _windows_snapshot() -> list[Process]:
    result = subprocess.run(
        ["tasklist", "/FO", "CSV", "/NH"],
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
        errors="replace",
    )
    processes: list[Process] = []
    for row in csv.reader(io.StringIO(result.stdout)):
        if len(row) < 5:
            continue
        try:
            pid = int(row[1])
        except ValueError:
            continue
        digits = "".join(char for char in row[4] if char.isdigit())
        memory_kb = int(digits) if digits else None
        processes.append(Process(pid=pid, name=row[0], memory_kb=memory_kb))
    return processes


def _posix_snapshot() -> list[Process]:
    result = subprocess.run(
        ["ps", "-eo", "pid=,comm=,rss="],
        capture_output=True,
        text=True,
        check=True,
    )
    processes: list[Process] = []
    for line in result.stdout.splitlines():
        parts = line.strip().split(None, 2)
        if len(parts) < 2:
            continue
        try:
            pid = int(parts[0])
            memory_kb = int(parts[2]) if len(parts) == 3 else None
        except ValueError:
            continue
        processes.append(Process(pid=pid, name=parts[1], memory_kb=memory_kb))
    return processes


def snapshot() -> list[Process]:
    """Return a point-in-time process snapshot for the current machine."""
    return _windows_snapshot() if os.name == "nt" else _posix_snapshot()


def diff(before: list[Process], after: list[Process]) -> dict[str, list[Process]]:
    """Return processes that appeared or disappeared between snapshots."""
    old = {process.pid: process for process in before}
    new = {process.pid: process for process in after}
    return {
        "started": [new[pid] for pid in sorted(new.keys() - old.keys())],
        "stopped": [old[pid] for pid in sorted(old.keys() - new.keys())],
    }


def top_memory(processes: list[Process], limit: int = 10) -> list[Process]:
    if limit < 0:
        raise ValueError("limit must be zero or greater")
    return sorted(
        processes,
        key=lambda process: process.memory_kb if process.memory_kb is not None else -1,
        reverse=True,
    )[:limit]
