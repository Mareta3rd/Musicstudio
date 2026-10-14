
from __future__ import annotations

import os
import subprocess
import sys


def main() -> int:
    host = os.getenv("MUSICSTUDIO_HOST", "127.0.0.1")
    port = os.getenv("MUSICSTUDIO_PORT", "8000")
    return subprocess.call([
        sys.executable,
        "-m",
        "uvicorn",
        "musicstudio.app:app",
        "--host",
        host,
        "--port",
        port,
        "--reload",
    ])


if __name__ == "__main__":
    raise SystemExit(main())
