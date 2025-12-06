from textual.app import App
from textual.screen import Screen
from screens import GameOverScreen, QuizScreen


class PresidentQuizApp(App):
    """A Textual app for the President Term Quiz."""

    TITLE = "Presidential Term Quiz"
    SCREENS = {
        "quiz": QuizScreen,
        "game_over": GameOverScreen,
    }
    CSS_PATH = "css/app.tcss"

    def on_mount(self) -> None:
        """Called after the app is mounted."""
        # Start the quiz by pushing the QuizScreen
        self.push_screen("quiz")

    def action_restart_quiz(self) -> None:
        """Restart the quiz from the Game Over Screen."""
        self.pop_screen()
        self.push_screen(QuizScreen())


if __name__ == "__main__":
    app = PresidentQuizApp()
    app.run()
