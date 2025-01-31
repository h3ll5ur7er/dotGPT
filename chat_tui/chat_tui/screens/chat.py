from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.binding import Binding
from textual.widgets import Header, Footer
from datetime import datetime
from typing import Tuple
from ..widgets.chat_list import ChatList
from ..widgets.message_view import MessageView
from ..widgets.input_box import MessageInput
from ..widgets.chat_settings import ChatSettingsModal
from ..models.mock_data import generate_mock_data
from ..models.schema import Chat, Message, ChatSettings


class ChatScreen(Screen):
    """The main chat screen of the application."""
    
    BINDINGS = [
        Binding("escape", "quit", "Quit", show=True),
        Binding("tab", "focus_next", "Focus Next", show=True),
        Binding("^n", "new_chat", "New chat", show=True),
        Binding("^e", "edit_chat", "Edit chat", show=True),
    ]
    
    def __init__(self):
        super().__init__()
        self.chats = generate_mock_data()
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Header()
        
        with Horizontal():
            # Left panel with chat list (1/4 of the width)
            with Vertical(classes="left-panel"):
                yield ChatList(self.chats)
            
            # Right panel with messages and input (3/4 of the width)
            with Vertical(classes="right-panel"):
                yield MessageView()
                yield MessageInput(placeholder="Type a message...")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when the screen is mounted."""
        self.add_class("chat-screen")
        # Select the first chat by default
        first_chat = self.chats.chats[0]
        self.update_messages(first_chat.settings.name)
    

    def on_chat_list_selected(self, message: ChatList.Selected) -> None:
        """Called when a chat is selected."""
        self.update_messages(message.chat_name)
    
    def update_messages(self, chat_name: str) -> None:
        """Update the message view with messages from the selected chat."""
        message_view = self.query_one(MessageView)
        chat = next((chat for chat in self.chats.chats if chat.settings.name == chat_name), [])
        message_view.update_messages(chat.messages)
    
    def on_message_input_submitted(self, message: MessageInput.Submitted) -> None:
        """Called when a message is submitted."""
        # Get the current chat
        chat_list = self.query_one(ChatList)
        current_chat_name = chat_list.selected_chat
        
        if not current_chat_name:
            return  # No chat selected
            
        # Find the current chat
        current_chat = next((chat for chat in self.chats.chats if chat.settings.name == current_chat_name), None)
        if not current_chat:
            return
            
        # Create and append the new message
        new_message = Message(
            sender="user",
            message=message.value,
            timestamp=datetime.now()
        )
        current_chat.messages.append(new_message)
        
        # Update the message view
        self.update_messages(current_chat_name)
    
    def action_quit(self) -> None:
        """Quit the application when escape is pressed."""
        self.app.exit()
    
    def action_new_chat(self) -> None:
        """An [action](/guide/actions) to create a new chat."""
        self.chats.chats.append(Chat(name="New Chat", messages=[]))
        # Update the chat list widget
        chat_list = self.query_one(ChatList)
        chat_list.update_chats(self.chats)
        chat_list.selected_chat = "New Chat"
        self.update_messages("New Chat")

    async def on_chat_list_settings_requested(self, message: ChatList.SettingsRequested) -> None:
        """Handle settings button click."""
        modal = ChatSettingsModal(message.settings)
        result = await self.app.push_screen(modal, callback=self._chat_settings_modal_changed)
        # If modal was dismissed without saving, no need to handle changes
        if not result:
            return

    def _chat_settings_modal_changed(self, result: Tuple[bool, ChatSettings, ChatSettings]) -> None:
        """Handle chat settings changes."""

        success, old_settings, new_settings = result

        # If modal was dismissed without saving, no need to handle changes
        if not success:
            return
        # Find and rename the chat
        chat = next((chat for chat in self.chats.chats if chat.settings == old_settings), None)
        if chat:

            old_name = chat.settings.name
            chat.settings = new_settings
            # Update the chat list
            chat_list = self.query_one(ChatList)
            chat_list.update_chats(self.chats)
            # Make sure the chat is selected and messages are updated
            chat_list.selected_chat = new_settings.name


            self.update_messages(new_settings.name)
            # Print for debugging
            print(f"Chat renamed from {old_name} to {new_settings.name}")
            print(f"Current chats: {[chat.settings.name for chat in self.chats.chats]}")



    async def action_edit_chat(self) -> None:
        """Open settings for the current chat."""
        chat_list = self.query_one(ChatList)
        if chat_list.selected_chat:
            result = await self.app.push_screen(ChatSettingsModal(chat_list.selected_chat))
            # If modal was dismissed without saving, no need to handle changes
            if not result:
                return
