"""Services for rendering and compiling the configured planner document."""

import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

import jinja2

from .config import DocumentConfig, Theme
from .drawing import RenderContext
from .pages import PAGE_BUILDERS


@dataclass(frozen=True)
class GeneratorPaths:
    root: Path
    template_name: str = "template.tex.jinja"
    tex_name: str = "remarkable_template.tex"
    pdf_name: str = "remarkable-gtd-template.pdf"

    @property
    def tex_path(self) -> Path:
        return self.root / "build" / self.tex_name

    @property
    def final_pdf_path(self) -> Path:
        return self.root / "dist" / self.pdf_name


class TectonicError(RuntimeError):
    pass


def build_pages(config: DocumentConfig) -> list[list[str]]:
    """Build TikZ command lists in configured page order."""
    unknown_pages = set(config.page_order) - PAGE_BUILDERS.keys()
    if unknown_pages:
        names = ", ".join(sorted(unknown_pages))
        raise ValueError(f"Unknown page name(s) in config.page_order: {names}")

    context = RenderContext(config.theme)
    page_count = len(config.page_order)
    return [
        PAGE_BUILDERS[name](context, page_number, page_count)
        for page_number, name in enumerate(config.page_order, start=1)
    ]


def render_latex(config: DocumentConfig, paths: GeneratorPaths) -> str:
    """Render configured pages into the LaTeX document template."""
    return render_command_pages(build_pages(config), paths, config.theme)


def render_command_pages(
    command_pages: list[list[str]], paths: GeneratorPaths, theme: Theme
) -> str:
    """Render prebuilt TikZ command lists into the LaTeX document template."""
    tikz_pages = [
        "\\begin{tikzpicture}[remember picture, overlay, "
        "shift={(current page.north west)}]\n"
        + "\n".join(commands)
        + "\n\\end{tikzpicture}"
        for commands in command_pages
    ]
    body = "\n\\newpage\n".join(tikz_pages)

    environment = jinja2.Environment(
        block_start_string="\\BLOCK{",
        block_end_string="}",
        variable_start_string="\\VAR{",
        variable_end_string="}",
        comment_start_string="\\#{",
        comment_end_string="}",
        line_statement_prefix="%%",
        line_comment_prefix="%#",
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(str(paths.root)),
    )
    return environment.get_template(paths.template_name).render(
        body=body,
        paper_width=theme.page_width,
        paper_height=theme.page_height,
    )


def compile_with_tectonic(tex_path: Path) -> Path:
    """Compile a LaTeX source file with Tectonic and return its PDF path."""
    print(
        "Running Tectonic... (first run may take a minute while packages are downloaded)"
    )
    result = subprocess.run(
        ["tectonic", "--keep-logs", "--keep-intermediates", tex_path.name],
        cwd=tex_path.parent,
        text=True,
    )
    if result.returncode != 0:
        raise TectonicError("tectonic failed -- see output above")
    return tex_path.with_suffix(".pdf")


def generate_pdf(config: DocumentConfig, paths: GeneratorPaths) -> Path:
    """Render, compile, and copy the configured planner PDF."""
    return generate_command_pdf(build_pages(config), paths, config.theme)


def generate_command_pdf(
    command_pages: list[list[str]], paths: GeneratorPaths, theme: Theme
) -> Path:
    """Render, compile, and copy prebuilt planner pages."""
    build_dir = paths.tex_path.parent
    build_dir.mkdir(parents=True, exist_ok=True)
    paths.final_pdf_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(
        prefix=f".{paths.tex_path.stem}-", dir=build_dir
    ) as temporary_dir:
        temporary_tex_path = Path(temporary_dir) / paths.tex_name
        temporary_tex_path.write_text(
            render_command_pages(command_pages, paths, theme),
            encoding="utf-8",
        )
        built_pdf = compile_with_tectonic(temporary_tex_path)

        descriptor, temporary_pdf_name = tempfile.mkstemp(
            prefix=f".{paths.final_pdf_path.name}.",
            suffix=".tmp",
            dir=paths.final_pdf_path.parent,
        )
        os.close(descriptor)
        temporary_pdf = Path(temporary_pdf_name)
        try:
            shutil.copyfile(built_pdf, temporary_pdf)
            os.replace(temporary_pdf, paths.final_pdf_path)
        finally:
            temporary_pdf.unlink(missing_ok=True)

    return paths.final_pdf_path
