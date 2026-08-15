"""Someday/maybe ideas page."""

from dataclasses import dataclass

from ..drawing import PageCanvas, RenderContext


@dataclass(frozen=True)
class SomedayConfig:
    title: str = "SOMEDAY / MAYBE"
    subtitle: str = "Ideas + ``we should fix X'' thoughts"
    footer: str = "Review at the Friday reset"
    row_count: int = 22
    row_spacing: float = 7.2


CONFIG = SomedayConfig()


def build(context: RenderContext, page_number: int, page_count: int) -> list[str]:
    config = CONFIG
    page = PageCanvas.start(context, config.title, config.subtitle)

    for _ in range(config.row_count):
        page.hline(
            page.left,
            page.right,
            gray=page.theme.writing_line_gray,
            width=page.theme.faint_rule_width,
        )
        page.advance(config.row_spacing)

    page.footer(config.footer, page_number, page_count)
    return page.commands
