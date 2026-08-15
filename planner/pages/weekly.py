"""Weekly review page."""

from dataclasses import dataclass

from ..config import Text
from ..drawing import PageCanvas, RenderContext


@dataclass(frozen=True)
class WeeklyConfig:
    title: str = "WEEKLY"
    subtitle: str = "One per week"
    priority_prompt: str = "Top 3-4 real priorities this week"
    project_prompt: str = "Projects needing a next action lined up"
    friday_items: tuple[Text, ...] = (
        "Process every capture point to zero",
        "Review Projects --- does each have a live next action?",
        "Review Waiting For --- anything gone quiet, needs a nudge?",
        "Carried forward 2x+?  ->  Do / Delegate / Drop",
    )
    handover_items: tuple[str, ...] = (
        "Anything Director-related redirected today?",
        "Backfill cross-checked against Waiting For?",
    )
    priority_rows: int = 4
    project_rows: int = 3
    meeting_rows: int = 3


CONFIG = WeeklyConfig()


def build(context: RenderContext, page_number: int, page_count: int) -> list[str]:
    config = CONFIG
    page = PageCanvas.start(context, config.title, config.subtitle)
    theme = page.theme

    page.node(page.left, "Week of:", gray=theme.label_gray)
    page.hline(
        page.left + 16,
        page.right,
        y_offset=3.2,
        gray=theme.text_gray,
        width=theme.form_rule_width,
    )
    page.advance(12)

    page.node(
        page.left,
        "MONDAY --- SET THE FRAME",
        size=theme.section_size,
        bold=True,
    )
    page.advance(6.5)
    page.node(
        page.left,
        config.priority_prompt,
        size=theme.note_size,
        italic=True,
        gray=theme.muted_gray,
    )
    page.advance(5.5)
    for _ in range(config.priority_rows):
        page.hline(page.left, page.right)
        page.advance(6.5)

    page.advance(2)
    page.node(
        page.left,
        config.project_prompt,
        size=theme.note_size,
        italic=True,
        gray=theme.muted_gray,
    )
    page.advance(5.5)
    for _ in range(config.project_rows):
        page.hline(page.left, page.right)
        page.advance(6.5)

    page.advance(4)
    page.node(
        page.left,
        "WED / THU --- MEETING CHECK",
        size=theme.section_size,
        bold=True,
    )
    page.node(
        page.right,
        "delegate / shorten / skip?",
        size=theme.small_size,
        italic=True,
        gray=theme.muted_gray,
        anchor="north east",
    )
    page.advance(6.5)
    for _ in range(config.meeting_rows):
        page.hline(page.left, page.right)
        page.advance(6.5)

    page.advance(4)
    page.node(
        page.left,
        "FRIDAY --- FULL RESET  (20 min)",
        size=theme.section_size,
        bold=True,
    )
    page.advance(6.5)
    for label in config.friday_items:
        page.checklist_row(label)
        page.advance(6.5)

    page.advance(3)
    page.node(
        page.left,
        "HANDOVER CHECK  (acting role only)",
        size=theme.section_size,
        bold=True,
    )
    page.advance(6.5)
    for label in config.handover_items:
        page.checklist_row(label)
        page.advance(6.5)

    page.footer("Core + acting-role overlay", page_number, page_count)
    return page.commands
