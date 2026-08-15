"""Delegated and waiting-for tracker page."""

from dataclasses import dataclass

from ..drawing import PageCanvas, RenderContext


@dataclass(frozen=True)
class WaitingForConfig:
    title: str = "WAITING FOR"
    subtitle: str = "Anything delegated or redirected"
    note: str = "Log the date. If it goes quiet, this is what tells you to chase it."
    footer: str = ""
    delegated_offset: float = 78
    date_offset: float = 112
    done_right_offset: float = 14
    row_count: int = 15
    row_height: float = 9


CONFIG = WaitingForConfig()


def build(context: RenderContext, page_number: int, page_count: int) -> list[str]:
    config = CONFIG
    page = PageCanvas.start(context, config.title, config.subtitle)

    page.node(
        page.left,
        config.note,
        size=page.theme.note_size,
        italic=True,
        gray=page.theme.muted_gray,
    )
    page.advance(7)

    col_who = page.left + config.delegated_offset
    col_date = page.left + config.date_offset
    col_done = page.right - config.done_right_offset
    page.table(
        columns=(
            (page.left, "ITEM"),
            (col_who, "TO / DELEGATED"),
            (col_date, "DATE"),
            (col_done, "DONE"),
        ),
        row_count=config.row_count,
        row_height=config.row_height,
    )

    page.footer(config.footer, page_number, page_count)
    return page.commands
