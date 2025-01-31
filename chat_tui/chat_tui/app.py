from textual.app import App

from .screens.chat import ChatScreen

class ChatApp(App):
    """A Textual app for chat interface."""
    
    CSS = """
    Screen {
        align: center middle;
    }
    
    .chat-screen {
        width: 100%;
        height: 100%;
        background: $surface;
    }
    
    .left-panel {
        width: 25%;
        height: 100%;
        border-right: solid $primary;
        background: $surface-darken-1;
        overflow: auto;
    }
    
    .right-panel {
        width: 75%;
        height: 100%;
        background: $surface;
        overflow: auto;
    }
    
    MessageView {
        height: 1fr;
        border: solid $primary;
        border-bottom: none;
        padding: 1 2;
        background: $surface;
        overflow-y: scroll;
    }
    
    MessageInput {
        dock: bottom;
        border: solid $primary;
        height: 3;
        padding: 0 2;
        background: $surface-darken-1;
    }
    
    ListView {
        background: transparent;
        border: none;
        width: 100%;
        height: 100%;
        padding: 0;
    }
    
    ListItem {
        padding: 1 2;
        width: 100%;
        height: auto;
        background: transparent;
        border: none;
    }
    
    ListItem:hover {
        background: $accent-darken-2;
        color: $text;
        text-style: bold;
    }
    
    ListItem.--highlight {
        background: $accent;
        color: $text;
        text-style: bold italic;
    }
    
    .active {
        background: $accent;
        color: $text;
        text-style: bold italic;
    }
    
    .chat-item {
        width: 100%;
        height: auto;
        padding: 0;
    }
    
    .chat-item-content {
        width: 100%;
        height: auto;
        padding: 1 2;
    }
    
    .chat-name {
        width: 1fr;
        content-align: left middle;
    }
    
    .settings-button {
        background: transparent;
        border: none;
        width: 3;
        min-width: 3;
        max-width: 3;
        height: 1;
        padding: 0;
        margin: 0;
        content-align: center middle;
    }
    
    .settings-button:hover {
        background: $accent;
    }
    
    .settings-modal {
        background: $surface;
        padding: 1 2;
        border: solid $primary;
        min-width: 40;
        max-width: 60;
        min-height: 10;
        max-height: 20;
    }
    
    .settings-title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }
    
    .button-container {
        margin-top: 1;
        height: auto;
        align: center middle;
    }
    
    Button {
        margin: 1 1;
    }

    Header {
        background: $primary;
        color: $text;
        height: 3;
        content-align: center middle;
        text-style: bold;
    }
    
    Footer {
        background: $primary;
        color: $text;
    }
    """
    
    def on_mount(self) -> None:
        """Called when app is mounted."""
        self.push_screen(ChatScreen())

def main():
    app = ChatApp()
    app.run()

if __name__ == "__main__":
    main() 