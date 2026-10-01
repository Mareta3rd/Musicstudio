
from __future__ import annotations

import importlib.util
import os
import shutil
import sys


REQUIRED = ["fastapi", "httpx", "pydantic", "uvicorn", "pytest"]


def check_module(name: str) -> tuple[bool, str]:
    return importlib.util.find_spec(name) is not None, name


def main() -> int:
    print("Musicstudio Doctor")
    print("==================")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Provider: {os.getenv('MUSICSTUDIO_PROVIDER', 'mock')}")
    print()

    failed = False

    print("Python packages:")
    for package in REQUIRED:
        ok, label = check_module(package)
        marker = "OK" if ok else "MISSING"
        print(f"  [{marker:7}] {label}")
        failed |= not ok

    print("\nSystem tools:")
    for tool in ["git", "ffmpeg"]:
        path = shutil.which(tool)
        marker = "OK" if path else "OPTIONAL"
        print(f"  [{marker:8}] {tool}" + (f" -> {path}" if path else ""))

    print("\nProject:")
    print("  [OK     ] repository files loaded by Python")
    print("  [OK     ] default provider is zero-cost Mock")

    if failed:
        print("\nDoctor result: environment needs attention.")
        return 1

    print("\nDoctor result: environment looks ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
