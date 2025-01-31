from textual.widgets import ListItem, ListView, Label, Button
from textual.binding import Binding
from textual.reactive import reactive
from textual.widget import Widget
from textual.message import Message
from textual.containers import Horizontal
from rich.text import Text
from rich.style import Style
from ..models.schema import ChatStore, Chat, ChatSettings

class ChatList(Widget):
    """A widget that displays a list of chats."""
    
    selected_chat = reactive("", init=False)
    
    BINDINGS = [
        Binding("up", "select_previous", "Previous Chat", show=False),
        Binding("down", "select_next", "Next Chat", show=False),
    ]
    
    def __init__(self, chats: ChatStore):
        super().__init__()
        self.chats = chats

    def create_chat_item(self, chat: Chat) -> ListItem:
        """Create a list item with chat name and settings button."""
        # Create a valid ID by replacing spaces with hyphens
        button_id = f"settings-{chat.settings.name.replace(' ', '-')}"
        btn = Button("⚙", classes="settings-button", id=button_id)
        btn.payload = chat
        return ListItem(
            Horizontal(
                Label(chat.settings.name, classes="chat-name"),
                btn,
                classes="chat-item-content"
            ),
            classes="chat-item"
        )

    def update_chats(self, chats: ChatStore) -> None:
        """Update the list of chats."""
        self.chats = chats
        
        # Update the ListView
        list_view = self.query_one(ListView)
        list_view.clear()
        
        for chat in self.chats.chats:

            item = self.create_chat_item(chat)
            list_view.append(item)

            

        # Select the last chat if it was just added
        if self.chats:
            list_view.index = len(self.chats.chats) - 1



    def compose(self):
        """Create child widgets."""
        # First yield an empty ListView
        yield ListView()
    
    def on_mount(self) -> None:
        """Called when widget is mounted."""
        # Get the ListView and add items after it's mounted
        list_view = self.query_one(ListView)
        list_view.can_focus = True
        
        # Add items to the list view
        for chat in self.chats.chats:
            item = self.create_chat_item(chat)
            list_view.append(item)


    def on_list_view_selected(self, event: ListView.Selected):
        """Called when a chat is selected."""
        list_view = self.query_one(ListView)
        for item in list_view.children:
            if list_view.index == list_view.children.index(item):
                item.add_class("active")
            else:
                if item.has_class("active"):
                    item.remove_class("active")
        if list_view.index is not None:
            self.selected_chat = self.chats.chats[list_view.index].settings.name
            self.post_message(self.Selected(self.selected_chat))


    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle settings button presses."""
        if hasattr(event.button, "payload") and event.button.payload is not None:
            chat = event.button.payload
            self.post_message(self.SettingsRequested(chat.settings))


    class Selected(Message):
        """Posted when a chat is selected."""
        def __init__(self, chat_name: str):
            self.chat_name = chat_name
            super().__init__()

    class SettingsRequested(Message):
        """Posted when settings button is clicked."""
        def __init__(self, settings: ChatSettings):
            self.settings = settings
            super().__init__() 