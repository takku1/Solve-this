"""Run an exact argv in a chosen directory, retaining UTF-8 logs and exit status."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("Provide a command after --")
    args.log.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    started = time.monotonic()
    with args.log.open("w", encoding="utf-8") as output:
        proc = subprocess.run(command, cwd=args.cwd, env=env, stdout=output,
                              stderr=subprocess.STDOUT, encoding="utf-8")
    metadata = {"argv": command, "cwd": str(args.cwd.resolve()),
                "returncode": proc.returncode,
                "elapsed_seconds": round(time.monotonic() - started, 3)}
    args.log.with_suffix(args.log.suffix + ".json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    text = args.log.read_text(encoding="utf-8")
    print(json.dumps(metadata))
    print("\n".join(text.splitlines()[-14:]))
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
