from textual.widgets import Input
from textual.binding import Binding
from textual.message import Message

class MessageInput(Input):
    """A widget for typing messages."""
    
    BINDINGS = [
        Binding("enter", "submit", "Send", show=False),
    ]
    
    class Submitted(Message):
        """Posted when the user submits a message."""
        def __init__(self, value: str):
            self.value = value
            super().__init__()
    
    def action_submit(self) -> None:
        """Handle the submit action."""
        if self.value.strip():
            self.post_message(self.Submitted(self.value))
            self.value = "" 