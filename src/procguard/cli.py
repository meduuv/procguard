import argparse
import json
import time
from dataclasses import asdict

from .core import diff, snapshot, top_memory


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="procguard",
        description="Inspect local processes and watch for starts or stops.",
    )
    parser.add_argument(
        "-w",
        "--watch",
        type=float,
        default=0.0,
        help="Take a second snapshot after this many seconds",
    )
    parser.add_argument(
        "-n",
        "--top",
        type=int,
        default=10,
        help="Number of memory-heavy processes to display",
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        dest="json_output",
        help="Print machine-readable JSON",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    before = snapshot()

    if args.watch > 0:
        time.sleep(args.watch)
        changes = diff(before, snapshot())
        payload = {
            key: [asdict(process) for process in processes]
            for key, processes in changes.items()
        }
    else:
        payload = {
            "processes": [
                asdict(process)
                for process in top_memory(before, args.top)
            ]
        }

    if args.json_output:
        print(json.dumps(payload, indent=2))
        return

    if "processes" in payload:
        print("PID      MEMORY(KB)  NAME")
        for process in payload["processes"]:
            memory = process["memory_kb"] if process["memory_kb"] is not None else ""
            print(f"{process['pid']:<8} {str(memory):<11} {process['name']}")
        return

    for label in ("started", "stopped"):
        print(f"{label.capitalize()}:")
        items = payload[label]
        if not items:
            print("  none")
            continue
        for process in items:
            print(f"  {process['pid']} {process['name']}")


if __name__ == "__main__":
    main()
