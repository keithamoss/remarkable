"""Document-wide visual configuration and page order."""

from dataclasses import dataclass, field
from typing import Union


@dataclass(frozen=True)
class RawLatex:
    value: str


Text = Union[str, RawLatex]


@dataclass(frozen=True)
class Theme:
    # Page geometry (reMarkable 2: 1404 x 1872 px @ 226 dpi), in millimetres
    page_width: float = 157.8
    page_height: float = 210.4
    left_margin: float = 13.0
    top_margin: float = 5.0
    right_margin: float = 2.5
    bottom_margin: float = 5.0

    # Typography, in points
    header_size: float = 17
    section_size: float = 10.5
    emphasis_size: float = 10
    compact_body_size: float = 9.5
    body_size: float = 9
    label_size: float = 8.5
    note_size: float = 8
    small_size: float = 7.5
    footer_size: float = 7.5

    # Grayscale intensity (0 = black, 1 = white)
    text_gray: float = 0.15
    label_gray: float = 0.3
    heading_gray: float = 0.35
    muted_gray: float = 0.4
    footer_gray: float = 0.55
    guide_gray: float = 0.6
    writing_line_gray: float = 0.7
    faint_gray: float = 0.75

    # Drawing dimensions, in millimetres
    rule_width: float = 0.15
    strong_rule_width: float = 0.3
    form_rule_width: float = 0.25
    faint_rule_width: float = 0.12
    vertical_rule_width: float = 0.1
    checkbox_size: float = 3.2
    checkbox_rule_width: float = 0.12

    @property
    def left(self) -> float:
        return self.left_margin

    @property
    def right(self) -> float:
        return self.page_width - self.right_margin

    @property
    def top(self) -> float:
        return self.top_margin

    @property
    def bottom(self) -> float:
        return self.page_height - self.bottom_margin


@dataclass(frozen=True)
class DocumentConfig:
    theme: Theme = field(default_factory=Theme)
    page_order: tuple[str, ...] = (
        "daily",
        "weekly",
        "projects",
        "waiting_for",
        "someday",
    )


CONFIG = DocumentConfig()
