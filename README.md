# reMarkable GTD Daily/Weekly Planner

Planner PDFs for the reMarkable 2, generated from Python and LaTeX/TikZ rather
than hand-placed PDF coordinates. The repository provides a reusable 5-page GTD
template and a dated 6-page, two-week planner.

**Pages:** Daily, Weekly, Projects, Waiting For, Someday/Maybe — a lightweight
GTD-style system (Next Actions with context tags, a Projects tracker, a Waiting
For log with dates, and a Someday/Maybe parking lot), built around a two-pass
email triage and a protected deep-work block.

## Requirements

- Python 3.9+
- Tectonic (https://tectonic-typesetting.github.io)

## Install

1. Install Tectonic with Homebrew.

```bash
brew install tectonic
```

2. Create and activate a virtual environment (recommended).

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install Python dependencies.

```bash
pip install -r requirements.txt
```

## Usage

Generate the reusable template:

```bash
python3 generate.py
```

The finished PDF is written to `dist/remarkable-gtd-template.pdf`.

Generate the dated planner. By default, its first set starts on the Monday of
the following week; the second set covers the week after that. Pass any date
in a different desired first week to override the default:

```bash
python3 generate_weekly.py
python3 generate_weekly.py --date 2026-08-10
```

Weekly PDFs are written to `dist/weekly-planner-YYYY-WNN.pdf`, using the ISO
week-year and week number. Each document contains two consecutive weekly sets.
Each set includes its weekly planner, a combined capture and Weekly Review
page, and a dot-grid Scratchpad.
Weekly pages have full-width Monday-Friday planning areas with numbered
priorities, project fields, paired writing blocks, and daily routine checklists.

## Using it on the reMarkable

Import the PDF (drag-and-drop in the desktop app, email-in, or the web
uploader). On the **Daily** page, use reMarkable's **duplicate page** each
morning so you always start fresh. **Projects**, **Waiting For**, and
**Someday/Maybe** are standing pages — write on them directly and duplicate
only when a page fills up.

## Customizing

The `planner` package keeps document-wide settings separate from page-specific
content and layout:

- `planner/config.py` contains the shared `Theme` and
  `DocumentConfig.page_order`.
- `planner/pages/` contains one module per page: `daily.py`, `weekly.py`,
  `projects.py`, `waiting_for.py`, and `someday.py`. Each module has a local
  `CONFIG` dataclass containing that page's copy, row counts, spacing, and
  column positions.
- `planner/drawing.py` contains the TikZ primitives and `PageCanvas`, which
  owns each page's command list and vertical cursor. Page modules use explicit
  `advance()` calls, so spacing remains easy to inspect and change.
- `planner/weekly_planner.py` contains the date-driven weekly, Weekly Review,
  and Scratchpad layouts used by `generate_weekly.py`.
- `planner/generator.py` assembles pages, renders the Jinja template, runs
  Tectonic in an isolated temporary build directory, and atomically publishes
  the finished PDF to `dist/`.
- `generate.py` and `generate_weekly.py` are the two command-line entry points.

Page dimensions and margins are configured in `Theme`, in millimetres:

```python
page_width: float = 157.8
page_height: float = 210.4
left_margin: float = 13.0
top_margin: float = 5.0
right_margin: float = 2.5
bottom_margin: float = 5.0
```

The configured width and height are passed into the LaTeX template, so custom
page dimensions affect both the drawing coordinates and the generated PDF.

Ordinary content strings are escaped for LaTeX, so characters such as `&`,
`%`, `_`, and `#` are safe to type. Wrap a value in `RawLatex(...)` only when
you intentionally want to include LaTeX markup.

Each page module exports the same function:

```python
def build(context: RenderContext, page_number: int, page_count: int) -> list[str]:
    ...
```

Register a new page name in `planner/pages/__init__.py`, add it to
`DocumentConfig.page_order`, then run `python generate.py` again.

`template.tex.jinja` is the LaTeX skeleton. It receives the rendered page body
and paper dimensions from the generator, so you should not need to touch it
unless you want to change fonts or page-level LaTeX packages.

## A gotcha worth knowing if you touch the coordinate helpers

The TikZ pictures use `overlay, shift={(current page.north west)}` to place
content in absolute page coordinates. **Do not** add `x=1mm, y=-1mm` (or any
negative-`y` unit vector) to the `tikzpicture` options to get a
"y grows downward" coordinate system — combined with `overlay`, that
silently drops *all* drawn content, with no error or warning. Instead, the
coordinate helpers negate `y` themselves before emitting it, so the rest of
the code can still use an intuitive downward-growing cursor. If pages start
rendering blank after an edit, this is the first thing to check.

`generate.py` compiles with Tectonic, which automatically handles any required
reruns for cross-references.

## License

MIT — see `LICENSE`.
