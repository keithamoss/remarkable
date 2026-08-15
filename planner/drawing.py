"""Theme-aware TikZ drawing primitives used by every page."""

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Optional

from .config import RawLatex, Text, Theme


class RenderContext:
    def __init__(self, theme: Theme):
        self.theme = theme

    @property
    def left(self) -> float:
        return self.theme.left

    @property
    def right(self) -> float:
        return self.theme.right

    @property
    def top(self) -> float:
        return self.theme.top

    @property
    def bottom(self) -> float:
        return self.theme.bottom

    def latex_text(self, text: Text) -> str:
        if isinstance(text, RawLatex):
            return text.value

        replacements = {
            "\\": r"\textbackslash{}",
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
        }
        return "".join(replacements.get(character, character) for character in text)

    def node(
        self,
        x: float,
        y: float,
        text: Text,
        size: Optional[float] = None,
        bold: bool = False,
        italic: bool = False,
        gray: float = 0,
        anchor: str = "north west",
    ) -> str:
        size = self.theme.body_size if size is None else size
        extra = ""
        if bold:
            extra += r"\bfseries"
        if italic:
            extra += r"\itshape"
        black_pct = round((1 - gray) * 100)
        leading = round(size * 1.2, 1)
        rendered_text = self.latex_text(text)
        return (
            f"\\node[anchor={anchor}, inner sep=0pt, text=black!{black_pct}, "
            f"font=\\fontsize{{{size}pt}}{{{leading}pt}}\\selectfont{extra}] "
            f"at ({x:.2f}mm,{-y:.2f}mm) {{{rendered_text}}};"
        )

    def hline(
        self,
        x1: float,
        y: float,
        x2: float,
        gray: Optional[float] = None,
        width: Optional[float] = None,
    ) -> str:
        gray = self.theme.guide_gray if gray is None else gray
        width = self.theme.rule_width if width is None else width
        black_pct = round((1 - gray) * 100)
        return f"\\draw[black!{black_pct}, line width={width}mm] ({x1:.2f}mm,{-y:.2f}mm) -- ({x2:.2f}mm,{-y:.2f}mm);"

    def vline(
        self,
        x: float,
        y1: float,
        y2: float,
        gray: Optional[float] = None,
        width: Optional[float] = None,
    ) -> str:
        gray = self.theme.faint_gray if gray is None else gray
        width = self.theme.vertical_rule_width if width is None else width
        black_pct = round((1 - gray) * 100)
        return f"\\draw[black!{black_pct}, line width={width}mm] ({x:.2f}mm,{-y1:.2f}mm) -- ({x:.2f}mm,{-y2:.2f}mm);"

    def checkbox(
        self,
        x: float,
        y: float,
        size: Optional[float] = None,
        gray: Optional[float] = None,
        width: Optional[float] = None,
    ) -> str:
        size = self.theme.checkbox_size if size is None else size
        gray = self.theme.text_gray if gray is None else gray
        width = self.theme.checkbox_rule_width if width is None else width
        black_pct = round((1 - gray) * 100)
        return f"\\draw[black!{black_pct}, line width={width}mm] ({x:.2f}mm,{-y:.2f}mm) rectangle ({x+size:.2f}mm,{-(y+size):.2f}mm);"

    def box(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        gray: Optional[float] = None,
        line_width: Optional[float] = None,
    ) -> str:
        gray = self.theme.text_gray if gray is None else gray
        line_width = (
            self.theme.vertical_rule_width if line_width is None else line_width
        )
        black_pct = round((1 - gray) * 100)
        return f"\\draw[black!{black_pct}, line width={line_width}mm] ({x:.2f}mm,{-y:.2f}mm) rectangle ({x+width:.2f}mm,{-(y+height):.2f}mm);"

    def footer(self, text: str, page_number: int, page_count: int) -> str:
        page_label = f"page {page_number} of {page_count}"
        label = (
            RawLatex(f"{self.latex_text(text)}  \\textbullet{{}}  {page_label}")
            if text
            else page_label
        )
        return self.node(
            self.theme.page_width / 2,
            self.bottom,
            label,
            size=self.theme.footer_size,
            italic=True,
            gray=self.theme.footer_gray,
            anchor="north",
        )

    def checklist_row(
        self,
        commands: list[str],
        y: float,
        label: Text,
        size: Optional[float] = None,
        gray: Optional[float] = None,
    ) -> None:
        size = self.theme.body_size if size is None else size
        gray = self.theme.text_gray if gray is None else gray
        commands.append(self.checkbox(self.left, y))
        commands.append(self.node(self.left + 6, y - 0.3, label, size=size, gray=gray))

    def page_header(self, commands: list[str], title: str, subtitle: str) -> float:
        commands.append(
            self.node(
                self.left, self.top, title, size=self.theme.header_size, bold=True
            )
        )
        commands.append(
            self.node(
                self.right,
                self.top,
                subtitle,
                size=self.theme.label_size,
                italic=True,
                gray=self.theme.heading_gray,
                anchor="north east",
            )
        )
        commands.append(
            self.hline(
                self.left,
                self.top + 8,
                self.right,
                gray=0,
                width=self.theme.strong_rule_width,
            )
        )
        return self.top + 14

    def table(
        self,
        commands: list[str],
        y: float,
        columns: Sequence[tuple[float, str]],
        row_count: int,
        row_height: float,
    ) -> None:
        for x, label in columns:
            commands.append(
                self.node(
                    x,
                    y,
                    label,
                    size=self.theme.note_size,
                    bold=True,
                    gray=self.theme.heading_gray,
                )
            )

        y += 4
        commands.append(
            self.hline(
                self.left,
                y,
                self.right,
                gray=self.theme.text_gray,
                width=self.theme.strong_rule_width,
            )
        )
        y += 6

        dividers = [x - 3 for x, _ in columns[1:]]
        for _ in range(row_count):
            commands.append(
                self.hline(
                    self.left,
                    y + row_height - 3,
                    self.right,
                    gray=self.theme.faint_gray,
                    width=self.theme.faint_rule_width,
                )
            )
            for x in dividers:
                commands.append(self.vline(x, y - 2, y + row_height - 3))
            y += row_height


@dataclass
class PageCanvas:
    context: RenderContext
    y: float = 0
    commands: list[str] = field(default_factory=list)

    @classmethod
    def start(cls, context: RenderContext, title: str, subtitle: str) -> "PageCanvas":
        canvas = cls(context)
        canvas.y = context.page_header(canvas.commands, title, subtitle)
        return canvas

    @property
    def theme(self) -> Theme:
        return self.context.theme

    @property
    def left(self) -> float:
        return self.context.left

    @property
    def right(self) -> float:
        return self.context.right

    @property
    def top(self) -> float:
        return self.context.top

    @property
    def bottom(self) -> float:
        return self.context.bottom

    def advance(self, distance: float) -> None:
        self.y += distance

    def node(
        self,
        x: float,
        text: Text,
        *,
        y_offset: float = 0,
        size: Optional[float] = None,
        bold: bool = False,
        italic: bool = False,
        gray: float = 0,
        anchor: str = "north west",
    ) -> None:
        self.commands.append(
            self.context.node(
                x,
                self.y + y_offset,
                text,
                size=size,
                bold=bold,
                italic=italic,
                gray=gray,
                anchor=anchor,
            )
        )

    def hline(
        self,
        x1: float,
        x2: float,
        *,
        y_offset: float = 0,
        gray: Optional[float] = None,
        width: Optional[float] = None,
    ) -> None:
        self.commands.append(
            self.context.hline(
                x1,
                self.y + y_offset,
                x2,
                gray=gray,
                width=width,
            )
        )

    def checkbox(self, x: float, *, y_offset: float = 0) -> None:
        self.commands.append(self.context.checkbox(x, self.y + y_offset))

    def box(
        self,
        x: float,
        width: float,
        height: float,
        *,
        y_offset: float = 0,
    ) -> None:
        self.commands.append(self.context.box(x, self.y + y_offset, width, height))

    def checklist_row(
        self,
        label: Text,
        *,
        size: Optional[float] = None,
        gray: Optional[float] = None,
    ) -> None:
        self.context.checklist_row(
            self.commands,
            self.y,
            label,
            size=size,
            gray=gray,
        )

    def table(
        self,
        columns: Sequence[tuple[float, str]],
        row_count: int,
        row_height: float,
    ) -> None:
        self.context.table(
            self.commands,
            self.y,
            columns,
            row_count,
            row_height,
        )

    def footer(self, text: str, page_number: int, page_count: int) -> None:
        self.commands.append(self.context.footer(text, page_number, page_count))
