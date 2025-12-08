from typing import Optional

from textual.app import ComposeResult
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.widgets import Header, Footer, Static, Button
from textual.screen import Screen
from textual.widget import Widget
from textual.binding import Binding

from config import SCOREBOARD, get_css_path
from models import GameLog, Result
from datetime import datetime


class ResultDetailScreen(Screen):
    """Shows the detailed results of a single quize game"""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back to Scoreboard", priority=True)
    ]

    CSS_PATH = get_css_path("scoreboard_screen.tcss")

    def __init__(
        self,
        log: GameLog,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.log = log

    @property
    def log(self) -> GameLog:
        return self._log

    @log.setter
    def log(self, value: GameLog) -> None:
        self._log = value

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        detail_view = Static(id="DetailView")

        # Build the content string
        content = f"Game Summary ({self.log.date.strftime('%Y-%m-%d %H:%M:%S')})\n"
        content += f"Score: {self.log.score} / {self.log.total_questions}\n"
        content += (
            f"Percentage: {(self.log.score / self.log.total_questions) * 100:0.0f}%\n"
        )
        content += f"Time: {self.log.duration:.1f} seconds\n\n"
        content += "Individual Results:\n"

        for i, result in enumerate(self.log.results):
            details = f"       President's term: {result.correct_year}"
            status = "✅ CORRECT"
            if not result.is_correct:
                status = "❌ INCORRECT"
                details += f"\n       Selected {result.selected_year}"

            content += f"  - {i+1}. {result.president.name}: {status}\n{details}\n"

        detail_view.update(content)

        with Vertical(id="GameOverContainer"):
            yield Static("Detailed Results", classes="title")
            # yield ScrollableContainer(detail_view)
            yield detail_view


class ScoreboardEntry(Widget):
    """A clickable widget to display one game log on the scoreboard"""

    can_focus: bool = True

    def __init__(self, log: GameLog, index: int) -> None:
        self.log = log
        self.index = index
        super().__init__()

    @property
    def log(self) -> GameLog:
        return self._log

    @log.setter
    def log(self, value: GameLog) -> None:
        self._log = value

    def render(self) -> str:
        date_str = self.log.date.strftime("%Y-%m-%d %H:%M")
        score_str = f"{self.log.score} / {self.log.total_questions}"
        time_str = f"{self.log.duration:.1f} seconds"

        # Determine sorting color (e.g., if this is the highest score)
        color = "white"
        if 0 == self.index:
            color = "yellow"

        return f"[b][{color}]{score_str:<10}[/][/b]{date_str:<25}{time_str:<10}  (Press ENTER for details)"

    def on_click(self) -> None:
        """Set focus to this entry when clicked."""
        self.focus()


class ScoreboardScreen(Screen):
    """Displays the list of completed quiz games."""

    CSS_PATH = get_css_path("scoreboard_screen.tcss")

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back to Game Over", priority=True),
        Binding("enter", "show_details", "View Details", show=False),
        Binding("up", "move_focus_up", "Move Up", show=False),
        Binding("down", "move_focus_down", "Move Down", show=False),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        with Vertical(id="GameOverContainer"):
            yield Static("President Quiz Scoreboard", classes="title")
            yield Static(id="ScoreboardHeader")
            yield Vertical(id="ScoreboardList")

    def on_mount(self) -> None:
        self.update_scoreboard()

    def update_scoreboard(self) -> None:
        sorted_scoreboard = sorted(
            SCOREBOARD,
            key=lambda log: (log.score, -log.duration),
            reverse=True,
        )

        # Update header
        header = self.query_one("#ScoreboardHeader", Static)
        header.update("[b]SCORE     DATE & TIME                TIME[/b]")

        # Update list
        list_container = self.query_one("#ScoreboardList", Vertical)
        list_container.remove_children()

        for i, log in enumerate(sorted_scoreboard):
            entry = ScoreboardEntry(log=log, index=i)
            list_container.mount(entry)

        # Focus the first entry
        if sorted_scoreboard:
            list_container.children[0].focus()

    def action_show_details(self) -> None:
        """Action triggered by ENTER key to show the details of the focused game."""
        focused_widget = self.focused
        if isinstance(focused_widget, ScoreboardEntry):
            self.app.push_screen(ResultDetailScreen(log=focused_widget.log))

    def action_move_focus_up(self) -> None:
        """Moves focus to the previous ScoreboardEntry in the list."""
        self._move_focus(-1)

    def action_move_focus_down(self) -> None:
        """Moves focus to the next ScoreboardEntry in the list."""
        self._move_focus(1)

    def _move_focus(self, direction: int) -> None:
        """Helper method to handle focus movement."""
        entries = self.query(ScoreboardEntry)
        if not entries:
            return

        focused_widget = self.focused
        if focused_widget is None:
            entries[0].focus()
            return

        new_index = focused_widget.index + direction
        if 0 <= new_index < len(entries):
            entries[new_index].focus()
