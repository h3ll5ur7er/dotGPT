from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label
from textual.message import Message
from textual.app import on
from textual.events import Key
from ..models.schema import ChatSettings

class ChatSettingsModal(ModalScreen):
    """A modal dialog for editing chat settings."""

    def __init__(self, chat_settings: ChatSettings):
        super().__init__()
        self.chat_settings = chat_settings

    def compose(self):
        """Create child widgets for the dialog."""
        with Vertical(classes="settings-modal"):
            yield Label("Chat Settings", classes="settings-title")
            yield Label("Name:")
            yield Input(value=self.chat_settings.name, id="name-input")
            
            with Vertical(classes="button-container"):
                yield Button("Save", variant="primary", id="save")
                yield Button("Cancel", variant="default", id="cancel")

    @on(Button.Pressed)
    def handle_button_press(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        match event.button.id:
            case "save":
                self.handle_submit()
            case "cancel":
                self.handle_cancel()
    @on(Key)
    def handle_key_press(self, event: Key) -> None:
        """Handle key presses."""
        match event.key:
            case "enter":
                self.handle_submit()
            case "escape":
                self.handle_cancel()

    def handle_submit(self) -> None:
        """Handle the submit action."""
        new_settings = self.chat_settings.model_copy(update={
            "name": self.query_one("#name-input").value
        })
        self.dismiss((True, self.chat_settings, new_settings))

    def handle_cancel(self) -> None:
        """Handle the cancel action."""
        self.dismiss((False, self.chat_settings, None))  