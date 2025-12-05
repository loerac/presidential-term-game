import random
from typing import Optional, Union

from textual.app import App, ComposeResult
from textual.containers import Center, Horizontal, Vertical
from textual.widgets import Header, Footer, Button, Static
from textual.message import Message
from textual.screen import Screen

from presidents import ALL_PRESIDENTS, President


class GameOverScreen(Screen):
    """Screen displayed when user has answered all the president’s term or has
    given up."""

    BINDINGS = [
        ("r", "restart", "Restart Quiz"),
        ("q", "quit", "Quit"),
    ]

    def __init__(
        self,
        score: int,
        total_questions: int,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        """Initialize the Game Over screen with the final score."""
        super().__init__(name, id, classes)
        self.score = score
        self.total_questions = total_questions

    def compose(self) -> ComposeResult:
        """Create the final widgets."""
        yield Header(show_clock=True)
        yield Footer()

        percentage = 0
        if self.total_questions > 0:
            percentage = (self.score / self.total_questions) * 100

        with Vertical(id="GameOverContainer"):
            yield Static("Game Over", classes="title")
            yield Static(
                f"You finished the quiz with a final score of {self.score} out of {self.total_questions} ({percentage:.0f}%)!",
                classes="message",
            )
            with Center():
                yield Button("Restart Quiz", id="restart", variant="success")
                yield Button("Quit Application", id="quit", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        match event.button.action:
            case "restart":
                self.action_restart()
            case "quit":
                self.action_quit()

    def action_restart(self) -> None:
        """Restart the quiz by returning to the main screen."""
        self.app.push_screen(QuizScreen())

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()


class QuizScreen(Screen):
    """The main screen for the quiz game."""

    BINDINGS = [
        ("a", "check_choice(0)", "Choice A"),
        ("b", "check_choice(1)", "Choice B"),
        ("c", "check_choice(2)", "Choice C"),
        ("d", "check_choice(3)", "Choice D"),
        ("g", "game_over", "Give up"),
        ("n", "next_question", "Next question"),
    ]
    curr_president = None
    curr_choices = []

    class ChoiceSelected(Message):
        """A message sent when a choice button is pressed or key is hit."""

        def __init__(self, selected_year: int) -> None:
            super().__init__()
            self.selected_year = selected_year

    def compose(self) -> ComposeResult:
        """Create the main widgets for the screen."""
        yield Header(show_clock=True)
        yield Footer()

        with Vertical(id="QuizContainer"):
            yield Static("Loading...", id="QuestionText")
            with Horizontal(id="ChoicesContainer"):
                yield Button("A. Choice A", id="choice-0", variant="primary")
                yield Button("B. Choice B", id="choice-1", variant="primary")
                yield Button("C. Choice C", id="choice-2", variant="primary")
                yield Button("D. Choice D", id="choice-3", variant="primary")
            yield Static(
                "Select the correct term year for the President above.",
                id="FeedbackText",
            )
            yield Button(
                "Next President", id="NextButton", variant="success", disabled=True
            )

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.remaining_presidents = list(ALL_PRESIDENTS)
        random.shuffle(self.remaining_presidents)

        self.score = 0
        self.total_questions_answered = 0

        self.update_header()
        self.next_question()

    def update_header(self) -> None:
        """Update the Header widget with the current score"""
        header = self.query_one(Header)
        header.tall = True

    def get_random_president(self) -> Union[President, None]:
        """Selects a random president from the list."""
        if not self.remaining_presidents:
            self.app.pop_screen()
            self.app.push_screen(
                GameOverScreen(self.score, self.total_questions_answered)
            )
            return

        return self.remaining_presidents.pop()

    def next_question(self) -> None:
        """Sets up the next question."""
        self.curr_president = self.get_random_president()
        # if self.curr_president is None:
        # self.app.pop_screen()
        # self.app.push_screen(
        # GameOverScreen(self.score, self.total_questions_answered)
        # )
        # return
        self.curr_choices = self.curr_president.generate_choices()

        # Get references to widgets
        question_text = self.query_one("#QuestionText", Static)
        feedback_text = self.query_one("#FeedbackText", Static)
        next_button = self.query_one("#NextButton", Button)

        question_text.update(
            f"When was {self.curr_president.name}, the {self.curr_president.ordinal} President, in term?"
        )
        feedback_text.update("Select the correct term year for the President above.")
        next_button.disabled = True

        for i, year in enumerate(self.curr_choices):
            button = self.query_one(f"#choice-{i}", Button)
            button.label = f"{chr(65 + i)}. {year}"
            button.disabled = False
            button.variant = "primary"

    def action_next_question(self) -> None:
        """Action handler to go to next question"""
        self.next_question()

    def action_game_over(self) -> None:
        """Action handler to go to Game Over screen"""
        self.app.pop_screen()
        self.app.push_screen(GameOverScreen(self.score, self.total_questions_answered))
        return

    def action_check_choice(self, index: int) -> None:
        """Action handler for key bindings (a, b, c, d)."""
        if self.curr_president is None:
            return

        # Check if a choice was already made
        button = self.query_one(f"#choice-{index}", Button)
        if not button.disabled:
            self.post_message(self.ChoiceSelected(self.curr_choices[index]))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button clicks."""
        if event.button.id and event.button.id.startswith("choice-"):
            index = int(event.button.id.split("-")[-1])
            selected_year = self.curr_choices[index]
            self.post_message(self.ChoiceSelected(selected_year))

        elif event.button.id == "NextButton":
            self.next_question()

    def on_quiz_screen_choice_selected(self, message: ChoiceSelected) -> None:
        """Handle the user selecting a choice."""
        if self.curr_president is None:
            return

        selected_year = message.selected_year
        is_correct = self.curr_president.within_term(selected_year)

        feedback_text = self.query_one("#FeedbackText", Static)
        next_button = self.query_one("#NextButton", Button)

        # A choice was already made, increment values
        if next_button.disabled:
            self.total_questions_answered += 1
            if is_correct:
                self.score += 1
            self.update_header()

        # Disable all choice buttons after a selection is made
        for i in range(4):
            button = self.query_one(f"#choice-{i}", Button)
            button.disabled = True

            if self.curr_choices[i] == selected_year:
                if is_correct:
                    button.variant = "success"
                else:
                    button.variant = "error"

            # Highlight the correct answer if the choice was wrong
            if not is_correct and self.curr_president.within_term(self.curr_choices[i]):
                button.variant = "warning"

        next_button.disabled = False
        msg = f"{self.curr_president.name} was President in between {self.curr_president.start} - {self.curr_president.end}"
        if is_correct:
            feedback_text.update(f"Correct! {msg}.")
        else:
            correct_year = self.curr_president.get_correct_year(self.curr_choices)
            feedback_text.update(
                f"❌ Wrong! The correct year was {correct_year}. {msg}"
            )


class PresidentQuizApp(App[None]):
    """A Textual app for the President Term Quiz."""

    TITLE = "Presidential Term Quiz"
    CSS_PATH = "app.tcss"
    SCREENS = {"game_over": GameOverScreen}

    def on_mount(self) -> None:
        self.push_screen(QuizScreen())


if __name__ == "__main__":
    app = PresidentQuizApp()
    app.run()
