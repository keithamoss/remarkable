"""Projects tracker page."""

from dataclasses import dataclass

from ..drawing import PageCanvas, RenderContext


@dataclass(frozen=True)
class ProjectsConfig:
    title: str = "PROJECTS"
    subtitle: str = "Anything needing more than one step"
    note: str = (
        "Each project has a defined outcome --- only its next action lives on the Daily page"
    )
    footer: str = ""
    outcome_offset: float = 30
    next_action_offset: float = 78
    status_right_offset: float = 18
    row_count: int = 13
    row_height: float = 10.5


CONFIG = ProjectsConfig()


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

    col_outcome = page.left + config.outcome_offset
    col_next = page.left + config.next_action_offset
    col_status = page.right - config.status_right_offset
    page.table(
        columns=(
            (page.left, "PROJECT"),
            (col_outcome, "OUTCOME"),
            (col_next, "NEXT ACTION"),
            (col_status, "STATUS"),
        ),
        row_count=config.row_count,
        row_height=config.row_height,
    )

    page.footer(config.footer, page_number, page_count)
    return page.commands
