"""Page builder registry."""

from typing import Callable

from ..drawing import RenderContext
from .daily import build as build_daily
from .projects import build as build_projects
from .someday import build as build_someday
from .waiting_for import build as build_waiting_for
from .weekly import build as build_weekly

PageBuilder = Callable[[RenderContext, int, int], list[str]]

PAGE_BUILDERS: dict[str, PageBuilder] = {
    "daily": build_daily,
    "weekly": build_weekly,
    "projects": build_projects,
    "waiting_for": build_waiting_for,
    "someday": build_someday,
}
