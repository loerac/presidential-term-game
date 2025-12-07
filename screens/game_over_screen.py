from typing import Optional
from textual.app import ComposeResult
from textual.containers import Vertical, Center
from textual.widgets import Header, Footer, Button, Static
from textual.screen import Screen

from config import get_css_path
from screens.constants import ButtonId
from screens.scoreboard_screen import ScoreboardScreen


class GameOverScreen(Screen):
    """Screen displayed when user has answered all the president’s term or
    player has given up."""

    CSS_PATH = get_css_path("game_over_screen.tcss")
    BINDINGS = [
        ("s", "view_scoreboard", "View Scoreboard"),
        ("r", "restart", "Restart Quiz"),
        ("q", "quit", "Quit"),
    ]

    def __init__(
        self,
        score: int,
        total_questions: int,
        duration: int,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        """Initialize the Game Over screen with the final score."""
        super().__init__(name, id, classes)
        self.score = score
        self.total_questions = total_questions
        self.duration = duration

    def compose(self) -> ComposeResult:
        """Create the final widgets."""
        yield Header()
        yield Footer()

        percentage = 0
        if self.total_questions > 0:
            percentage = (self.score / self.total_questions) * 100

        with Vertical(id="GameOverContainer"):
            yield Static("Game Over", classes="title")
            yield Static(
                f"You finished the quiz with a final score of {self.score} out of {self.total_questions}"
                f" ({percentage:.0f}%) in {self.duration:.1f} seconds!",
                classes="message",
            )
            with Center():
                yield Button("Restart Quiz", id=ButtonId.RESTART)
                yield Button("View Scoreboard", id=ButtonId.VIEW_SCOREBOARD)
                yield Button("Quit Application", id=ButtonId.QUIT)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        match event.button.id:
            case ButtonId.RESTART:
                self.action_restart()
            case ButtonId.VIEW_SCOREBOARD:
                self.action_view_scoreboard()
            case ButtonId.QUIT:
                self.action_quit()

    def action_restart(self) -> None:
        """Trigger the main application to restart the quiz."""
        self.app.action_restart_quiz()

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()

    def action_view_scoreboard(self) -> None:
        """Pushes the scoreboard screen."""
        self.app.push_screen(ScoreboardScreen())
