import random
from typing import Union

from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Button, Static
from textual.screen import Screen
from textual.message import Message

from models.presidents import President, ALL_PRESIDENTS
from screens import GameOverScreen, constants
from screens.constants import ButtonVariant


class QuizScreen(Screen):
    """The main screen for the quiz game."""

    CSS_PATH = "../css/quiz_screen.tcss"
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
        yield Header()
        yield Footer()

        with Vertical(id="QuizContainer"):
            yield Static(constants.FLAG_ART, id="FlagArt")
            yield Static("Loading...", id="QuestionText")
            with Horizontal(id="ChoicesContainer"):
                yield Button(
                    "A. Choice A", id="choice-0", variant=ButtonVariant.PRIMARY
                )
                yield Button(
                    "B. Choice B", id="choice-1", variant=ButtonVariant.PRIMARY
                )
                yield Button(
                    "C. Choice C", id="choice-2", variant=ButtonVariant.PRIMARY
                )
                yield Button(
                    "D. Choice D", id="choice-3", variant=ButtonVariant.PRIMARY
                )
            yield Static(
                "Select the correct term year for the President above.",
                id="FeedbackText",
            )
            yield Button(
                "Next President",
                id="NextButton",
                variant=ButtonVariant.DEFAULT,
                disabled=True,
            )

    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.remaining_presidents = list(ALL_PRESIDENTS)
        random.shuffle(self.remaining_presidents)

        self.score = 0
        self.total_questions_answered = 0

        self.next_question()

    def get_random_president(self) -> Union[President, None]:
        """Selects a random president from the list."""
        if not self.remaining_presidents:
            self.app.pop_screen()
            game_over_screen = GameOverScreen(
                score=self.score, total_questions=self.total_questions_answered
            )
            self.app.push_screen(game_over_screen)
            return

        return self.remaining_presidents.pop()

    def next_question(self) -> None:
        """Sets up the next question."""
        self.curr_president = self.get_random_president()
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
            button.variant = ButtonVariant.PRIMARY

    def action_next_question(self) -> None:
        """Action handler to go to next question"""
        self.next_question()

    def action_game_over(self) -> None:
        """Action handler to go to Game Over screen"""
        self.app.pop_screen()

        game_over_screen = GameOverScreen(
            score=self.score, total_questions=self.total_questions_answered
        )
        self.app.push_screen(game_over_screen)
        return

    def action_check_choice(self, index: int) -> None:
        """Action handler for key bindings (a, b, c, d)."""
        button = self.query_one(f"#choice-{index}", Button)
        if not button.disabled and self.curr_president is not None:
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

        # Disable all choice buttons after a selection is made
        for i in range(4):
            button = self.query_one(f"#choice-{i}", Button)
            button.disabled = True

            current_choice = self.curr_choices[i]
            if current_choice == selected_year:
                if is_correct:
                    button.variant = ButtonVariant.SUCCESS
                else:
                    button.variant = ButtonVariant.ERROR

            # Highlight the correct answer if the choice was wrong
            if not is_correct and self.curr_president.within_term(current_choice):
                button.variant = ButtonVariant.SUCCESS

        next_button.disabled = False
        next_button.label = "Next President"
        if not self.remaining_presidents:
            next_button.label = "Finish Quiz"

        msg = f"{self.curr_president.name} was President in between {self.curr_president.start} - {self.curr_president.end}"
        if is_correct:
            feedback_text.update(f"Correct! {msg}.")
        else:
            correct_year = self.curr_president.get_correct_year(self.curr_choices)
            feedback_text.update(
                f"❌ Wrong! The correct year was {correct_year}. {msg}"
            )
