"""Non-executing source-inspection helper for the JARVIS reliability case study.

Reads a Python source file as text. Does not import the target, run audio, access
credentials, connect to an API or make changes to the inspected project.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def analyse(source: str) -> dict[str, bool]:
    """Search for code patterns worth investigating; not proof of bugs."""
    return {
        "Live session resumption configured": "SessionResumptionConfig(" in source,
        "Resumption update handling visible": "session_resumption_update" in source,
        "Bounded outgoing audio queue": "asyncio.Queue(maxsize=" in source,
        "Nonblocking queue insertion": "put_nowait" in source,
        "Explicit QueueFull handling visible": "QueueFull" in source,
        "Reconnect loop visible": "Reconnecting" in source or "reconnect" in source.lower(),
        "Turn completion handling visible": "turn_complete" in source,
        "Partial transcript buffers visible": "in_buf" in source and "out_buf" in source,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Path to a local Python source file to inspect")
    args = parser.parse_args()
    if not args.source.is_file():
        parser.error(f"File not found: {args.source}")
    if args.source.suffix != ".py":
        parser.error("Please provide a Python (.py) file")
    source = args.source.read_text(encoding="utf-8")
    print(f"Source inspection: {args.source.name}")
    for label, present in analyse(source).items():
        print(f"[{'found' if present else 'not seen'}] {label}")
    print("\nPattern matches are investigation leads, not confirmed faults or fixes.")


if __name__ == "__main__":
    main()
