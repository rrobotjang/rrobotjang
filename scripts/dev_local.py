#!/usr/bin/env python3
"""Run selected Spring services locally without Docker.

Usage:
  python scripts/dev_local.py --services auth-service api-gateway
"""
from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICES_DIR = ROOT / "services"


def start_service(name: str) -> subprocess.Popen:
    service_dir = SERVICES_DIR / name
    if not service_dir.exists():
        raise FileNotFoundError(f"Service not found: {name}")
    cmd = ["gradle", "bootRun"]
    return subprocess.Popen(cmd, cwd=service_dir)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--services", nargs="+", required=True)
    args = parser.parse_args()

    procs: list[subprocess.Popen] = []

    def shutdown(*_):
        for p in procs:
            if p.poll() is None:
                p.terminate()
        time.sleep(1)
        for p in procs:
            if p.poll() is None:
                p.kill()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    for name in args.services:
        procs.append(start_service(name))
        print(f"started: {name}")

    while True:
        for p in procs:
            if p.poll() is not None:
                return p.returncode or 1
        time.sleep(1)


if __name__ == "__main__":
    raise SystemExit(main())
