"""Generate the reMarkable GTD template PDF."""

import sys
from pathlib import Path

from planner.config import CONFIG
from planner.generator import GeneratorPaths, TectonicError, generate_pdf


def main() -> None:
    paths = GeneratorPaths(Path(__file__).parent)
    try:
        final_pdf = generate_pdf(CONFIG, paths)
    except TectonicError as exc:
        sys.exit(str(exc))
    print(f"Wrote {final_pdf}")


if __name__ == "__main__":
    main()
