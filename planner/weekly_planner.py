"""Date-driven weekly planner page."""

from datetime import date, timedelta

from .config import RawLatex
from .drawing import RenderContext
from .pages.daily import CONFIG as DAILY_CONFIG
from .pages.weekly import CONFIG as WEEKLY_CONFIG


def _monday_for(day: date) -> date:
    return day - timedelta(days=day.weekday())


def _add_week_label(commands: list[str], context: RenderContext, day: date) -> None:
    theme = context.theme
    monday = _monday_for(day)
    commands.append(
        context.node(
            theme.right,
            10,
            f"Week of {monday.day} {monday.strftime('%B')}",
            size=theme.small_size,
            gray=theme.muted_gray,
            anchor="north east",
        )
    )


def build_week_page(context: RenderContext, day: date) -> list[str]:
    """Build a weekly planner page containing the week that includes ``day``."""
    theme = context.theme
    monday = _monday_for(day)
    week = [monday + timedelta(days=offset) for offset in range(7)]
    month_date = week[3]
    commands: list[str] = []

    left = theme.left
    right = theme.right

    month_label = RawLatex(
        f"\\fontfamily{{opensans-TLF}}\\selectfont\\bfseries {month_date.strftime('%B')}"
    )
    commands.append("\\begin{scope}[xshift=2pt]")
    commands.append(context.node(left, 5, month_label, size=21))
    theme_label_x = left + (right - left) * 0.25 + 3.8
    commands.append(
        context.node(
            theme_label_x,
            7,
            "Theme:",
            size=theme.label_size,
            bold=True,
            gray=theme.heading_gray,
        )
    )
    commands.append(
        context.hline(
            theme_label_x,
            10.5,
            right,
            gray=theme.guide_gray,
            width=theme.rule_width,
        )
    )
    commands.append(context.hline(left, 14, right, gray=0, width=0.35))

    weekday_top = 20.5
    routine_content_height = 21.6
    routine_top = theme.bottom - routine_content_height
    weekday_gap = 1.5
    weekday_span = routine_top - weekday_top - weekday_gap
    weekday_height = (weekday_span - 4 * weekday_gap) / 5
    for offset, current_day in enumerate(week[:5]):
        top = weekday_top + offset * (weekday_height + weekday_gap)
        _add_weekday_row(commands, context, current_day, top, weekday_height)

    _add_daily_routine(commands, context, routine_top)
    commands.append("\\end{scope}")

    return commands


def build_scratchpad_page(context: RenderContext, day: date) -> list[str]:
    """Build a full-page dot-grid scratchpad."""
    theme = context.theme
    commands = ["\\begin{scope}[xshift=2pt]"]
    title = RawLatex("\\fontfamily{opensans-TLF}\\selectfont\\bfseries Scratchpad")

    commands.append(context.node(theme.left, 5, title, size=21))
    _add_week_label(commands, context, day)
    commands.append(context.hline(theme.left, 14, theme.right, gray=0, width=0.35))

    dot_spacing = 5
    row_count = int((theme.page_height - 28) / dot_spacing) + 1
    column_count = int((theme.right - theme.left) / dot_spacing) + 1
    for row in range(row_count):
        y = 22 + row * dot_spacing
        for column in range(column_count):
            x = theme.left + column * dot_spacing
            commands.append(f"\\fill[black!25] ({x:.2f}mm,{-y:.2f}mm) circle (0.10mm);")

    commands.append("\\end{scope}")
    return commands


def build_weekly_review_page(context: RenderContext, day: date) -> list[str]:
    """Build a compact capture and Friday reset page."""
    theme = context.theme
    left = theme.left
    right = theme.right
    commands = ["\\begin{scope}[xshift=2pt]"]
    title = RawLatex("\\fontfamily{opensans-TLF}\\selectfont\\bfseries Weekly Review")

    commands.append(context.node(left, 5, title, size=21))
    _add_week_label(commands, context, day)
    commands.append(context.hline(left, 14, right, gray=0, width=0.35))

    y = 20.5
    y = _add_review_table(
        commands,
        context,
        y,
        "PROJECTS",
        "Line up the next actions for this week.",
        ((left, "PROJECT"), (left + 52.87, "NEXT ACTIONS")),
        row_count=5,
        row_height=7.5,
    )
    y = _add_review_table(
        commands,
        context,
        y + 5,
        "WAITING FOR",
        "Log the date; chase it if it goes quiet.",
        ((left, "ITEM"), (left + 82, "SITTING WITH"), (right - 24, "DATE")),
        row_count=5,
        row_height=7.5,
    )

    y += 5
    commands.append(context.node(left, y, "Someday Maybe", size=10, bold=True))
    commands.append(
        context.node(
            right,
            y,
            "Park it here; reconsider during Friday reset.",
            size=theme.small_size,
            italic=True,
            gray=theme.muted_gray,
            anchor="north east",
        )
    )
    y += 6
    trigger_x = left + 98
    commands.append(
        context.node(
            left,
            y,
            "IDEA",
            size=theme.small_size,
            bold=True,
            gray=theme.heading_gray,
        )
    )
    commands.append(
        context.node(
            trigger_x,
            y,
            "TRIGGER",
            size=theme.small_size,
            bold=True,
            gray=theme.heading_gray,
        )
    )
    y += 4
    commands.append(
        context.hline(left, y, right, gray=theme.guide_gray, width=theme.rule_width)
    )
    someday_row_height = 7.5
    someday_bottom = y + 6 * someday_row_height
    commands.append(
        context.vline(
            trigger_x - 3,
            y,
            someday_bottom,
            gray=theme.faint_gray,
            width=theme.faint_rule_width,
        )
    )
    for row in range(1, 7):
        row_y = y + row * someday_row_height
        commands.append(
            context.hline(
                left,
                row_y,
                right,
                gray=theme.writing_line_gray,
                width=theme.faint_rule_width,
            )
        )

    reset_top = someday_bottom + 5
    commands.append(
        context.node(left, reset_top, "FRIDAY --- FULL RESET", size=10, bold=True)
    )
    for index, label in enumerate(WEEKLY_CONFIG.friday_items):
        row_y = reset_top + 4 + index * 4
        commands.append(context.checkbox(left, row_y, size=2.8))
        commands.append(
            context.node(
                left + 4.5,
                row_y - 0.2,
                label,
                size=theme.small_size,
                gray=theme.text_gray,
            )
        )

    commands.append("\\end{scope}")
    return commands


def _add_review_table(
    commands: list[str],
    context: RenderContext,
    y: float,
    title: str,
    guidance: str,
    columns: tuple[tuple[float, str], ...],
    row_count: int,
    row_height: float,
) -> float:
    theme = context.theme
    left = theme.left
    right = theme.right
    commands.append(context.node(left, y, title, size=10, bold=True))
    commands.append(
        context.node(
            right,
            y,
            guidance,
            size=theme.small_size,
            italic=True,
            gray=theme.muted_gray,
            anchor="north east",
        )
    )
    y += 6

    for x, label in columns:
        commands.append(
            context.node(
                x,
                y,
                label,
                size=theme.small_size,
                bold=True,
                gray=theme.heading_gray,
            )
        )
    y += 4
    commands.append(
        context.hline(left, y, right, gray=theme.guide_gray, width=theme.rule_width)
    )

    dividers = [x - 3 for x, _ in columns[1:]]
    table_bottom = y + row_count * row_height
    for divider in dividers:
        commands.append(
            context.vline(
                divider,
                y,
                table_bottom,
                gray=theme.faint_gray,
                width=theme.faint_rule_width,
            )
        )
    for row in range(1, row_count + 1):
        row_y = y + row * row_height
        commands.append(
            context.hline(
                left,
                row_y,
                right,
                gray=theme.writing_line_gray,
                width=theme.faint_rule_width,
            )
        )
    return table_bottom


def _add_daily_routine(
    commands: list[str],
    context: RenderContext,
    top: float,
) -> None:
    theme = context.theme
    left = theme.left
    right = theme.right
    column_width = (right - left) / 2
    second_column = left + column_width
    row_top = top + 5.5
    row_spacing = 4.5
    routine_items = (
        "Before 9AM --- protected focus",
        "9AM --- email triage",
        "12:30 --- work @Email actions",
        "After lunch --- protected deep work",
    )

    commands.append(
        context.node(left, top, "DAILY ROUTINE", size=theme.section_size, bold=True)
    )
    commands.append(
        context.node(
            second_column + 3,
            top + row_spacing,
            "END OF DAY",
            size=theme.small_size,
            bold=True,
            gray=theme.heading_gray,
        )
    )

    for column_left, first_row_y, items in (
        (left, row_top, routine_items),
        (second_column + 3, row_top + row_spacing, DAILY_CONFIG.sweep_items),
    ):
        for index, label in enumerate(items):
            row_y = first_row_y + index * row_spacing
            commands.append(
                context.checkbox(
                    column_left,
                    row_y,
                    size=2.6,
                    gray=theme.text_gray,
                )
            )
            commands.append(
                context.node(
                    column_left + 4.5,
                    row_y - 0.2,
                    label,
                    size=theme.small_size,
                    gray=theme.text_gray,
                )
            )


def _add_weekday_row(
    commands: list[str],
    context: RenderContext,
    current_day: date,
    top: float,
    height: float,
) -> None:
    theme = context.theme
    left = theme.left
    right = theme.right
    width = right - left
    list_right = left + width * 0.25
    writing_width = (right - list_right) / 2
    second_block = list_right + writing_width
    content_top = top + 6
    content_bottom = top + height - 2.5
    writing_row_height = (content_bottom - content_top) / 4
    first_item_line_y = content_top + 1.75 * writing_row_height
    day_title_bottom = top + 12 * 25.4 / 72
    subheading_height = 9 * 25.4 / 72
    first_item_top = first_item_line_y - 3
    subheading_y = (day_title_bottom + first_item_top - subheading_height) / 2

    commands.append(
        context.node(
            left,
            top,
            f"{current_day.strftime('%A')} {current_day.day}",
            size=10,
            bold=True,
        )
    )
    commands.append(
        context.node(
            left + 2,
            subheading_y,
            "Top 3 today",
            size=theme.small_size,
            bold=True,
            gray=theme.heading_gray,
        )
    )
    commands.append(
        context.node(
            list_right + 3,
            top,
            "Prj:",
            size=theme.label_size,
            bold=True,
            gray=theme.heading_gray,
        )
    )

    first_project_x = list_right + 13
    second_project_x = second_block + 3
    for project_number, project_x in enumerate(
        (first_project_x, second_project_x), start=1
    ):
        commands.append(
            context.node(
                project_x,
                top,
                f"{project_number}.",
                size=theme.small_size,
                gray=0.4,
            )
        )

    commands.append(
        context.hline(
            first_project_x,
            top + 3.5,
            second_block - 3,
            gray=theme.guide_gray,
            width=theme.rule_width,
        )
    )
    commands.append(
        context.hline(
            second_project_x,
            top + 3.5,
            right - 3,
            gray=theme.guide_gray,
            width=theme.rule_width,
        )
    )

    commands.append(
        context.vline(
            second_block,
            content_top,
            content_bottom,
            gray=theme.faint_gray,
            width=theme.faint_rule_width,
        )
    )

    for index in range(3):
        item_line_y = content_top + (index + 1.75) * writing_row_height
        item_y = item_line_y - 3
        commands.append(
            context.node(
                left + 2,
                item_y,
                f"{index + 1}.",
                size=theme.label_size,
                bold=True,
                gray=theme.heading_gray,
            )
        )
        commands.append(
            context.hline(
                left + 7,
                item_line_y,
                list_right - 3,
                gray=theme.guide_gray,
                width=theme.rule_width,
            )
        )

    for block_left in (list_right, second_block):
        line_left = block_left + 3
        line_right = block_left + writing_width - 3
        line_gap = 2
        available_width = line_right - line_left - line_gap
        short_width = available_width * 0.3 * 0.7
        for row in range(4):
            line_y = content_top + (row + 0.75) * writing_row_height
            commands.append(
                context.node(
                    line_left + 0.8,
                    line_y - 3,
                    "@",
                    size=theme.small_size,
                    gray=0.4,
                )
            )
            commands.append(
                context.hline(
                    line_left,
                    line_y,
                    line_left + short_width,
                    gray=theme.guide_gray,
                    width=theme.rule_width,
                )
            )
            commands.append(
                context.hline(
                    line_left + short_width + line_gap,
                    line_y,
                    line_right,
                    gray=theme.guide_gray,
                    width=theme.rule_width,
                )
            )
