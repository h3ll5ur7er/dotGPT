from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label
from textual.message import Message
from ..models.schema import ChatSettings

class ChatSettingsModal(ModalScreen):
    """A modal dialog for editing chat settings."""



    BINDINGS = [
        ("escape", "cancel", "Cancel"),
        ("enter", "submit", "Save"),
    ]

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

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "save":
            self.action_submit()
        else:
            self.action_cancel()

    def action_submit(self) -> None:
        """Handle the submit action."""
        new_settings = self.chat_settings.model_copy(update={
            "name": self.query_one("#name-input").value
        })
        self.dismiss((True, self.chat_settings, new_settings))



    def action_cancel(self) -> None:
        """Handle the cancel action."""
        self.dismiss((False, self.chat_settings, None))  