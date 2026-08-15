"""Generate a dated reMarkable weekly planner PDF."""

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

from planner.config import CONFIG
from planner.drawing import RenderContext
from planner.generator import GeneratorPaths, TectonicError, generate_command_pdf
from planner.weekly_planner import (
    build_scratchpad_page,
    build_week_page,
    build_weekly_review_page,
)


def _next_monday(day: date) -> date:
    return day + timedelta(days=7 - day.weekday())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--date",
        type=date.fromisoformat,
        default=_next_monday(date.today()),
        metavar="YYYY-MM-DD",
        help="a date in the first week to generate (default: next Monday)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    iso_year, iso_week, _ = args.date.isocalendar()
    paths = GeneratorPaths(
        Path(__file__).parent,
        tex_name="weekly_planner.tex",
        pdf_name=f"weekly-planner-{iso_year}-W{iso_week:02d}.pdf",
    )
    context = RenderContext(CONFIG.theme)
    following_week = args.date + timedelta(weeks=1)
    pages = [
        build_week_page(context, args.date),
        build_weekly_review_page(context, args.date),
        build_scratchpad_page(context, args.date),
        build_week_page(context, following_week),
        build_weekly_review_page(context, following_week),
        build_scratchpad_page(context, following_week),
    ]

    try:
        final_pdf = generate_command_pdf(pages, paths, context.theme)
    except TectonicError as exc:
        sys.exit(str(exc))
    print(f"Wrote {final_pdf}")


if __name__ == "__main__":
    main()
