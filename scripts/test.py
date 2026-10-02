from __future__ import annotations

import subprocess
import sys


def main() -> int:
    compile_result = subprocess.call([
        sys.executable,
        "-m",
        "compileall",
        "-q",
        "src",
        "tests",
    ])
    if compile_result != 0:
        return compile_result
    return subprocess.call([sys.executable, "-m", "pytest", "-q"])


if __name__ == "__main__":
    raise SystemExit(main())
