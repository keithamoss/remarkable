"""Daily planner page."""

from dataclasses import dataclass

from ..drawing import PageCanvas, RenderContext


@dataclass(frozen=True)
class DailyConfig:
    title: str = "DAILY"
    subtitle: str = "Duplicate this page each morning"
    focus_label: str = "Before 9am --- Protected focus block"
    first_email_label: str = "9:00 --- First email pass (triage only, don't answer yet)"
    action_contexts: str = "@Email   @Quick   @Person   @Desk"
    landing_pad_title: str = "LANDING PAD  (meetings / where I left off + next step)"
    deep_work_label: str = "After lunch --- Protected deep block"
    second_email_label: str = "12:30 --- Second email pass (work @Email actions)"
    sweep_items: tuple[str, ...] = (
        "Anything uncaptured today?",
        "Waiting For list updated?",
        "Tomorrow's top 3 set?",
    )
    action_rows: int = 9
    landing_pad_rows: int = 3


CONFIG = DailyConfig()


def build(context: RenderContext, page_number: int, page_count: int) -> list[str]:
    config = CONFIG
    page = PageCanvas.start(context, config.title, config.subtitle)
    theme = page.theme

    page.node(page.left, "Date:", gray=theme.label_gray)
    page.hline(
        page.left + 10,
        page.left + 45,
        y_offset=3.2,
        gray=theme.text_gray,
        width=theme.form_rule_width,
    )
    page.node(page.left + 50, "Top 3 today:", gray=theme.label_gray)
    page.hline(
        page.left + 78,
        page.right,
        y_offset=3.2,
        gray=theme.text_gray,
        width=theme.form_rule_width,
    )
    page.advance(10)

    page.checklist_row(config.focus_label, size=theme.emphasis_size)
    page.advance(8)
    page.checklist_row(config.first_email_label, size=theme.compact_body_size)
    page.advance(9)

    page.node(page.left, "NEXT ACTIONS", size=theme.section_size, bold=True)
    page.node(
        page.right,
        config.action_contexts,
        size=theme.small_size,
        italic=True,
        gray=theme.muted_gray,
        anchor="north east",
    )
    page.advance(7)
    for _ in range(config.action_rows):
        page.checkbox(page.left)
        page.box(page.left + 6, 12, theme.checkbox_size)
        page.hline(page.left + 21, page.right, y_offset=2.5)
        page.advance(6)

    page.advance(3)
    page.node(
        page.left,
        config.landing_pad_title,
        size=theme.compact_body_size,
        bold=True,
    )
    page.advance(6)
    for _ in range(config.landing_pad_rows):
        page.hline(page.left, page.right)
        page.advance(6)

    page.advance(2)
    page.checklist_row(config.deep_work_label, size=theme.emphasis_size)
    page.advance(7.5)
    page.node(
        page.left + 6,
        "Project:",
        size=theme.label_size,
        gray=theme.label_gray,
    )
    page.hline(
        page.left + 22,
        page.left + 85,
        y_offset=3.2,
        gray=theme.text_gray,
        width=theme.form_rule_width,
    )
    page.node(
        page.left + 90,
        "Next action:",
        size=theme.label_size,
        gray=theme.label_gray,
    )
    page.hline(
        page.left + 118,
        page.right,
        y_offset=3.2,
        gray=theme.text_gray,
        width=theme.form_rule_width,
    )
    page.advance(10)

    page.checklist_row(config.second_email_label, size=theme.compact_body_size)
    page.advance(9)

    page.node(
        page.left,
        "END OF DAY SWEEP  (10 min)",
        size=theme.section_size,
        bold=True,
    )
    page.advance(6.5)
    for label in config.sweep_items:
        page.checklist_row(label)
        page.advance(6)

    page.footer("Core system", page_number, page_count)
    return page.commands
