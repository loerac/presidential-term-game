from textual.app import App
from textual.screen import Screen

from config import get_css_path
from screens import GameOverScreen, ResultDetailScreen, ScoreboardScreen, QuizScreen


class PresidentQuizApp(App):
    """A Textual app for the President Term Quiz."""

    TITLE = "Presidential Term Quiz"
    SCREENS = {
        "details": ResultDetailScreen,
        "game_over": GameOverScreen,
        "scoreboard": ScoreboardScreen,
        "quiz": QuizScreen,
    }
    CSS_PATH = get_css_path("app.tcss")

    def on_mount(self) -> None:
        """Called after the app is mounted."""
        self.theme = "tokyo-night"
        self.push_screen("quiz")

    def action_restart_quiz(self) -> None:
        """Restart the quiz from the Game Over Screen."""
        self.pop_screen()
        self.push_screen(QuizScreen())
